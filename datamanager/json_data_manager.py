import json
from moviweb_app.datamanager.data_manager_interface import DataManagerInterface


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def read_file(self):
        with open(self.filename, 'r+') as handle:
            data = json.load(handle)
        return data

    """def get_all_users(self):
        # Return all the users all users
        data = self.read_file()
        users_dict = {}
        for user_id, username in data.items():
            users_dict[int(user_id)] = username['name']
        return users_dict"""

    def get_all_users(self):
        # Return all the users all users
        data = self.read_file()
        users_list = []
        for user_id, username in data.items():
            users_list.append(username['name'])
        return users_list

    def get_user_movies(self, user_id):
        # Return all the movies for a given user
        data = self.read_file()
        return data[str(user_id)]['movies']
