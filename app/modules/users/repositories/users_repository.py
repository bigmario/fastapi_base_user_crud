import bcrypt
from sqlalchemy.orm import Session


from fastapi.exceptions import HTTPException

import app.core.database.models.db_models as models
import app.core.database.schemas.db_schemas as schemas


class UserRepo:
    async def create(self, db: Session, user: schemas.UserCreate):

        salt = bcrypt.gensalt()
        db_user = models.User(
            username=user.username,
            password=bcrypt.hashpw(user.password.encode("utf-8"), salt),
            name=user.name,
            last_name=user.last_name,
        )
        db_user.password = db_user.password.decode("utf-8")
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def fetch_by_id(self, db: Session, _id):
        return db.query(models.User).filter(models.User.id == _id).first()

    def fetch_by_name(self, db: Session, name):
        return db.query(models.User).filter(models.User.name == name).first()

    def fetch_by_username(self, db: Session, username):
        return db.query(models.User).filter(models.User.username == username).first()

    def fetch_all(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.User).offset(skip).limit(limit).all()

    def delete(self, db: Session, user_id):
        db_user = db.query(models.User).filter_by(id=user_id).first()

        if not db_user:
            raise HTTPException(status_code=404, detail="Item not exists!")

        db.delete(db_user)
        db.commit()
        return db_user

    def update(self, db: Session, user_id, user_data: schemas.UserUpdate):
        db_query = db.query(models.User).filter(models.User.id == user_id)
        db_item = db_query.first()

        if not db_item:
            raise HTTPException(status_code=404, detail="Item not exists!")

        data_dict = user_data.dict(exclude_unset=True)
        db_query.update(data_dict, synchronize_session=False)
        db.commit()
        db.refresh(db_item)
        return db_item
