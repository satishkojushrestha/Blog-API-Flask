from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
db_config = 'sqlite:///blog.sqlite3' #database type and database name