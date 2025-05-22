from flask import Blueprint,request, jsonify
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_404_NOT_FOUND, HTTP_409_CONFLICT,HTTP_403_FORBIDDEN, HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_200_OK,HTTP_401_UNAUTHORIZED
import validators
from app.models.user import User
from app.models.product import Product
from app.extensions import db, bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity,  jwt_required

#Product blueprint
products = Blueprint('products', __name__,url_prefix= '/api/v1/products')


#Creating products
@products.route('/create' , methods=['POST'])
@jwt_required()
def createProduct():

    #Storing request values
    data = request.json
    description = data.get('description')
    id = get_jwt_identity()
    product_name = data.get('product_name')
    


#Validations of the incoming request.
    if not product_name or not id or not description:
        return({"error":"All fields are required"}),HTTP_400_BAD_REQUEST
    
    if Product.query.filter_by(product_name=product_name).first() is not None:
        return({"error":"Product name already in use"}),HTTP_409_CONFLICT
    
    try:

        #Creating a new product
        new_product = Product(
            product_name=product_name, description=description, id= id
        )
        db.session.add(new_product)
        db.session.commit()

        return({
            'message': product_name + " has been created succesfully created",
            'order':{
                "id":new_product.id,
                "product_name":new_product.product_name,
                "description":new_product.description
            
            }
        }),HTTP_201_CREATED


    except Exception as e:
        db.session.rollback()
        return jsonify ({"error":str(e)}),HTTP_500_INTERNAL_SERVER_ERROR
    
# Getting all products
@products.get('/all')
@jwt_required()
def getAllProducts():

    try:
        all_products = Product.query.all()

        products_data = []
        for product in all_products :
            product_info = {
                'id': product.id,
                'product_name': product.product_name,
                'image': product.image,
                'description': product.description,
                'user':{
                    'name': product.user.name,
                    'email':product.user.email,
                    'role': product.user.role,
                    'created_at':product.user.created_at,
                },
                'created_at':product.created_at

                
            }
            products_data.append(product_info)

        return jsonify({
            'message': "All products retrieved successfully",
            'total_products': len(products_data),
            "products": products_data
        }), HTTP_200_OK

    except Exception as e:
        return jsonify({
            'error':str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR
    
# Getting product by id

@products.get('/product/<int:id>')
@jwt_required()
def getProduct(id):
    try:
        product = Product.query.filter_by(id=id).first()

        if not product:
            return jsonify({
                "error": "Product is not found"
            }), HTTP_404_NOT_FOUND

        return jsonify({
            'message': "product details retrieved successfully",
            "product": {
                'id': product.id,
                'name': product.product_name,
                'description': product.description,
                'user': {
                    'name': product.user.name,
                    'email':product.user.email,
                    'role': product.user.role,
                    'created_at':product.user.created_at,
                },
                'created_at': product.created_at
            }
        }), HTTP_200_OK

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR

#Updates product details

@products.route('/edit/<int:id>', methods =['PUT','PATCH'])
@jwt_required()
def updateProductDetails(id):

    try:
        current_user = get_jwt_identity()
        loggedInUser = User.query.filter_by(id=current_user).first()

#get product by id
        product = Product.query.filter_by(id=id).first()

        if not product:
            return jsonify({
                "error": "product is not found"
            }),HTTP_404_NOT_FOUND
        
        elif loggedInUser.role != 'Admin' and product.id != current_user:
            return jsonify({
                "error":"You are not authorized to update the product details"
            }), HTTP_403_FORBIDDEN
        
        else:
            product_name = request.get_json().get('product_name',product_name.name)
            description = request.get_json().get('description',product.description)
            


            if product_name != product_name.name and Product.query.filter(Product.product_name).first():
               return jsonify({
                "error": "Product already in exists"
                }), HTTP_409_CONFLICT


            product_name.name = product_name
            product.description = description
            

            db.session.commit()
            
            return jsonify({
                'message': product_name + "'s details have been sucessfully updated ",
            "product": {
                'id': product.id,
                'product_name': product.product_name,
                'description': product.description,
                'user': {
                    'name': product.user.name,
                    'email':product.user.email,
                    'role': product.user.role,
                    'created_at':product.user.created_at,
                },
                'created_at': product.created_at
            }
        }), HTTP_200_OK

    except Exception as e:
        return jsonify({
            'error':str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR


#Deletes a product
@products.route('/delete/<int:id>', methods =['DELETE'])
@jwt_required()
def deleteProduct(id):

    try:
        current_user = get_jwt_identity()
        loggedInUser = User.query.filter_by(id=current_user).first()

#get product by id
        product = Product.query.filter_by(id=id).first()

        if not Product:
            return jsonify({
                "error": "Product not found"
            }),HTTP_404_NOT_FOUND
        
        elif loggedInUser.role != 'Admin' and product.id != current_user:
            return jsonify({
                "error":"You are not authorized to delete this product."
            }),HTTP_403_FORBIDDEN
        else:


            #delete associated books 
            for product in Product.products:
                db.session.delete(product)
            

            db.session.delete(product)
            db.session.commit()


            return jsonify({
                'message': "Product deleted successfully",

            })

    except Exception as e:
        return jsonify({
            'error':str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR