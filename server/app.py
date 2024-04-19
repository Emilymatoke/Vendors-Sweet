
from models import db, Sweet, Vendor, VendorSweet
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Code challenge</h1>'

# Route to get all vendors
@app.route('/vendors', methods=['GET'])
def get_vendors():
    vendors = Vendor.query.all()
    vendors_data = [{'id': vendor.id, 'name': vendor.name} for vendor in vendors]
    return jsonify(vendors_data)

# Route to get a specific vendor by ID
@app.route('/vendors/<int:id>', methods=['GET'])
def get_vendor(id):
    vendor = Vendor.query.get(id)
    if vendor:
        vendor_data = {
            'id': vendor.id,
            'name': vendor.name,
            'vendor_sweets': [{
                'id': vs.id,
                'price': vs.price,
                'sweet': {'id': vs.sweet.id, 'name': vs.sweet.name},
                'sweet_id': vs.sweet_id,
                'vendor_id': vs.vendor_id
            } for vs in vendor.vendor_sweets]
        }
        return jsonify(vendor_data)
    else:
        return jsonify({'error': 'Vendor not found'}), 404

# Route to get all sweets
@app.route('/sweets', methods=['GET'])
def get_sweets():
    sweets = Sweet.query.all()
    sweets_data = [{'id': sweet.id, 'name': sweet.name} for sweet in sweets]
    return jsonify(sweets_data)

# Route to get a specific sweet by ID
@app.route('/sweets/<int:id>', methods=['GET'])
def get_sweet(id):
    sweet = Sweet.query.get(id)
    if sweet:
        sweet_data = {'id': sweet.id, 'name': sweet.name}
        return jsonify(sweet_data)
    else:
        return jsonify({'error': 'Sweet not found'}), 404

# Route to create a new VendorSweet
# Route to create a new VendorSweet
# Route to create a new VendorSweet
@app.route('/vendor_sweets', methods=['POST'])
def create_vendor_sweet():
    data = request.json
    price = data.get('price')
    vendor_id = data.get('vendor_id')
    sweet_id = data.get('sweet_id')

    # Validate input
    if price is None or vendor_id is None or sweet_id is None:
        return jsonify({'errors': ['price, vendor_id, and sweet_id are required']}), 400

    try:
        # Check if price is negative
        if price < 0:
            raise ValueError("Price cannot be negative.")

        # Check if vendor and sweet exist
        vendor = Vendor.query.get(vendor_id)
        sweet = Sweet.query.get(sweet_id)
        if not vendor or not sweet:
            return jsonify({'errors': ['Vendor or Sweet not found']}), 404

        # Create VendorSweet
        vendor_sweet = VendorSweet(price=price, vendor=vendor, sweet=sweet)
        db.session.add(vendor_sweet)
        db.session.commit()

        # Prepare response
        response_data = {
            'id': vendor_sweet.id,
            'price': vendor_sweet.price,
            'sweet': {'id': sweet.id, 'name': sweet.name},
            'sweet_id': sweet_id,
            'vendor': {'id': vendor.id, 'name': vendor.name},
            'vendor_id': vendor_id
        }
        return jsonify(response_data), 201

    except ValueError as e:
        return jsonify({'errors': ['validation errors']}), 400

# Route to delete a VendorSweet by ID
# Route to delete a VendorSweet by ID
@app.route('/vendor_sweets/<int:id>', methods=['DELETE'])
def delete_vendor_sweet(id):
    vendor_sweet = VendorSweet.query.get(id)
    if vendor_sweet:
        db.session.delete(vendor_sweet)
        db.session.commit()
        return '', 204  # Return an empty response with a 204 status code
    else:
        return jsonify({'error': 'VendorSweet not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)


