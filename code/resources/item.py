# from flask import Flask, request
# from flask_restful import Resource, Api, reqparse
# from flask_jwt import JWT, jwt_required

# from security import authenticate, identity

# # the class inherits from Resource, similar to extends **
# class Item(Resource):
#     # kind of validation to be used in methods that choose to use it
#     parser = reqparse.RequestParser()
#         # because we've only defined price, if we put any other argument in the payload
#         # it wont show, it would just be erased
#     parser.add_argument('price',
#         type=float,
#         required=True,
#         help="This field cannot be left blank!"

#         )

#     @jwt_required()
#     def get(self, name):
        
#         # data = request.get_json() # this function can take force=True or silent=True, check them out, they are both optional
#         # the filter function returns a filter object which methods can be called on
#         # so we can use list, next etc
#         # next will return the first item
#         # we would add a default value when using next, because it will break the code if no item is found 
#         # fitting the criteria
#         # item = list(filter(lambda x: x['name'] == name, items))
#         item = next(filter(lambda x: x['name'] == name, items), None)
#         return {'item': item}, 200 if item is not None else 404
    
#     def post(self, name):
#         # next will return the first item
#         # we would add a default value when using next, because it will break the code if no item is found 
#         if next(filter(lambda x: x['name'] == name, items), None) is not None: # we can omit if not None (because is still satisfies the condition)
#             return {'message': 'An item with name {} already exists'.format(name)}, 400
        
#         # data = request.get_json()
#         data = Item.parser.parse_args()
#         item = {'name': name, 'price': data['price']}
#         items.append(item)
#         return item, 201
    
#     def delete(self, name):
#         #using the global items variable (ie data store)
#         global items
#         # remeber that the filter function returns a filtered object which we can perform thing on
#         # so we convert it to a list here
#         previous_length = len(items)
#         items = list(filter(lambda x: x['name'] != name, items))
#         new_length = len(items)

#         if previous_length == new_length:
#             return {'message': 'No item with name {} found'.format(name)}
#         return {'message': 'Item deleted'}
    
#     def put(self, name):
       
#         # data = request.get_json()
#         data = Item.parser.parse_args()
#         item = next(filter(lambda x: x['name'] == name, items), None)
#         if item is None:
#             item = {'name': name, 'price': data['price']}
#             items.append(item)
#         else:
#             # it means it will be a dictionary which will have the update method
#             item.update(data)
#         return item

# class ItemList(Resource):
#     def get(self):
#         return {'items': items}
