from flask import Blueprint, request, jsonify
from app import db
from models import UserTable
from flask_httpauth import HTTPBasicAuth

auth_bp = Blueprint('auth', __name__)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    user = UserTable.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    if UserTable.query.filter_by(username=username).first() is not None:
        return jsonify({'message': 'User already exists'}), 400

    user = UserTable(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
@auth.login_required
def login():
    return jsonify({'message': 'Logged in successfully'}), 200
