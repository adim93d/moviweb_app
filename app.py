from flask import Flask, render_template, request, redirect, url_for  # Import necessary modules from Flask
from datamanager.json_data_manager import JSONDataManager  # Import JSONDataManager for data management
import requests  # Import requests for API calls

app = Flask(__name__)  # Initialize the Flask application
data_manager = JSONDataManager('data/movie_data.json')  # Initialize the data manager with the path to the JSON data file
USERS = data_manager.get_all_users()  # Retrieve all users from the data manager
REQUEST_URL = 'https://www.omdbapi.com/?'  # Base URL for the OMDB API
API_KEY = 'apikey=3ac01df6'  # API key for the OMDB API
SEARCH_BY_TITLE = '&t='  # Parameter for searching by title in the OMDB API


# Function to get all users
def get_users():
    return data_manager.get_all_users()


# Function to get all movies for a specific user
def get_user_movies(user_id):
    return data_manager.get_user_movies(user_id)


# Function to read data from the JSON file
def read_data():
    return data_manager.read_file()


# Function to write data to the JSON file
def write_data(data):
    data_manager.write_file(data)


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
        users = get_users()
    except Exception as e:
        return render_template('error.html', message=str(e)), 500
    return render_template('users.html', users=users)


# Route to list all movies for a specific user
@app.route('/users/<user_id>')
def list_user_movies(user_id):
    try:
        user_movies = get_user_movies(user_id)
        username = USERS.get(int(user_id))
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
        users = read_data()
        new_user_id = str(max(int(user_id) for user_id in users.keys()) + 1 if users else 1)
        users[new_user_id] = {"name": username, "movies": {}}
        write_data(users)
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
            users = read_data()
            user_movies = users[user_id]['movies']
            new_movie_id = str(max(int(mid) for mid in user_movies.keys()) + 1 if user_movies else 1)
            movie_details = {
                "movie_name": search_result['Title'],
                "producer": search_result['Director'],
                "year": search_result['Year'],
                "rating": search_result['imdbRating'],
                "img_url": search_result['Poster']
            }
            users[user_id]['movies'][new_movie_id] = movie_details
            write_data(users)
            message = 'Movie added successfully!'
        else:
            message = 'Movie not found!'
    except Exception as e:
        return render_template('error.html', message=str(e)), 500
    return redirect(url_for('list_user_movies', user_id=user_id, message=message))


# Route to render the form for updating a movie for a specific user
@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['GET'])
def update_movie_form(user_id, movie_id):
    try:
        users = read_data()
        movie_details = users[user_id]['movies'][movie_id]
    except Exception as e:
        return render_template('error.html', message=str(e)), 500
    return render_template('update_movie.html', user_id=user_id, movie_id=movie_id, movie=movie_details)


# Route to handle the submission of the form to update a movie for a specific user
@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['POST'])
def update_movie(user_id, movie_id):
    try:
        users = read_data()
        movie_details = users[user_id]['movies'][movie_id]
        movie_details['movie_name'] = request.form.get('movie_name')
        movie_details['producer'] = request.form.get('producer')
        movie_details['year'] = request.form.get('year')
        movie_details['rating'] = request.form.get('rating')
        movie_details['img_url'] = request.form.get('img_url')
        write_data(users)
    except Exception as e:
        return render_template('error.html', message=str(e)), 500
    return redirect(url_for('list_user_movies', user_id=user_id))


# Route to handle the deletion of a movie for a specific user
@app.route('/users/<user_id>/delete_movie/<movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    try:
        users = read_data()
        del users[user_id]['movies'][movie_id]
        write_data(users)
    except Exception as e:
        return render_template('error.html', message=str(e)), 500
    return redirect(url_for('list_user_movies', user_id=user_id))


# Route to handle the deletion of a user
@app.route('/users/<user_id>/delete', methods=['POST'])
def delete_user(user_id):
    try:
        users = read_data()
        if user_id in users:
            del users[user_id]
            write_data(users)
            message = 'User deleted successfully!'
        else:
            message = 'User not found!'
    except Exception as e:
        return render_template('error.html', message=str(e)), 500
    return redirect(url_for('list_users', message=message))


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
