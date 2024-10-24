"""Flask app for Cupcakes"""
from flask import Flask, request, redirect, render_template, current_app, jsonify, flash, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_ECHO'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

toolbar = DebugToolbarExtension(app)

connect_db(app)
with app.app_context():
    db.create_all()

toolbar = DebugToolbarExtension(app)



@app.route('/')
def root():
       return render_template("home.html")


@app.route('/api/cupcakes', methods = ["GET"])
def cupcakes_data():
        # Get data about all cupcakes. Respond with JSON
        #  like: {cupcakes: [{id, flavor, size, rating, image}, ...]}. 
        # The values should come from each cupcake instance.
        cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.order_by(Cupcake.flavor.desc()).all()]
        return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes', methods = ["POST"])
def cupcake_add():
        # Create a cupcake with flavor, size, rating and image data 
        # from the body of the request. Respond with JSON 
        # like: {cupcake: {id, flavor, size, rating, image}}.
        data = request.json
        cupcake = Cupcake(
               flavor = data['flavor'],
               rating = data['rating'],
               size = data['size'],
               image = data['image'] or None)
        db.session.add(cupcake)
        db.session.commit()
        return (jsonify(cupcake=cupcake.to_dict()), 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods = ["GET"])
def cupcake_inspect(cupcake_id):
        #  Get data about a single cupcake. Respond with JSON 
        # like: {cupcake: {id, flavor, size, rating, image}}.
        #  This should raise a 404 if the cupcake cannot be found.
       
        cupcake = Cupcake.query.get_or_404(cupcake_id)

        return jsonify(cupcake=cupcake.to_dict())

@app.route('/api/cupcakes/<int:cupcake_id>', methods = ["PATCH"])
def cupcake_update(cupcake_id):
        #  Update a cupcake with the id passed in the URL and flavor,
        #  size, rating and image data from the body of the request. 
        # You can always assume that the entire cupcake object will be
        #  passed to the backend. This should raise a 404 if the cupcake cannot be found.
        # Respond with JSON of the newly-updated cupcake, 
        # like this: {cupcake: {id, flavor, size, rating,image}}.
        data = request.json
        cupcake = Cupcake.query.get_or_404(cupcake_id)

        cupcake.flavor = data['flavor']
        cupcake.rating = data['rating']
        cupcake.size = data['size']
        cupcake.image = data['image'] or None

        db.session.add(cupcake)
        db.session.commit()

        return jsonify(cupcake=cupcake.to_dict())

@app.route('/api/cupcakes/<int:cupcake_id>', methods = ["DELETE"])
def cupcake_delete(cupcake_id):
        #  This should raise a 404 if the cupcake cannot be found.
        # Delete cupcake with the id passed in the URL. Respond with JSON
        #  like `{message: "Deleted"}`.
        cupcake = Cupcake.query.get_or_404(cupcake_id)
        db.session.delete(cupcake)
        db.session.commit()
        return jsonify(message = 'Cupcake Deleted')