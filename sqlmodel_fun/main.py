import logging
from typing import Dict, Optional

from sqlmodel import JSON, Column, Field, Session, SQLModel, create_engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None
    data: Optional[Dict] = Field(default={}, sa_column=Column(JSON))

    # Needed for Column(JSON)
    class Config:
        arbitrary_types_allowed = True


sqlite_file_name = (
    "/Users/shotashimizu/github.com/banbiossa/sqlmodel-fun/db/database.db"
)
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    logger.info("create_db_and_tables")
    SQLModel.metadata.create_all(engine)
    logger.info("create_db_and_tables done")


def create_heroes():
    logger.info("create_heroes")
    hero1 = Hero(name="Deadpool", secret_name="Wade Wilson", age=28, data={"iam": "me"})
    hero2 = Hero(name="Spiderman", secret_name="Peter Parker", age=18)
    hero3 = Hero(name="Batman", secret_name="Bruce Wayne", age=36)

    with Session(engine) as session:

        session.add(hero1)
        session.add(hero2)
        session.add(hero3)
        logger.info(f"after session: {hero1}")

        session.commit()
        logger.info(f"after commit: {hero1}")
        # logger.info(f"just the name: {hero1.name}")

        # session.refresh(hero1)
        # logger.info(f"after refresh: {hero1}")
    logger.info(f"after session: {hero1}")

    logger.info("create_heroes done")


def main():
    create_db_and_tables()
    create_heroes()


if __name__ == "__main__":
    logger.info("main")
    main()
    logger.info("main done")
