import bcrypt
from sqlalchemyseeder import ResolvingSeeder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import Settings

conf = Settings()

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{conf.db_user}:{conf.db_password}@{conf.db_host}:{conf.db_port}/{conf.db_name}"


engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()
seeder = ResolvingSeeder(db)


async def seed_database():
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw("123456789".encode("utf-8"), salt)

    user = {
        "target_class": "app.core.database.models.db_models:User",
        "data": {
            "email": "admin@mail.com",
            "name": "Admin",
            "last_name": "Admin",
            "phone": "+58-000000000",
            "password": hashed_password.decode("utf-8"),
        },
    }
    seeder.load_entities_from_data_dict(user)
    db.commit()
    db.close()
