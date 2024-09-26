# api.py
from flask import Blueprint, jsonify, request
from moviweb_app.SQLiteDataManager import SQLiteDataManager, User, Movie, Review

# Initialize the SQLiteDataManager
data_manager = SQLiteDataManager('moviwebapp.db')

# Define the Blueprint for API routes
api = Blueprint('api', __name__)

# Route to get all users in JSON format
@api.route('/users', methods=['GET'])
def get_users():
    try:
        users = data_manager.list_all_users()
        users_data = [{'id': user.user_id, 'name': user.username} for user in users]
        return jsonify({'status': 'success', 'data': users_data}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# Route to get all movies for a specific user in JSON format
@api.route('/users/<int:user_id>/movies', methods=['GET'])
def get_user_movies(user_id):
    try:
        user_movies = data_manager.list_user_movies(user_id)
        movies_data = [{'id': movie.movie_id, 'title': movie.title, 'director': movie.director,
                        'release_year': movie.release_year, 'rating': movie.rating, 'img_url': movie.img_url}
                       for movie in user_movies]
        return jsonify({'status': 'success', 'data': movies_data}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# Route to get details of a specific movie
@api.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    try:
        movie = data_manager.get_movie(movie_id)
        if not movie:
            return jsonify({'status': 'error', 'message': 'Movie not found'}), 404

        movie_data = {'id': movie.movie_id, 'title': movie.title, 'director': movie.director,
                      'release_year': movie.release_year, 'rating': movie.rating, 'img_url': movie.img_url}
        return jsonify({'status': 'success', 'data': movie_data}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# Route to get reviews for a specific movie
@api.route('/movies/<int:movie_id>/reviews', methods=['GET'])
def get_movie_reviews(movie_id):
    try:
        reviews = data_manager.get_reviews(movie_id)
        reviews_data = [{'id': review.review_id, 'user_id': review.user_id, 'movie_id': review.movie_id,
                         'review_text': review.review_text, 'rating': review.rating} for review in reviews]
        return jsonify({'status': 'success', 'data': reviews_data}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# Route to add a new movie review
@api.route('/movies/<int:movie_id>/reviews', methods=['POST'])
def add_movie_review(movie_id):
    try:
        user_id = request.json.get('user_id')
        review_text = request.json.get('review_text')
        rating = request.json.get('rating')

        new_review = Review(user_id=user_id, movie_id=movie_id, review_text=review_text, rating=rating)
        data_manager.add_user_review(new_review)

        return jsonify({'status': 'success', 'message': 'Review added successfully!'}), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
