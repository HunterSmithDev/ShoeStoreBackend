from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)

class ProductModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(200), nullable=False)

    def __repr__ (self):
        return f'<Product {self.id} - {self.name}, Description - {self.description}, Price - {self.price}, Category - {self.category}>'

product_args = reqparse.RequestParser()
product_args.add_argument('name', type=str, required=True, help='Name cannot be empty')
product_args.add_argument('description', type=str, required=True, help='Description cannot be empty')
product_args.add_argument('price', type=float, required=True, help='Price cannot be empty')
product_args.add_argument('image', type=str, required=True, help='Image cannot be empty')
product_args.add_argument('category', type=str, required=True, help='category cannot be empty')

product_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'description': fields.String,
        'price': fields.Float,
        'image': fields.String,
        'category': fields.String
    }

class Products(Resource):
    @marshal_with(product_fields)
    def get(self):
        return ProductModel.query.all()
    
    @marshal_with(product_fields)
    def post(self):
        args = product_args.parse_args()
        product = ProductModel(name=args['name'], description=args['description'], price=args['price'], image=args['image'], category=args['category'])
        db.session.add(product)
        db.session.commit()
        return product, 201
    
class Product(Resource):
    @marshal_with(product_fields)
    def get(self, product_id):
        product = ProductModel.query.get_or_404(product_id)
        return product
    
    def delete(self, product_id):
        product = ProductModel.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return '', 204

api.add_resource(Products, '/products')
api.add_resource(Product, '/products/<int:product_id>')
@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)