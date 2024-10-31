from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings

database_uri: str = (
    f"{settings.DATABASE_DIALECT_DRIVER}://"
    f"{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@"
    f"{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/"
    f"{settings.DATABASE_NAME}"
)

engine = create_engine(url=database_uri, pool_pre_ping=True)

# a sessionmaker(), also in the same scope as the engine
# we can now construct a Session() and include begin()/commit()/rollback()
Session = sessionmaker(bind=engine, expire_on_commit=False)
