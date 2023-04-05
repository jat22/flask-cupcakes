from flask import Flask, jsonify, request
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "SECRET"

def serlialize_cupcake(cupcake):

	return {
        "id" : cupcake.id,
        "flavor" : cupcake.flavor,
		"size" : cupcake.size,
		"rating" : cupcake.rating,
		"image" : cupcake.image
	}

@app.route('/api/cupcakes')
def list_all_cupcakes():
	"""Return JSON {'cupcakes' : [{id, flavor, size, rating, image}, ...]"""
	cupcakes = Cupcake.query.all()
	serialized = [serlialize_cupcake(cc) for cc in cupcakes]

	return jsonify(cupcakes = serialized)

@app.route('/api/cupcakes/<cupcake_id>')
def list_single_cupcake(cupcake_id):
	"""return JSON {'cupake' : {id, flavor, size, rating, image}}"""
	cupcake = Cupcake.query.get(cupcake_id)
	serialized = serlialize_cupcake(cupcake)

	return jsonify(cupcake = serialized)

@app.route('/api/cupcakes', methods = ["POST"])
def create_cupcake():
	"""create new cupcake"""

	flavor = request.json['flavor']
	size = request.json['size']
	rating = request.json['rating']
	image = request.json['image']


	new_cupcake = Cupcake(flavor = flavor, size = size, rating = rating, image = image)

	db.session.add(new_cupcake)
	db.session.commit()

	serialized = serlialize_cupcake(new_cupcake)

	return (jsonify(cupcake=serialized), 201)

@app.route('/api/cupcakes/<cupcake_id>', methods = ["PATCH"])
def udpate_cupcake(cupcake_id):
	"""update cupcake"""
	cupcake = Cupcake.query.get_or_404(cupcake_id)
	cupcake.flavor = request.json['flavor']
	cupcake.size = request.json['size']
	cupcake.rating = request.json['rating']
	cupcake.image = request.json['image']

	db.session.commit()

	serialized = serlialize_cupcake(cupcake)
	return(jsonify(cupcake=serialized))

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
	"""Delete cupcake"""
	cupcake = Cupcake.query.get_or_404(cupcake_id)
	db.session.delete(cupcake)
	db.session.commit()
	return jsonify(message="deleted")