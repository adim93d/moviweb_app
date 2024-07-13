
# MovieWeb App

MovieWeb App is a web application that allows users to manage their movie collections. Users can add new movies, update existing ones, and delete them. The application fetches movie details from the OMDB API.

## Technologies Used

- **Flask**: A micro web framework for Python to handle routing and templates.
- **JSON**: For storing user and movie data.
- **OMDB API**: To fetch movie details using movie titles.
- **HTML/CSS**: For the front-end design of the application.

## Requirements

To run the MovieWeb App, you need to have the following installed:

- Python 3.x
- Flask
- Requests

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/movieweb-app.git
   cd movieweb-app
   ```

2. Install the required Python packages:
   ```sh
   pip install flask requests
   ```

3. Run the application:
   ```sh
   python app.py
   ```

4. Open your browser and navigate to `http://127.0.0.1:5000/`.

## Functionality

### Home Page

- **Route**: `/`
- **Template**: `index.html`
- **Description**: Displays a welcome message and a link to the users page.

### List Users

- **Route**: `/users`
- **Template**: `users.html`
- **Description**: Lists all users with their names and options to view or delete them.

### List User Movies

- **Route**: `/users/<user_id>`
- **Template**: `user_movies.html`
- **Description**: Lists all movies for a specific user with options to update or delete each movie.

### Add User

- **Route**: `/add_user`
- **Template**: `add_user.html`
- **Description**: Provides a form to add a new user.

### Add Movie

- **Route**: `/users/<user_id>/add_movie`
- **Template**: `add_movie.html`
- **Description**: Provides a form to add a new movie for a specific user.

### Update Movie

- **Route**: `/users/<user_id>/update_movie/<movie_id>`
- **Template**: `update_movie.html`
- **Description**: Provides a form to update an existing movie for a specific user.

### Delete Movie

- **Route**: `/users/<user_id>/delete_movie/<movie_id>`
- **Description**: Handles the deletion of a movie for a specific user.

### Delete User

- **Route**: `/users/<user_id>/delete`
- **Description**: Handles the deletion of a user.

## Error Handling

### 404 - Page Not Found

- **Template**: `404.html`
- **Description**: Custom error page for non-existent routes.

### 500 - Internal Server Error

- **Template**: `500.html`
- **Description**: Custom error page for server errors.

## Data Management

The application uses a JSON file (`data/movie_data.json`) to store user and movie data. The `JSONDataManager` class handles reading and writing data to this file.

## Links

- [Home Page](#home-page)
- [List Users](#list-users)
- [List User Movies](#list-user-movies)
- [Add User](#add-user)
- [Add Movie](#add-movie)
- [Update Movie](#update-movie)
- [Delete Movie](#delete-movie)
- [Delete User](#delete-user)
- [Error Handling](#error-handling)
  - [404 - Page Not Found](#404---page-not-found)
  - [500 - Internal Server Error](#500---internal-server-error)
- [Data Management](#data-management)
