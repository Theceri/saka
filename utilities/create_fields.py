from models.field import FieldModel
from main import db

def seeding():
    fields = ['Accountancy, banking and finance', 'Business, consulting and management', 'Charity and voluntary work', 'Creative arts and design', 'Energy and utilities', 'Engineering and manufacturing', 'Environment and agriculture', 'Healthcare', 'Hospitality and events management', 'Information technology', 'Law', 'Law enforcement and security', 'Leisure, sport and tourism', 'Marketing, advertising and PR', 'Media and internet', 'Property and construction', 'Public services and administration', 'Recruitment and HR', 'Retail', 'Sales', 'Science and pharmaceuticals', 'Social care', 'Teacher training and education', 'Transport and logistics']

    for field in fields:        
        exists = FieldModel.query.filter_by(name = field).first()

        if not exists:
            new_field = FieldModel(name = field)
            db.session.add(new_field)
            db.session.commit()