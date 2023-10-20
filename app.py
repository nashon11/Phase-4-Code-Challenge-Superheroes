#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from sqlalchemy.exc import IntegrityError
from models import db, Hero, Power, HeroPowers

app = Flask(__name)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False  # Fix the JSON output setting

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)

class Heroes(Resource):
    def get(self):
        heroes = Hero.query.all()
        return jsonify([hero.serialize() for hero in heroes])

api.add_resource(Heroes, '/heroes')

class HeroesById(Resource):
    def get(self, id):
        hero = Hero.query.get(id)
        if hero:
            return jsonify(hero.serialize())
        else:
            return {'error': 'Hero not found'}, 404

api.add_resource(HeroesById, '/heroes/<int:id>')

class Powers(Resource):
    def get(self):
        powers = Power.query.all()
        return jsonify([power.serialize() for power in powers])

api.add_resource(Powers, '/powers')

class PowersById(Resource):
    def get(self, id):
        power = Power.query.get(id)
        if power:
            return jsonify(power.serialize())
        else:
            return {'error': 'Power not found'}, 404

    def patch(self, id):
        power = Power.query.get(id)

        if power is None:
            return {'error': 'Power not found'}, 404

        try:
            data = request.get_json()

            if 'description' in data:
                latest_description = data['description']
                if not latest_description:
                    return jsonify({'errors': ['Description must be present']}), 400

                if len(latest_description) < 20:
                    return jsonify({'errors': ['Description must be at least 20 characters']}), 400

                power.description = latest_description
                db.session.commit()
                return jsonify(power.serialize())
            else:
                return {'errors': ['No valid fields for updates']}, 400
        except ValueError as e:
            return jsonify({'errors': [str(e)]}), 400

api.add_resource(PowersById, '/powers/<int:id>')

class HeroPower(Resource):
    def post(self):
        try:
            data = request.get_json()
            strength = data.get('strength')
            power_id = data.get('power_id')
            hero_id = data.get('hero_id')

            power = Power.query.get(power_id)
            hero = Hero.query.get(hero_id)

            if not (power and hero):
                return jsonify({'errors': ['Power or Hero not found']}), 404

            hero_power = HeroPowers(strength=strength, power_id=power_id, hero_id=hero_id)
            db.session.add(hero_power)
            db.session.commit()

            return jsonify(hero.serialize()), 201

        except ValueError as e:
            return jsonify({'errors': [str(e)]}), 400

api.add_resource(HeroPower, '/hero_powers')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
