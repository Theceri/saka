from datetime import datetime
from typing import List

from flask_login import UserMixin

from . import db

class UserModel(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    email =  db.Column(db.String(80), nullable=False, unique=True)
    phone =  db.Column(db.String(12), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow(), nullable=True)

    user_roles = db.relationship('UserRoleModel', lazy='dynamic') 
    employer = db.relationship('EmployerModel', lazy='dynamic') 
    provider = db.relationship('ProviderModel', lazy='dynamic')

    def __repr__(self):
        return '<UserModel %r>' % self.full_name


    def insert_record(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetch_all(cls) -> List['UserModel']:
        return cls.query.order_by(cls.id.asc()).all()

    @classmethod
    def fetch_by_full_name(cls, full_name:str) -> List['UserModel']:
        return cls.query.filter_by(full_name=full_name).all()

    @classmethod
    def fetch_by_id(cls, id:int) -> 'UserModel':
        return cls.query.get(id)

    @classmethod
    def fetch_by_email(cls, email:str) -> 'UserModel':
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def fetch_by_phone(cls, phone:str) -> 'UserModel':
        return cls.query.filter_by(phone=phone).first()

    @classmethod  
    def update(cls, id:int, full_name:str=None, email:str=None, phone:str=None) -> None:
        record = cls.fetch_by_id(id)
        if full_name:
            record.full_name = full_name
        if email:
            record.email = email
        if phone:
            record.phone = phone
        db.session.commit()

    @classmethod
    def update_password(cls, id:int, password:str=None) -> None:
        record = cls.fetch_by_id(id)
        if password:
            record.password = password
        db.session.commit()

    @classmethod
    def delete_by_id(cls, id:int) -> None:
        record = cls.query.filter_by(id=id)
        record.delete()
        db.session.commit()
