from flask import render_template, request, redirect, url_for  # Import necessary modules from Flask
from moviweb_app.SQLiteDataManager import SQLiteDataManager, Movie, User, UserMovies, db
import requests  # Import requests for API calls


# Initialize the Flask application
data_manager = SQLiteDataManager('moviwebapp.db') # Initialize the data manager with the path to the JSON data file
data_manager.create_tables()
app = data_manager.app
# USERS = data_manager.list_all_users()  # Retrieve all users from the data manager
REQUEST_URL = 'https://www.omdbapi.com/?'  # Base URL for the OMDB API
API_KEY = 'apikey=3ac01df6'  # API key for the OMDB API
SEARCH_BY_TITLE = '&t='  # Parameter for searching by title in the OMDB API


# Function to fetch movie details from the OMDB API based on the movie title
def fetch_movie_details(movie_title):
    response = requests.get(f"{REQUEST_URL}{API_KEY}{SEARCH_BY_TITLE}{movie_title}")
    return response.json()


# Route to render the home page
@app.route('/')
def home():
    return render_template('index.html')


# Route to list all users
@app.route('/users')
def list_users():
    try:
        users = data_manager.list_all_users()
    except Exception as e:
        return render_template('error.html', message=str(e)), 500
    return render_template('users.html', users=users)


# Route to list all movies for a specific user
@app.route('/users/<user_id>')
def list_user_movies(user_id):
    try:
        user_movies = data_manager.list_user_movies(user_id)
        username = data_manager.get_username(user_id)
    except Exception as e:
        return render_template('error.html', message=str(e)), 500
    message = request.args.get('message')
    return render_template('user_movies.html', movies=user_movies, username=username, user_id=user_id, message=message)


# Route to render the form for adding a new user
@app.route('/add_user', methods=['GET'])
def add_user_form():
    return render_template('add_user.html')


# Route to handle the submission of the form to add a new user
@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form.get('name')
    try:
        new_user = User(username=username)
        data_manager.add_user(new_user)
    except Exception as e:
        return render_template('error.html', message=str(e)), 500
    return redirect(url_for('list_users'))


# Route to render the form for adding a new movie for a specific user
@app.route('/users/<user_id>/add_movie', methods=['GET'])
def add_movie_form(user_id):
    return render_template('add_movie.html', user_id=user_id)


# Route to handle the submission of the form to add a new movie for a specific user
@app.route('/users/<user_id>/add_movie', methods=['POST'])
def add_movie(user_id):
    movie_title_search = request.form.get('movie_name')
    search_result = fetch_movie_details(movie_title_search)
    try:
        if search_result.get('Response') == 'True':
            # Create a new Movie object
            movie = Movie(
                title=search_result['Title'],
                producer=search_result['Producer'],
                release_year=search_result['Year'],
                rating=search_result['imdbRating'],
                img_url=search_result['Poster']
            )
            # Add the movie to the database
            data_manager.add_movie(movie)

            # Now link the movie to the user using the UserMovies table
            user_movie = UserMovies(user_id=user_id, movie_id=movie.movie_id)
            db.session.add(user_movie)
            db.session.commit()

            message = 'Movie added and linked to the user successfully!'
        else:
            message = 'Movie not found!'
    except Exception as e:
        db.session.rollback()  # Rollback in case of an error
        return render_template('error.html', message=str(e)), 500

    return redirect(url_for('list_user_movies', user_id=user_id, message=message))


# Route to render the form for updating a movie for a specific user
@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['GET'])
def update_movie_form(user_id, movie_id):
    try:
        users = data_manager.list_user_movies(user_id)
        movie_details = data_manager.get_movie(movie_id)
    except Exception as e:
        return render_template('error.html', message=str(e)), 500
    return render_template('update_movie.html', user_id=user_id, movie_id=movie_id, movie=movie_details)


# Route to handle the submission of the form to update a movie for a specific user
@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['POST'])
def update_movie(user_id, movie_id):
    try:
        # Fetch the existing movie object by movie_id
        movie = db.session.query(Movie).get(movie_id)
        if not movie:
            raise Exception('Movie not found')

        # Update the movie object with data from the form
        movie.title = request.form.get('movie_name')
        movie.producer = request.form.get('producer')
        movie.release_year = request.form.get('year')
        movie.rating = request.form.get('rating')
        movie.img_url = request.form.get('img_url')

        # Call the data_manager to update the movie in the database
        data_manager.update_movie(movie)

    except Exception as e:
        return render_template('error.html', message=str(e)), 500

    return redirect(url_for('list_user_movies', user_id=user_id))


# Route to handle the deletion of a movie for a specific user
@app.route('/users/<user_id>/delete_movie/<movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    try:
        users = data_manager.list_user_movies(user_id)
        data_manager.delete_movie(movie_id)
    except Exception as e:
        return render_template('error.html', message=str(e)), 500
    return redirect(url_for('list_user_movies', user_id=user_id))


# # Route to handle the deletion of a user
# @app.route('/users/<user_id>/delete', methods=['POST'])
# def delete_user(user_id):
#     try:
#         users = read_data()
#         if user_id in users:
#             del users[user_id]
#             write_data(users)
#             message = 'User deleted successfully!'
#         else:
#             message = 'User not found!'
#     except Exception as e:
#         return render_template('error.html', message=str(e)), 500
#     return redirect(url_for('list_users', message=message))


# Custom error handler for 404 - Page Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Custom error handler for 500 - Internal Server Error
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', message=str(e)), 500


# Main entry point of the application
if __name__ == '__main__':
    app.run(debug=True)
