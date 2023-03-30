from flask import Flask
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.sqlite3'


class Blog(Resource):
    
    def get(self):
        return "Hello"

api.add_resource(Blog,'/') 

if __name__ == "__main__":
    app.run(debug=True)