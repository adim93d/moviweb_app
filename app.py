from flask import Flask, render_template, request, redirect, url_for
from datamanager.json_data_manager import JSONDataManager
import requests

app = Flask(__name__)
data_manager = JSONDataManager('data/movie_data.json')
USERS = data_manager.get_all_users()
REQUEST_URL = 'https://www.omdbapi.com/?'
API_KEY = 'apikey=3ac01df6'
SEARCH_BY_TITLE = '&t='


def get_users():
    return data_manager.get_all_users()


def get_user_movies(user_id):
    return data_manager.get_user_movies(user_id)


def read_data():
    return data_manager.read_file()


def write_data(data):
    data_manager.write_file(data)


def fetch_movie_details(movie_title):
    response = requests.get(f"{REQUEST_URL}{API_KEY}{SEARCH_BY_TITLE}{movie_title}")
    return response.json()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/users')
def list_users():
    try:
        users = get_users()
    except Exception as e:
        return render_template('error.html', message=str(e)), 500
    return render_template('users.html', users=users)


@app.route('/users/<user_id>')
def list_user_movies(user_id):
    try:
        user_movies = get_user_movies(user_id)
        username = USERS.get(int(user_id))
    except Exception as e:
        return render_template('error.html', message=str(e)), 500
    message = request.args.get('message')
    return render_template('user_movies.html', movies=user_movies, username=username, user_id=user_id, message=message)


@app.route('/add_user', methods=['GET'])
def add_user_form():
    return render_template('add_user.html')


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


@app.route('/users/<user_id>/add_movie', methods=['GET'])
def add_movie_form(user_id):
    return render_template('add_movie.html', user_id=user_id)


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


@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['GET'])
def update_movie_form(user_id, movie_id):
    try:
        users = read_data()
        movie_details = users[user_id]['movies'][movie_id]
    except Exception as e:
        return render_template('error.html', message=str(e)), 500
    return render_template('update_movie.html', user_id=user_id, movie_id=movie_id, movie=movie_details)


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


@app.route('/users/<user_id>/delete_movie/<movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    try:
        users = read_data()
        del users[user_id]['movies'][movie_id]
        write_data(users)
    except Exception as e:
        return render_template('error.html', message=str(e)), 500
    return redirect(url_for('list_user_movies', user_id=user_id))


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


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', message=str(e)), 500


if __name__ == '__main__':
    app.run(debug=True)
