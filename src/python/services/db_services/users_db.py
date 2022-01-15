import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.models import User
from services.models.user import UserDBModel

logger = logging.getLogger(__name__)


SQLALCHEMY_DATABASE_URL = 'postgresql://love_and_marriage:FoolishPassword@postgres.default:5432/users'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()


def get_users(skip: int = 0, limit: int = 100):
    return db.query(UserDBModel).offset(skip).limit(limit).all()


def get_user(user_name: str) -> User:
    return db.query(UserDBModel).filter(UserDBModel.user_name == user_name).first()


get_users()
