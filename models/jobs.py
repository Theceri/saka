from datetime import datetime
from typing import List

from . import db

class JobModel(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    qualifications = db.Column(db.Text, nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey('employers.id'), nullable=False)
    employer = db.relationship('EmployerModel')
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id'), nullable=False)
    field = db.relationship('FieldModel')
    created = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow(), nullable=True)


    def insert_record(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetch_all(cls) -> List['JobModel']:
        return cls.query.order_by(cls.id.asc()).all()

    @classmethod
    def fetch_paginated(cls, page_num:int) -> List['JobModel']:
        return cls.query.paginate(per_page=20, page=page_num, error_out=True)

    @classmethod
    def fetch_by_name(cls, name:str) -> List['JobModel']:
        return cls.query.filter_by(name=name).first()

    @classmethod
    def fetch_by_id(cls, id:int) -> 'JobModel':
        return cls.query.get(id)
    
    @classmethod
    def fetch_by_field(cls, field_id:int, page:int) -> 'JobModel':
        return cls.query.filter_by(field_id=field_id).paginate(per_page=20, page=page_num, error_out=True)

    # @classmethod
    # def fetch_by_employer(cls, employer_id:int, page:int) -> 'JobModel':
    #     return cls.query.filter_by(employer_id=employer_id).paginate(per_page=20, page=page_num, error_out=True)

    @classmethod
    def fetch_by_employer(cls, employer_id:int) -> 'JobModel':
        return cls.query.filter_by(employer_id=employer_id).all()


    @classmethod  
    def update(cls, id:int, name:str=None, description:str=None, qualifications:str=None, field_id:int=None) -> None:
        record = cls.fetch_by_id(id)
        if name:
            record.name = name
        if description:
            record.description = description
        if qualifications:
            record.qualifications = qualifications
        if field_id:
            record.field_id = field_id
        db.session.commit()


    @classmethod
    def delete_by_id(cls, id:int) -> None:
        record = cls.query.filter_by(id=id)
        record.delete()
        db.session.commit()   