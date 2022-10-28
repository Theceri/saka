from datetime import datetime
from typing import List

from . import db

class ApplicationModel(db.Model):
    __tablename__ = 'applications'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False, default='Created') # created, selected, disqualified
    provider_id = db.Column(db.Integer, db.ForeignKey('providers.id'), nullable=False)
    provider = db.relationship('ProviderModel')
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    job = db.relationship('JobModel')
    created = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow(), nullable=True)

    def insert_record(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetch_all(cls) -> List['ApplicationModel']:
        return cls.query.order_by(cls.id.asc()).all()

    @classmethod
    def fetch_paginated(cls, page_num:int) -> List['ApplicationModel']:
        return cls.query.paginate(per_page=20, page=page_num, error_out=True)

    # @classmethod
    # def fetch_by_name(cls, status:str) -> List['ApplicationModel']:
    #     return cls.query.filter_by(status=status).all()

    @classmethod
    def fetch_by_id(cls, id:int) -> 'ApplicationModel':
        return cls.query.get(id)

    @classmethod
    def fetch_by_provider(cls, provider_id:int) -> 'ApplicationModel':
        return cls.query.filter_by(provider_id=provider_id).all()

    # @classmethod
    # def fetch_by_job(cls, job_id:int, page_num:int) -> 'ApplicationModel':
    #     return cls.query.filter_by(job_id=job_id).paginate(per_page=20, page=page_num, error_out=True)

    @classmethod
    def fetch_by_job(cls, job_id:int) -> 'ApplicationModel':
        return cls.query.filter_by(job_id=job_id).all()

    @classmethod
    def select_applicant(cls, id:int ) -> None:
        record = cls.fetch_by_id(id)
        record.status = 'Selected'
        db.session.commit()

    @classmethod
    def disqualify_applicant(cls, id:int ) -> None:
        record = cls.fetch_by_id(id)
        record.status = 'Disqualified'
        db.session.commit()