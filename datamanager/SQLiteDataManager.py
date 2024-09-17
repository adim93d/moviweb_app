from flask_sqlalchemy import SQLAlchemy
import class_models
from data_manager_interface import DataManagerInterface


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name):
        self.db = SQLAlchemy(db_file_name)

    def list_all_users(self):
        return self.db.session.query(class_models.User).all()

    def list_user_movies(self, user_id):
        # Query movies linked to the user through UserMovies
        return (self.db.session.query(class_models.Movie)
                .join(class_models.UserMovies)
                .filter(class_models.UserMovies.user_id == user_id)
                .all())

    def add_user(self, user):
        self.db.session.add(user)
        self.db.session.commit()

    def add_movie(self, movie):
        self.db.session.add(movie)
        self.db.session.commit()

    def update_movie(self, movie):
        existing_movie = self.db.session.query(class_models.Movie).get(movie.movie_id)
        if existing_movie:
            existing_movie.title = movie.title
            existing_movie.producer = movie.producer
            existing_movie.release_year = movie.release_year
            existing_movie.rating = movie.rating
            existing_movie.img_url = movie.img_url
            self.db.session.commit()

    def delete_movie(self, movie_id):
        movie = self.db.session.query(class_models.Movie).get(movie_id)
        if movie:
            self.db.session.delete(movie)
            self.db.session.commit()
