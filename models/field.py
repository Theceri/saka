from datetime import datetime
from typing import List

from . import db

class FieldModel(db.Model):
    __tablename__ = 'fields'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    created = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow(), nullable=True)

    
    def insert_record(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetch_all(cls) -> List['FieldModel']:
        return cls.query.order_by(cls.id.asc()).all()

    @classmethod
    def fetch_paginated(cls, page_num:int) -> List['FieldModel']:
        return cls.query.paginate(per_page=20, page=page_num, error_out=True)

    @classmethod
    def fetch_by_name(cls, name:str) -> List['FieldModel']:
        return cls.query.filter_by(name=name).first()

    @classmethod
    def fetch_by_id(cls, id:int) -> 'FieldModel':
        return cls.query.get(id)

    @classmethod  
    def update(cls, id:int, name:str=None) -> None:
        record = cls.fetch_by_id(id)
        if name:
            record.name = name
        db.session.commit()

    @classmethod
    def delete_by_id(cls, id:int) -> None:
        record = cls.query.filter_by(id=id)
        record.delete()
        db.session.commit()