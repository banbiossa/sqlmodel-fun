import logging
from pathlib import Path
from typing import Dict, Optional

from sqlmodel import (
    JSON,
    Column,
    Field,
    Session,
    SQLModel,
    col,
    create_engine,
    or_,
    select,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)
    data: Optional[Dict] = Field(default={}, sa_column=Column(JSON))

    team_id: Optional[int] = Field(default=None, foreign_key="team.id")

    # Needed for Column(JSON)
    class Config:
        arbitrary_types_allowed = True


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str


sqlite_file_name = "db/database.sqlite"
# remove db if exists (because inserting each time)
if Path(sqlite_file_name).exists():
    Path(sqlite_file_name).unlink()

sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    logger.info("create_db_and_tables")
    SQLModel.metadata.create_all(engine)
    logger.info("create_db_and_tables done")


def create_heroes():
    with Session(engine) as session:
        logger.info("create teams")
        team1 = Team(name="Avengers", headquarters="New York")
        team2 = Team(name="Wane Enterprises", headquarters="Gotham City")
        session.add(team1)
        session.add(team2)
        session.commit()

        logger.info("create_heroes")
        hero1 = Hero(
            name="Deadpool", secret_name="Wade Wilson", age=28, data={"iam": "me"}
        )
        hero2 = Hero(name="Spiderman", secret_name="Peter Parker", team_id=team1.id)
        hero3 = Hero(name="Batman", secret_name="Bruce Wayne", age=36, team_id=team2.id)
        hero4 = Hero(name="Black Widow", secret_name="Natasha Romanoff", age=30)
        hero5 = Hero(
            name="Captain America",
            secret_name="Steve Rogers",
            age=100,
            team_id=team1.id,
        )
        hero6 = Hero(
            name="Doctor Strange",
            secret_name="Stephen Strange",
            age=45,
            team_id=team1.id,
        )

        session.add(hero1)
        session.add(hero2)
        session.add(hero3)
        session.add(hero4)
        session.add(hero5)
        session.add(hero6)
        logger.info(f"after session: {hero5}")

        hero = hero5
        session.commit()
        logger.info(f"after commit: {hero}")
        # logger.info(f"just the name: {hero1.name}")

        session.refresh(hero)
        logger.info(f"after refresh: {hero}")
    logger.info(f"after session: {hero}")

    logger.info("create_heroes done")


def select_heroes():
    with Session(engine) as session:
        statement = select(Hero).offset(3).limit(3)
        results = session.exec(statement)
        for hero in results:
            logger.info(f"hero: {hero}")


def update_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spiderman")
        results = session.exec(statement)
        hero = results.one()

        hero.age = 15
        session.add(hero)
        session.commit()
        logger.info(f"before refresh: {hero=}")
        session.refresh(hero)

        logger.info(f"after refresh: {hero=}")


def delete_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Doctor Strange")
        results = session.exec(statement)
        hero = results.one()
        session.refresh(hero)

        session.delete(hero)
        session.commit()
        logger.info(f"after delete: {hero=}")


def main():
    create_db_and_tables()
    create_heroes()


#     select_heroes()
#     update_heroes()
#     delete_heroes()
#

if __name__ == "__main__":
    logger.info("main")
    main()
    logger.info("main done")
