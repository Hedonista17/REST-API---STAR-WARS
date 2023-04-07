"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,People,Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)



    ##RUTAS 

@app.route('/users', methods=['GET'])
def get_users():
    all_users= User.query.all() # consulta model.py
    serialize_all_users = list(map(lambda user : user.serialize(),all_users)) #mapeo
    return jsonify(serialize_all_users), 200

@app.route('/users/<int:id>', methods=['GET'])
def get_user_id(id):
    user = User.query.get(id)
    return(jsonify(user.serialize())), 200

@app.route('/users', methods=['POST'])       
def create_users():
    data = request.get_json() # con esto obtenemos en formato json la peticion del body 
    new_user = User(data['email'], data['user_name'], data['first_name'], data['last_name'], data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 200





@app.route('/user/favorites', methods=['GET']) ## POR REVISAR 
def get_users_favs():
    all_favs = Favorites.query.all() ## consulta model.py
    serialize_favs = list(map(lambda user : user.serialize(),all_favs)) #mapeo
    return jsonify(serialize_all_users), 200





@app.route('/people', methods=['GET'])
def get_people():
    all_people = People.query.all() ## consulta model.py
    serialize_all_people = list(map(lambda people : people.serialize(),all_people)) #mapeo
    return jsonify(serialize_all_people), 200

@app.route('/people/<int:id>', methods=['GET'])
def get_people_id(id):
    people = People.query.get(id)
    return(jsonify(people.serialize())), 200

@app.route('/people', methods=['POST'])
def create_people():
    data = request.get_json()
    new_people =  People(data['name'], data['birth_date'],data['description'],data['eye_color'],data['hair_color'])
    db.session.add(new_people)
    db.session.commit()
    return jsonify(new_people.serialize()), 200



@app.route('/planets', methods=['GET'])
def get_planet():
    all_planet= Planet.query.all() # consulta model.py
    serialize_all_planet = list(map(lambda planet : planet.serialize(),all_planet)) #mapeo
    return jsonify(serialize_all_planet), 200

@app.route('/planets/<int:id>', methods=['GET'])
def get_planets_id(id):
    planets = Planet.query.get(id)
    return(jsonify(planets.serialize())), 200

@app.route('/planets', methods=['POST'])
def create_planet():
    data = request.get_json()
    new_planet =  Planet(data['name'], data['description'],data['population'],data['terrain'],data['climate'])
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 200












# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
