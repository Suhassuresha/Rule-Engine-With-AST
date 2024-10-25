from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rule_string = db.Column(db.String(500), nullable=False)
    ast_json = db.Column(db.JSON)

def create_db():
    """Create the database schema."""
    with app.app_context():
        db.create_all()
        print("Database created!")

if __name__ == "__main__":
    create_db()
