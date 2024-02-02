#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):

        all_plants = [n.to_dict() for n in Plant.query.all()]

        response = make_response(
            all_plants,
            200
        )

        return response
    
    def post(self):
        req = request.get_json()

        new_plant = Plant(
            name=req["name"],
            image=req["image"],
            price=req["price"]
        )

        print(new_plant)

        db.session.add(new_plant)
        db.session.commit()

        plant_dict = new_plant.to_dict()

        response = make_response( 
            plant_dict,
            201
        )

        return response
    
api.add_resource(Plants, '/plants')

class Plant_by_id(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first().to_dict()

        response = make_response(
            plant,
            200
        )

        return response
    
api.add_resource(Plant_by_id, '/plants/<int:id>')


class PlantByID(Resource):
    pass
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
