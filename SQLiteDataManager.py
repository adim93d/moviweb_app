from flask_sqlalchemy import SQLAlchemy
from moviweb_app.data_manager_interface import DataManagerInterface
from flask import Flask
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

# Initialize the Flask app and SQLAlchemy globally
app = Flask(__name__, template_folder='templates')
db = SQLAlchemy()

class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name: str):
        self.app = app  # Use the global Flask app
        self.app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_file_name}'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(self.app)  # Initialize SQLAlchemy with the Flask app

    def create_tables(self):
        with self.app.app_context():
            db.create_all()

    def list_all_users(self):
        return db.session.query(User).all()

    def list_user_movies(self, user_id):
        return (db.session.query(Movie)
                .join(UserMovies)
                .filter(UserMovies.user_id == user_id)
                .all())

    def get_username(self, user_id):
        user = db.session.query(User).get(user_id)  # Get the user by user_id
        if user:
            return user.username  # Return the username if the user exists
        return None  # Return None if the user doesn't exist

    def add_user(self, user):
        db.session.add(user)
        db.session.commit()

    def add_movie(self, movie):
        db.session.add(movie)
        db.session.commit()

    def get_movie(self, movie_id):
        movie = db.session.query(Movie).get(movie_id)
        if movie:
            return movie
        return None

    def update_movie(self, movie):
        existing_movie = db.session.query(Movie).get(movie.movie_id)
        if existing_movie:
            existing_movie.title = movie.title
            existing_movie.director = movie.director
            existing_movie.release_year = movie.release_year
            existing_movie.rating = movie.rating
            existing_movie.img_url = movie.img_url
            db.session.commit()  # Ensure the changes are saved

    def delete_movie(self, movie_id):
        movie = db.session.query(Movie).get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()

# Define the Movie class using the global db instance
class Movie(db.Model):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    director = Column(String)
    release_year = Column(Integer)
    rating = Column(Float)
    img_url = Column(String)
    user_movies = relationship('UserMovies', back_populates='movie')

# Define the User class
class User(db.Model):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    user_movies = relationship('UserMovies', back_populates='user')

# Define the UserMovies class
class UserMovies(db.Model):
    __tablename__ = "user_movies"

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.movie_id'), primary_key=True)
    user = relationship('User', back_populates='user_movies')
    movie = relationship('Movie', back_populates='user_movies')
