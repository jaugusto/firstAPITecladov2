from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema
from models import StoreModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("stores", __name__, description="Store Module")


@blp.route('/store/<int:store_id>')
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        return StoreModel.query.get_or_404(store_id)

    def delete(self, store_id):
        item = StoreModel.query.get_or_404(store_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "store deleted"}


@blp.route('/store')
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, data_store):
        store = StoreModel(**data_store)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A story with that already exists")
        except SQLAlchemyError:
            abort(500, message="A error occurred while tried save a store")
