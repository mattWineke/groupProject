import json
import os

class Database:
    # Constructor for Database class
    def __init__(self, path="database/data.json"): # Default path - can be changed when initializing
        self.path = path
        self.data = {}
        self._load()

    # Private method to load data from file
    def _load(self):
        if not os.path.exists(self.path):
            self.data = {}
            return
        
        with open(self.path, 'r') as file:
            self.data = json.load(file)

    # Private method to save data to file
    def _save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True) # exist_ok to not raise an error if the directory already exists
        
        with open(self.path, 'w') as file:
            json.dump(self.data, file, indent=4) # indent to make the file more readable

    # Public method to get the high score from the database
    def get_high_score(self):
        return self.data.get("high_score", 0)

    # Public method to set the high score in the database
    def set_high_score(self, score):
        self.data["high_score"] = score
        self._save()