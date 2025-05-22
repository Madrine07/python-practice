# storing all functions used for performing the different authentication process of log in and log out.
from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_401_UNAUTHORIZED,HTTP_200_OK

from app.models.user import User
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity,create_refresh_token

#authors blueprint
users = Blueprint('users', __name__, url_prefix ='/api/v1/users')

# Retrieving all authors from the database

@users.get('/')
@jwt_required()
def getAllUsers():
    try:
       all_users =User.query.all()
       users_data = []

       for user in all_users:
            user_info = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role,
                'password': user.password,
                'created_at': user.created_at,
                'products': []
            }
             
            if hasattr(user, 'products'):
                user_info['products'] = [{
                    'id': product.id,
                    'name': product.name,
                    'description': product.description,
                    'image': product.image,
                    'created_at': product.created_at
                } for product in user.products]

            users_data.append(user_info)
            return jsonify({
            "message": "All users retrieved successfully",
            "total_users": len(users_data),
            "users": users_data
        }), HTTP_200_OK
        



    except Exception as e:
       return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR