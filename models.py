"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMG = "https://tinyurl.com/demo-cupcake"

class Cupcake(db.Model):
    __tablename__ = "cupcakes" 

    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, nullable=False, default = DEFAULT_IMG)

    def to_dict(self): 
        return {
            "id": self.id,
            "flavor": self.flavor,
            "rating": self.rating,
            "size": self.size,
            "image": self.image,
        }
   
def connect_db(app): 
    db.app = app
    db.init_app(app)


    