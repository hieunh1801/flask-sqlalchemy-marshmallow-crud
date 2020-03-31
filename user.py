from db_config import db, ma
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Column, Integer, String, DateTime
from collections import defaultdict
from flask import abort


class UserModel(db.Model):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(500), nullable=False)
    password = Column(String(500), nullable=False)
    date_of_bird = Column(DateTime)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel


class UserCRUD():
    def get_all(page_size: int = 20, page_number: int = 1) -> (list, int):
        data = UserModel.query.paginate(
            page=page_number, per_page=page_size).items  # get all
        total = UserModel.query.paginate().total
        data_dump = UserSchema().dump(data, many=True)
        return data_dump, total

    def get_by_id(id) -> dict:
        data = UserModel.query.filter_by(id=id).one_or_none()
        user_dump = UserSchema().dump(data, many=False)
        return user_dump

    def create(user: dict) -> dict:
        try:
            new_user = UserModel(**user)
            db.session.add(new_user)
            db.session.commit()
            user_dump = UserSchema().dump(new_user, many=False)
            return user_dump
        except SQLAlchemyError as error:
            print("create error", error)
            return {}

    def delete(user_id: int) -> dict:
        try:
            user = UserModel.query.filter_by(id=user_id).one_or_none()
            if not user:
                return abort(400, "Not found id: " + str(user_id))
            else:
                user_dump = UserSchema().dump(user, many=False)
                db.session.delete(user)
                db.session.commit()
                return user_dump
        except SQLAlchemyError as error:
            print("delete error", error)
            return {}

    def update(user_id: int, user: dict) -> dict:
        try:
            patch_of_user = {key: value for key,
                             value in user.items() if value}
            user = UserModel.query.filter_by(id=user_id).one_or_none()
            if not user:
                return abort("User not exists")
            UserModel.query.filter_by(id=user_id).update(patch_of_user)
            db.session.commit()
            user_dump = UserSchema().dump(user, many=False)
            return user_dump
        except SQLAlchemyError as error:
            print("update error", error)
            return {}
