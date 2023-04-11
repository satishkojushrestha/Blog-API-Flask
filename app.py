from flask import Flask, request, session, jsonify
from flask_restful import Api, abort, fields, marshal_with
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

#function adding users in database
@app.route('/user/register', methods=['POST'])
def post():          
    data = request.form
    result = User.query.filter_by(username=data['username']).first()
    if result:
        return {"message": "User already exists with that username"}, 409        
    user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        username=data['username'],
        password=generate_password_hash(data['password']), #generate_password_hash is a function to hash passwords, we are storing hashed passowrd instead of storing plain text 
    )
    #adding new user to the database
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

#resource_field is a way to define how an object should be serialized
resource_fields = {
    'post_id': fields.Integer,
    'user_id': fields.Integer,
    'title': fields.String,
    'body': fields.String,
}

@app.route('/admin/post')
@marshal_with(resource_fields)
def get_posts():
    check_login()
    return UserPost.query.all()

@app.route('/admin/post/create', methods=['POST'])
def create_post():
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

@app.route('/admin/post/update/<int:post_id>', methods=['PATCH'])
@marshal_with(resource_fields)
def update_post(post_id):
    check_login()
    post = UserPost.query.filter_by(post_id=post_id).first()
    if not post:
        abort(404, message="Post Not Found")
    data = request.form
    if data['title']:
        post.title = data['title']     
    if data['body']:
        post.body = data['body']

    db.session.commit() 
    return post  

@app.route('/admin/post/delete/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    check_login()
    post = UserPost.query.filter_by(post_id=post_id).first()
    if not post:
        abort(404, message="Post Not Found")
    db.session.delete(post)
    db.session.commit()
    return '', 204

blog_fields = {
    'post_id': fields.Integer,
    'title': fields.String,
    'body': fields.String
}

#without pagination
@app.route('/blog/all',methods=['GET'])
@marshal_with(blog_fields)
def get_blog():
    return UserPost.query.all()

@app.route('/blog/<int:post_id>', methods=['GET'])
@marshal_with(blog_fields)
def get_specific_blog(post_id):
    post = UserPost.query.filter_by(post_id=post_id).first()
    if not post:
        abort(404, message="Blog not found!")
    return post

#with pagination
@app.route('/blog/paginate', defaults={'page_number':None}, methods=['GET'])
@app.route('/blog/paginate/<int:page_number>',methods=['GET'])
def get_blog_paginated(page_number):
    if not page_number:
        paginate = UserPost.query.paginate(per_page=5)
    else:
        paginate = UserPost.query.paginate(per_page=5, page=page_number)

    data = []

    for post_content in paginate.items:
        data.append({
            'post_id': post_content.post_id,
            'title': post_content.title,
            'body': post_content.body
        })
    
    meta = {
        'has_next': paginate.has_next,
        'current_page': paginate.page,
        'posts_per_page': paginate.per_page,
        'has_previous': paginate.has_prev,
        'total_numbers_of_pages': paginate.pages,
        'next_page_number': paginate.next_num,
        'previous_page_number': paginate.prev_num,
        'total_number_of_items': paginate.total
    }
    
    return jsonify({'data': data, 'meta':meta}), 200


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)