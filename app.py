from flask import Flask, request, session, jsonify
from flask_restful import Api, Resource, abort, fields, marshal_with
from database import db, db_config
from model import User, UserPost
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = db_config
db.init_app(app)
app.config['SECRET_KEY'] = 'flask-apitest-secretekey'
 
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=10)

class RegisterUser(Resource):

    def post(self):          
        data = request.form
        result = User.query.filter_by(username=data['username']).first()
        if result:
            abort(409, message="User with that username already exists.")        
        user = User(
            first_name=data['first-name'],
            last_name=data['last-name'],
            username=data['username'],
            password=generate_password_hash(data['password']),
        )
        db.session.add(user)
        db.session.commit()
        return {"message": "User created successfully!"},200
    

@app.route('/login',methods=['POST'])
def login():
    userdata = request.form 
    username = userdata['username']
    password = userdata['password']
    if username and password:
        result = User.query.filter_by(username=username).first()
        if not result:
            abort(404, message="Bad Request - Invalid Credentials")

        if check_password_hash(result.password, password):
                session['username'] = username
                return jsonify({'message' : 'You are successfully loggedin'})
        else:
            resp = jsonify({'message' : 'Bad Request - invalid password'})
            resp.status_code = 400
            return resp

@app.route('/checklogin')        
def check_login():
    if 'username' in session:
        return {"Status":"Authorized"}
    else:
        abort(401, message="Unauthorized")
    
@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
    return jsonify({'message' : 'You successfully logged out'})


resource_fields = {
    'post_id': fields.Integer,
    'user_id': fields.Integer,
    'title': fields.String,
    'body': fields.String,
    'time_stamp': fields.DateTime,
}


class Post(Resource):

    @marshal_with(resource_fields)
    def get(self):
        check_login()
        return User.query.all()

    def post(self):
        check_login()
        username = session['username']
        user = User.query.filter_by(username=username).first()
        data = request.form        
        post = UserPost(     
            user_id = user.user_id,
            title = data['title'],       
            body = data['body'],         
        )
        db.session.add(post)
        db.session.commit()
        return {"message": "New post created."} 


class Blog(Resource):
    
    def get(self):
        return "Hello"

api.add_resource(Blog,'/') 
api.add_resource(RegisterUser,'/user/register') 
api.add_resource(Post,'/admin/post') 

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)