from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Column, Integer, String, DateTime
from flask import abort

db = SQLAlchemy()
ma = Marshmallow()


class BaseCRUD():
    def __init__(self, Model, Schema, id_field):
        self.Model = Model
        self.__tablename__ = Model.__tablename__
        self.Schema = Schema
        self.id_field = id_field

    def get_all(
            self,
            page_size: int = 20,
            page_number: int = 1) -> (list, int):
        Model = self.Model
        Schema = self.Schema
        data = Model.query.paginate(page=page_number, per_page=page_size).items
        total = Model.query.paginate().total
        data_dump = Schema().dump(data, many=True)
        return data_dump, total

    def get_by_id(self, id) -> dict:
        Model = self.Model
        Schema = self.Schema
        id_field = self.id_field
        data = Model.query.filter(getattr(Model, id_field) == id).one_or_none()
        data_dump = Schema().dump(data, many=False)
        return data_dump

    def create(self, payload: dict) -> dict:
        try:
            Model = self.Model
            Schema = self.Schema
            __tablename__ = self.__tablename__
            new_data = Model(**payload)
            db.session.add(new_data)
            db.session.commit()
            new_data_dump = Schema().dump(new_data, many=False)
            return new_data_dump
        except SQLAlchemyError as error:
            print(f"create {__tablename__} error: {error}")
            return abort(400, f"create {__tablename__} error: {error}")

    def delete(self, id: int) -> dict:
        try:
            Model = self.Model
            Schema = self.Schema
            __tablename__ = self.__tablename__
            id_field = self.id_field
            record = Model.query.filter(
                getattr(Model, id_field) == id).one_or_none()
            if not record:
                return abort(400, f"Not found {__tablename__} id: {id}")
            else:
                record_dump = Schema().dump(record, many=False)
                db.session.delete(record)
                db.session.commit()
                return record_dump
        except SQLAlchemyError as error:
            print(f"delete {__tablename__} error: {error}")
            return abort(400, f"create {__tablename__} error: {error}")

    def update(self, id: int, payload: dict) -> dict:
        try:
            Model = self.Model
            Schema = self.Schema
            __tablename__ = self.__tablename__
            id_field = self.id_field
            patch_of_payload = {key: value for key,
                                value in payload.items() if value}
            record = Model.query.filter(
                getattr(Model, id_field) == id).one_or_none()
            if not record:
                return abort(400, f"Not found {__tablename__} id: {id}")
            Model.query.filter(getattr(Model, id_field) ==
                               id).update(patch_of_payload)
            db.session.commit()
            record_dump = Schema().dump(record, many=False)
            return record_dump
        except SQLAlchemyError as error:
            print(f"delete {__tablename__} error: {error}")
            return abort(400, f"create {__tablename__} error: {error}")
