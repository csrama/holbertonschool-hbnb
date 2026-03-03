from app.extensions import db
class SQLAlchemyRepository:

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, model, obj_id):
        return model.query.get(obj_id)

    def get_all(self, model):
        return model.query.all()

    def delete(self, obj):
        db.session.delete(obj)
        db.session.commit()
