Users = []

Meetups = []

Questions = []

class BaseModels:
    """"This performs all basic actions performed on all data sets"""
    def __init__(self, data_model, view_data):
        self.db = data_model
        self.data = view_data

    def autogen_id(self):
        if len(self.db) == 0:
            self.data["id"] = 1
        else:
            new_id = self.db[-1]["id"] + 1
            self.data["id"] = new_id

        return self.data

    def save_the_data(self):
        self.db.append(self.data)
        return self.db[-1]

    def delete_the_data(self):
        self.db.remove(self.data)
        return self.db

    def chec_exists(self, field_to_check, the_value):
        exists = 0
        available = [value for value in self.db if value[field_to_check] == the_value]

        if len(available) > 0:
            exists = 1

        return exists
