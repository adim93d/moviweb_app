from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa

db = SQLAlchemy()

class Movie(db.Model):
    __tablename__ = "movies"
    movie_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String)  # Corrected typo
    producer = sa.Column(sa.String)
    release_year = sa.Column(sa.Integer)
    rating = sa.Column(sa.Float)
    img_url = sa.Column(sa.String)
    user_movies = db.relationship('UserMovies', back_populates='movie')  # Changed 'user' to 'movie'

class User(db.Model):
    __tablename__ = "users"
    user_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    username = sa.Column(sa.String)
    user_movies = db.relationship('UserMovies', back_populates='user')

class UserMovies(db.Model):
    __tablename__ = "user_movies"
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.user_id'), primary_key=True)
    movie_id = sa.Column(sa.Integer, sa.ForeignKey('movies.movie_id'), primary_key=True)
    user = db.relationship('User', back_populates='user_movies')
    movie = db.relationship('Movie', back_populates='user_movies')
