from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from resources.item import Item, ItemList

app = Flask(__name__)
# throws TypeError: Expecting a string- or bytes-formatted key. if secrete key is not set
app.config['SECRET_KEY'] = 'super-secret'

app.debug=True

# prevents the {"message": "Internal Server Error"}
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)

jwt = JWT(app, authenticate, identity) # jwt creates a new endpoint /auth
items = []




api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

if __name__ == '__main__':
    # done here due to circular import
    from db import db
    db.init_app(app)
    app.run(port=5000)
