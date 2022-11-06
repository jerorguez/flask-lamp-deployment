from app.utils.db import db

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    status = db.Column(db.Boolean, default=False)

    def __init__(self, name):
        self.name = name