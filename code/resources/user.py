import sqlite3
from flask_restful import Resource, reqparse

class User:
    #we wont use id, because that is reserved keyword in python
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password
    
    @classmethod
    def find_by_username(cls, username)
