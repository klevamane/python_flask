from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, ValidationError, pre_load, fields

#  from security import authenticate, identity
# from resources.item import Item, ItemList

app = Flask(__name__)
db = SQLAlchemy(app)
# throws TypeError: Expecting a string- or bytes-formatted key. if secrete key is not set
app.config['SECRET_KEY'] = 'super-secret'
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////Users/onengiyerichard/Documents/pythonprojects/flaskproject/database2.db'
app.config['SQLALCHEMY_DATABASE_URI']='postgres://user:user@localhost/flaskdb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.debug=True

# prevents the {"message": "Internal Server Error"}
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)

# jwt = JWT(app, authenticate, identity) # jwt creates a new endpoint /auth
items = []

### MODELS ###
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first =  db.Column(db.String(80))
    last =  db.Column(db.String(80))

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(80), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship(
        'Author',
        backref = db.backref('quotes', lazy='dynamic')
    )
    posted_at = db.Column(db.DateTime)



##### SCHEMAS #######
class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    first = fields.Str()
    last = fields.Str()
    formatted_name = fields.Method('format_name', dump_only=True)

    def format_name(self, author):
        return '{}, {}'.format(author.last, author.first)

def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')

class QuotesSchema(Schema):
    id = fields.Int(dump_only=True)
    author = fields.Nested(AuthorSchema, validate=must_not_be_blank)
    content = fields.Str(required=True, validate=must_not_be_blank)
    posted_at = fields.DateTime(dump_only=True)

    # Allow client to pass author's full name in the request body
    # e.g {"author": "thefirstname thelastname"} rather than {"first": "thefirstname", "last:" "thelastname"}
    @pre_load
    def process_author(self, data):
        author_name = data.get('author')
        if author_name:
            first, last = author_name.split(' ')
            #dict mapping - rember this is like a json / an object but not exactl
            # list is like an array, but can have different datatypes, etc
            auth_dict = dict(first=first, last=last)
        else:
            auth_dict = {}
        data['author'] = auth_dict
        return data

author_schema = AuthorSchema()
author_schemas = AuthorSchema(many=True)
quote_schema = QuotesSchema()
quotes_schema = QuotesSchema(many=True, only=('id', 'content'))

@app.route('/authors')
def get_authors():
    authors = Author.query.all()
    # Serialize the queryset
    result = author_schema.dump(authors)
    return jsonify({'authors': result})

@app.route('/authors/<int:pk>')
def get_author(pk):
    try:
        author = Author.query.get(pk)
    except IntegrityError:
        return jsonify({ 'message': 'Author could not be found'}), 400
    author_result = author_schema.dump(author)
    quotes_result = quotes_schema.dump(author.quotes.all())
    return jsonify({'author': author_result, 'quotes': quotes_result})

@app.route('/quotes', methods=['GET'])
def get_quotes():
    quotes = Quote.query.all()
    result = quote_schema.dumps(quotes, many=True)
    return jsonify({'quotes': result})



@app.route('/quotes/<int:pk>')
def get_quote(pk):
    try:
        quote = Quote.query.get(pk)
    except IntegrityError:
        return jsonify({'message': 'Quote could not be found.'}), 400
    result = quote_schema.dump(quote)
    return jsonify({'quote': result})



@app.route('/quotes/', methods=['POST'])
def new_quote():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400
    # Validate and deserialize input
    try:
        data = quote_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422
    first, last = data['author']['first'], data['author']['last']
    author = Author.query.filter_by(first=first, last=last).first()
    if author is None:
        # Create a new author
        author = Author(first=first, last=last)
        db.session.add(author)
    # Create new quote
    quote = Quote(
        content=data['content'],
        author=author,
        posted_at=datetime.datetime.utcnow(),
    )
    db.session.add(quote)
    db.session.commit()
    result = quote_schema.dump(Quote.query.get(quote.id))
    return jsonify({
        'message': 'Created new quote.',
        'quote': result,
    })


if __name__ == '__main__':
    # done here due to circular import
    from db import db
    db.init_app(app)
    app.run(port=5000)
