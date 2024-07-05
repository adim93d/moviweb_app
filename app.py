from flask import Flask, render_template, request, redirect, url_for
from datamanager.json_data_manager import JSONDataManager
import requests
import json

app = Flask(__name__)
data_manager = JSONDataManager('data/movie_data.json')
USERS = data_manager.get_all_users()
REQUEST_URL = 'https://www.omdbapi.com/?'
API_KEY = 'apikey=3ac01df6'
SEARCH_BY_TITLE = '&t='


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<user_id>')
def list_user_movies(user_id):
    user_movies = data_manager.get_user_movies(user_id)
    username = USERS.get(int(user_id))
    return render_template('user_movies.html', movies=user_movies, username=username, user_id=user_id)


@app.route('/add_user', methods=['GET'])
def add_user_form():
    return render_template('add_user.html')


@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form.get('name')
    users = data_manager.read_file()
    new_user_id = str(max(int(user_id) for user_id in users.keys()) + 1 if users else 1)
    users[new_user_id] = {"name": username, "movies": {}}
    data_manager.write_file(users)
    return redirect(url_for('list_users'))


@app.route('/users/<user_id>/add_movie', methods=['GET'])
def add_movie_form(user_id):
    return render_template('add_movie.html', user_id=user_id)


@app.route('/users/<user_id>/add_movie', methods=['POST'])
def add_movie(user_id):
    movie_title_search = request.form.get('movie_name')
    search_result = requests.get(REQUEST_URL + API_KEY + SEARCH_BY_TITLE + movie_title_search).json()

    if search_result.get('Response') == 'True':
        movie_id = str(len(data_manager.get_user_movies(user_id)) + 1)
        movie_details = {
            "movie_name": search_result['Title'],
            "producer": search_result['Director'],
            "year": search_result['Year'],
            "rating": search_result['imdbRating'],
            "img_url": search_result['Poster']}

        users = data_manager.read_file()
        users[user_id]['movies'][movie_id] = movie_details
        data_manager.write_file(users)
        message = 'Movie added successfully!'
    else:
        message = 'Movie not found!'

    return redirect(url_for('list_user_movies', user_id=user_id, message=message))


@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['GET'])
def update_movie_form(user_id, movie_id):
    users = data_manager.read_file()
    movie_details = users[user_id]['movies'][movie_id]
    return render_template('update_movie.html', user_id=user_id, movie_id=movie_id, movie=movie_details)


@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['POST'])
def update_movie(user_id, movie_id):
    users = data_manager.read_file()
    movie_details = users[user_id]['movies'][movie_id]

    movie_details['movie_name'] = request.form.get('movie_name')
    movie_details['producer'] = request.form.get('producer')
    movie_details['year'] = request.form.get('year')
    movie_details['rating'] = request.form.get('rating')
    movie_details['img_url'] = request.form.get('img_url')

    data_manager.write_file(users)
    return redirect(url_for('list_user_movies', user_id=user_id))


@app.route('/users/<user_id>/delete_movie/<movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    users = data_manager.read_file()
    del users[user_id]['movies'][movie_id]
    data_manager.write_file(users)
    return redirect(url_for('list_user_movies', user_id=user_id))


if __name__ == '__main__':
    app.run(debug=True)
