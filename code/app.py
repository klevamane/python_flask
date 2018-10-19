from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []

# the class inherits from Resource, similar to extends **
class Item(Resource):
    def get(self, name):
        for item in items:
            if(item['name'] == name):
                return item
        
        return {'item': None }, 404 # we understand the synthax now, its a python thing to add a status code

    def post(self, name):
         # this will give an error for content type header
        data = request.get_json() # this function can take force=True or silent=True, check them out, they are both optional
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
app.run(port=5000)
