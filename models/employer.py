from datetime import datetime
from typing import List

from . import db

class EmployerModel(db.Model):
    __tablename__ = 'employers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    user = db.relationship('UserModel')
    created = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow(), nullable=True)

    jobs = db.relationship('JobModel', lazy='dynamic')

    def insert_record(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetch_all(cls) -> List['EmployerModel']:
        return cls.query.order_by(cls.id.asc()).all()

    @classmethod
    def fetch_paginated(cls, page_num:int) -> List['EmployerModel']:
        return cls.query.paginate(per_page=20, page=page_num, error_out=True)

    @classmethod
    def fetch_by_name(cls, name:str) -> List['EmployerModel']:
        return cls.query.filter_by(name=name).first()

    @classmethod
    def fetch_by_user_id(cls, user_id:str) -> List['EmployerModel']:
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def fetch_by_id(cls, id:int) -> 'EmployerModel':
        return cls.query.get(id)
    
    @classmethod  
    def update(cls, id:int, name:str=None, description:str=None, field_id:int=None) -> None:
        record = cls.fetch_by_id(id)
        if name:
            record.name = name
        if description:
            record.description = description
        if field_id:
            record.field_id = field_id
        db.session.commit()


    @classmethod
    def delete_by_id(cls, id:int) -> None:
        record = cls.query.filter_by(id=id)
        record.delete()
        db.session.commit()