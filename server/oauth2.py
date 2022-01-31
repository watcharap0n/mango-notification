import pytz
from db import db
from datetime import timedelta, datetime
from firebase_admin import exceptions, auth
from models.oauth2 import Register, TokenUser, User
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, status, HTTPException, Depends, Response
from config.firebase_auth import ConfigFirebase
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config.environ.client_firebase import firebaseAuth, firebaseConfig

router = APIRouter()

collection = 'secure'
config = ConfigFirebase(path_auth=firebaseAuth, path_db=firebaseConfig)
pb = config.authentication()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/authentication/token")


def verify_password(plain_password, hashed_password):
    """

    :param plain_password:
    :param hashed_password:
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """

    :param password:
    :return:
    """
    return pwd_context.hash(password)


async def authentication_signin(
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends()
):
    try:
        sign_in = pb.sign_in_with_email_and_password(
            form_data.username, form_data.password
        )
    except exceptions.FirebaseError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Failed to create a session cookie'
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Email or password invalid'
        )
    check_verify = auth.get_user_by_email(form_data.username)
    user = await db.find_one(collection=collection, query={'email': form_data.username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                'message': 'Please contact developer',
                'email': 'wera.watcharapon@gmail'
            }
        )
    if not check_verify.email_verified:
        pb.send_email_verification(sign_in.get("idToken"))
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Email not verification!'
        )
    auth_cookie = auth.create_session_cookie(
        id_token=sign_in.get('idToken'), expires_in=timedelta(minutes=30)
    )
    response.set_cookie(key='access_token', value=str(auth_cookie))
    return {'access_token': auth_cookie, 'token_type': 'bearer'}


@router.post('/token')
async def generate_token(user=Depends(authentication_signin)):
    return user


@router.post('/register', response_model=TokenUser)
async def register(payload: Register):
    try:
        user = auth.create_user(
            email=payload.email,
            password=payload.password
        )
        tz = pytz.timezone('Asia/Bangkok')
        set_time = datetime.now(tz)
        date = set_time.strftime('%d/%m/%y')
        time = set_time.strftime('%H:%M:%S')
        uid = user.__dict__['_data']['localId']
        item_model = jsonable_encoder(payload)
        item_model['password'] = get_password_hash(payload.password)
        item_model['date'] = date
        item_model['time'] = time
        item_model['uid'] = uid
        store_model = TokenUser(**item_model)
        await db.insert_one(collection=collection, data=item_model)
        return store_model

    except auth.EmailAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Register already exists')


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """

    :param token:
    :return:
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        refresh = auth.verify_session_cookie(token)
        auth.revoke_refresh_tokens(refresh["sub"])
        return refresh
    except auth.RevokedSessionCookieError:
        return credentials_exception
    except auth.InvalidSessionCookieError:
        raise credentials_exception


async def get_current_active(current_user: dict = Depends(get_current_user)):
    store_model = User(**current_user)
    return store_model


@router.get("/user", response_model=User)
async def read_user_me(current_user: User = Depends(get_current_active)):
    """

    :param current_user:
    :return:
    """
    return current_user


@router.delete('/auth/setting/delete', status_code=status.HTTP_204_NO_CONTENT)
async def revoke_user(uid: str):
    try:
        auth.delete_user(uid)
        await db.delete_one(collection=collection, query={'uid': uid})
        return {'detail': 'revoke user success'}
    except auth.UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='No user record found for the given identifier')
