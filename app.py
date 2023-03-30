from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort
from database import db, db_config
from model import User, Post

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = db_config
db.init_app(app)


class RegisterUser(Resource):

    def post(self):          
        arguments = request.form
        result = User.query.filter_by(username=arguments['username']).first()
        if result:
            abort(409, message="User with that username already exists.")        
        user = User(
            first_name=arguments['first-name'],
            last_name=arguments['last-name'],
            username=arguments['username'],
            password=arguments['password'],
        )
        db.session.add(user)
        db.session.commit()
        return {"message": "User created successfully!"},200


class Blog(Resource):
    
    def get(self):
        return "Hello"

api.add_resource(Blog,'/') 
api.add_resource(RegisterUser,'/user/register') 

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)