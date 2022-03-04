from email.mime import image
from flask import Flask, jsonify, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ThisIsHidden123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

"""Flask app for Cupcakes"""

connect_db(app)


@app.route('/')
def show_home_page():
    """Home page"""

    all_cupcakes = Cupcake.query.all()
    return render_template('home.html', cupcakes=all_cupcakes)


@app.route('/api/cupcakes', methods=['GET'])
def get_all_cupcakes():
    """Gets list of all cupcakes"""

    cupcakes = Cupcake.query.all()
    serialized = [cupcake.serialize() for cupcake in cupcakes]
    return jsonify(cupcakes=serialized)


@app.route('/api/cupcakes/<int:id>', methods=['GET'])
def get_specific_cupcake(id):
    """Gets details about one cupcake"""

    cupcake = Cupcake.query.get_or_404(id)
    serialized = cupcake.serialize()
    return jsonify(cupcake=serialized)


@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Creates a new cupcake record"""

    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json.get('image')
    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(new_cupcake)
    db.session.commit()
    serialized = new_cupcake.serialize()
    return (jsonify(cupcake=serialized), 201)


@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    """Updates a cupcake record"""

    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json['flavor']
    cupcake.size = request.json['size']
    cupcake.rating = request.json['rating']
    cupcake.image = request.json['image']
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
    """Deletes a cupcake record"""

    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify({'message': 'Deleted'})