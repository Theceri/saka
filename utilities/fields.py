from main import app

def get_fields():
    try:
        with app.app_context():
            from main import db
            from models.user import UserModel
            from models.provider import ProviderModel
            from models.skill import SkillModel
            from models.application import ApplicationModel
            from models.field import FieldModel

            db.create_all()
            fields = [(field.id, field.name) for field in FieldModel.fetch_all()]
            return fields
    except Exception as e:
        print('==========================')
        print(f'Error: {e}')
        print('==========================')