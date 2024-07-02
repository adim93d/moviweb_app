import json
from data_manager_interface import DataManagerInterface


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def read_file(self):
        with open(self.filename, 'r+') as handle:
            data = json.load(handle)
        return data

    def get_all_users(self):
        # Return all the users all users
        data = self.read_file()
        users_dict = {}
        for user_id, username in data.items():
            users_dict[int(user_id)] = username['name']
        return users_dict

    def get_user_movies(self, user_id):
        # Return all the movies for a given user
        data = self.read_file()
        return data[str(user_id)]['movies']


# JSONDataManager('temp_json_data.json').get_all_users()
print(JSONDataManager('temp_json_data.json').get_user_movies(2))
