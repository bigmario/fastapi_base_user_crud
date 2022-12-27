import bcrypt
from sqlalchemy.orm import Session

import app.core.database.models.db_models as models
import app.core.database.schemas.db_schemas as schemas


class UserRepo:
    async def create(db: Session, user: schemas.UserCreate):

        salt = bcrypt.gensalt()
        db_user = models.User(
            username=user.username,
            password=bcrypt.hashpw(user.password.encode("utf-8"), salt),
            name=user.name,
            last_name=user.last_name,
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def fetch_by_id(db: Session, _id):
        return db.query(models.User).filter(models.User.id == _id).first()

    def fetch_by_name(self, db: Session, name):
        return db.query(models.User).filter(models.User.name == name).first()

    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.User).offset(skip).limit(limit).all()

    async def delete(db: Session, user_id):
        db_user = db.query(models.User).filter_by(id=user_id).first()
        db.delete(db_user)
        db.commit()

    async def update(db: Session, user_data):
        updated_user = db.merge(user_data)
        db.commit()
        return updated_user
