from werkzeug.security import safe_str_cmp
from user import User

users = [
    User(1, 'brian', 'asdf')
]
# set comprehension
# here we are assigning key-value pairs
# assign each user in the users data (in-memory) to its password
username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}

def authenticate(username, password):
    user = username_mapping.get(username, None)
    # if user is not None
    # use safe_str_cmp so the comparison is compatible even in python 2
    # else just compare - if user.password == password
    if user is not None and safe_str_cmp(user.password, password):
    # if user and user.password == password:
        return user

# this function is unique to FLASK-JWT extension
# the payload is the content of the jwt token
# that information will be extracted from the payload
def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
