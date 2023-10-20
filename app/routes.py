from flask import jsonify

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_data = [{"id": hero.id, "name": hero.name} for hero in heroes]
    return jsonify(hero_data)
