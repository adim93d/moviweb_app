from flask import Flask, render_template, request, redirect, url_for
from datamanager.json_data_manager import JSONDataManager

app = Flask(__name__)
data_manager = JSONDataManager('data/movie_data.json')
USERS = data_manager.get_all_users()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/users')
def list_users():
    return render_template('users.html', users=USERS)


@app.route('/users/<user_id>')
def list_user_movies(user_id):
    user_movies = data_manager.get_user_movies(user_id)
    username = USERS.get(int(user_id))
    return render_template('user_movies.html', movies=user_movies, username=username)


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
"""Error: 405, method not allowed.. problem when adding a new user, user is not added into the JSON"""


@app.route('/users/<user_id>/add_movie')
def add_movie():
    pass


@app.route('/users/<user_id>/update_movie/<movie_id>')
def update_movie():
    pass


@app.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_movie():
    pass


if __name__ == '__main__':
    app.run(debug=True)
