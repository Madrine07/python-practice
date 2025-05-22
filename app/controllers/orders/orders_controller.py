
# storing all functions used for performing the different authentication process of log in and log out.
from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_401_UNAUTHORIZED,HTTP_200_OK
from app.models.product import Product
from app.models.order import Order
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity,create_refresh_token

#products blueprint
orders = Blueprint('orders', __name__, url_prefix ='/api/v1/orders')

# Retrieving all orders from the database

@orders.route('/create', methods=['POST'])
@jwt_required()
def getAllOrders():
    try:
       all_orders = Order.query.all()
       orders_data = []
       data = request.json

       order_name = data.get('order_name')
       description = data.get('description')
       image = data.get('image')

       if not order_name or not description:
        return jsonify({'error': 'Name and description are required'}), HTTP_400_BAD_REQUEST
   
       for order in all_orders:
            order_info = {
                'id': order.id,
                'user_id': order.user_id,
                'description': order.description,
                'image': order.image,
                'created_at': order.created_at,
                'orders': []
            }
             
            if hasattr(order, 'product'):
                 order_info['product']=[{
                     'id': product.id,
                     'name': product.product_name,
                     'description': product.description,
                 } for product in order.products]

            

            orders_data.append(order_info)
            return jsonify({
            "message": "All orders retrieved successfully",
            "total_orders": len(orders_data),
            "orders": orders_data
        }), HTTP_200_OK
        



    except Exception as e:
       return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR