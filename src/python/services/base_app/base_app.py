from base64 import b64encode
from datetime import datetime, timedelta
from time import time

from fastapi import status, FastAPI, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from jsonrpcserver import async_dispatch
from passlib.context import CryptContext
from prometheus_client import make_wsgi_app
from pydantic import BaseModel
from typing import Optional
from secrets import token_bytes

from starlette.middleware.wsgi import WSGIMiddleware

from services.base_app.prometheus import REQUEST_COUNT, REQUEST_LATENCY
from services.db_services.users_db import get_user as get_user_from_db
from services.models import User

SECRET_KEY = b64encode(token_bytes(32)).decode()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str) -> User:
    user = get_user_from_db(username)
    if user:
        return User.from_orm(user)


def authenticate_user(username: str, password: str) -> Optional[User]:
    user = get_user(username)
    if not user:
        return
    if not verify_password(password, user.hashed_password):
        return
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "Bearer"}


@app.get("/health_check")
@app.post("/health_check")
async def health_check():
    return b"ok"


@app.get("/authentication_check")
@app.post("/authentication_check")
async def authentication_check(current_user: User = Depends(get_current_active_user)):
    return {'Status': 'OK'}


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time()

    response = await call_next(request)

    process_time = time() - start_time

    REQUEST_LATENCY.labels(app.title, request.url.path).observe(process_time)
    REQUEST_COUNT.labels(app.title, request.method, request.url.path, response.status_code).inc()
    return response


def get_base_app(title: str = None) -> FastAPI:
    app.title = title or app.title

    prometheus_app = make_wsgi_app()
    app.mount("/metrics", WSGIMiddleware(prometheus_app))

    return app


def get_base_rpc_app(title: str = None) -> FastAPI:
    rpc_app = get_base_app(title)

    @rpc_app.post("/")
    async def index(request: Request, current_user: User = Depends(get_current_active_user)):
        response = Response(await async_dispatch(await request.body()))
        response.headers["Content-Type"] = "application/json"
        return response

    return rpc_app
