from flask import Flask
from app.views import todo
from app.utils.db import db

app = Flask(__name__)

# Replace the fields with the relevant data
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://daw:daw1234@localhost/todo'
app.config['SQALCHEMY_TRACK_MODIFICATION'] = False

app.register_blueprint(todo)

db.init_app(app)
with app.app_context():
    db.create_all()