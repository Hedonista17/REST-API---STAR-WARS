from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    user_name = db.Column(db.String(25),nullable=False)
    first_name = db.Column(db.String(50),nullable=False)
    last_name = db.Column(db.String(50),nullable=False)
    register_data = db.Column(db.String(50),nullable=False)  
    favorites = db.relationship("Favorites")  # relacion entre clases  1 a N = multiples favoritos,

    def __repr__(self):
        return '<User %r>' % self.user_name  # con esta forma en la bd pinta el self que queramos en esta caso el nombre de usuario en vez de poner  <User 1 por ejemplo>


    def __init__(self,email,user_name,first_name,last_name,password):  #inicio las columnas que quiero, son los datos que introduciré 
        self.email = email
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = datetime.datetime.now()  # COMPROBAR SI ES CORRECTO ESTA FORMA 
        self.password = password   
        # self.favorites = favorites.serialize() CONSULTAR
        

    def serialize(self):  #transformo a diccionario  los datos para ver una respuesta JSON /enviar a JSON
        return {
            "id": self.id,
            "email": self.email,
            "user_name":self.user_name,
            "first_name":self.user_name,
            "last_name":self.last_name,
            # do not serialize the password, its a security breach
        }



class People(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    birth_date = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(120), unique=True, nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id")) #relacion de tabla.id
    planet = db.relationship("Planet") #relacion entre clases 
    eye_color = db.Column(db.String(120), unique=True, nullable=False)
    hair_color = db.Column(db.String(120), unique=True, nullable=False)
    favorites = db.relationship("Favorites")

    def __repr__(self):
        return '<People %r>' % self.name

    def __init__(self,name,birth_date,description,eye_color,hair_color):
      self.name = name
      self.birth_date = birth_date
      self.description = description
      self.eye_color = eye_color
      self.hair_color = hair_color

    def serialize(self):
        return{
            "id": self.id,
            "name":self.name,
            "birth_day":self.birth_date,
            "description":self.description,
            "planet_id":self.planet_id,
            "eye_color":self.eye_color,
            "hair_color":self.hair_color,
        }


class Planet(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(120), unique=True, nullable=False)
    population = db.Column(db.Integer)
    terrain = db.Column(db.String(120), unique=True, nullable=False)
    climate = db.Column(db.String(120), unique=True, nullable=False)
    people = db.relationship("People")
    favorites = db.relationship("Favorites")

    def __repr__(self):
        return '<Planet %r>' % self.name
    

    def __init__(self,name,description,population,terrain,climate):

     self.name = name
     self.description = description
     self.population = population
     self.terrain = terrain
     self.climate = climate
     

    def serialize(self):
        return {
          "id": self.id,
          "name":self.name,
          "descirption":self.description,
          "population":self.population,
          "terrain": self.terrain,
          "climate":self.climate,
          
        }



class Favorites(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    planets_id= db.Column(db.Integer,db.ForeignKey("planet.id"))          #nombre de la table + id
    people_id= db.Column(db.Integer, db.ForeignKey("people.id"))
    user= db.relationship("User", back_populates="favorites") ##union de clases y tabla    #relacion class y unir tablas- inner join                           #relacion entre las class 
    planet= db.relationship("Planet",back_populates="favorites")
    people= db.relationship("People",back_populates="favorites") #insertar en la tabla favoritos las clases 
    

    def __init__(self,user_id,planets_id,people_id):

     self.user_id = user_id
     self.planets_id = planets_id
     self.people_id = people_id


    def serialize(self):
      return {
         "id":self.id,
         "user_id":self.user_id,
         "people_id":self.people_id,
         "planet_id":self.planets_id,

      }





















    # def __repr__(self):
    #     return '<User %r>' % self.username