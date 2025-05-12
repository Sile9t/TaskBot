import pytest
from taskbot.dao.database import Database
from taskbot.dao.models import User

class UserTests:
    db = Database()

    def createUser():
        newUser = User(
            
        )