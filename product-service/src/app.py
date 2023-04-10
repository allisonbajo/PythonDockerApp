from flask import Flask, jsonify, request
import logging.config
from sqlalchemy import exc
import configparser
from db import db
from Product import Product


# Configure the logging package from the logging ini file
logging.config.fileConfig("/config/logging.ini", disable_existing_loggers=False)

# Get a logger for our module
log = logging.getLogger(__name__)

#products = [
#    {'id': 1, 'name': 'Product 1'},
#    {'id': 2, 'name': 'Product 2'}
#]


def get_database_url():
    # Load our database configuration
    config = configparser.ConfigParser()
    config.read('/config/db.ini')
    database_configuration = config['mysql']
    host = database_configuration['host']
    username = database_configuration['username']
    db_password = open('/run/secrets/db_password')
    password = db_password.read()
    database = database_configuration['database']
    database_url = f'mysql://{username}:{password}@{host}/{database}'
    
    # WARNING: this log will expose the username/password for the database
    log.info(f'Connecting to database: {database_url}')

    return database_url


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_database_url()  #'mysql://root:password@db/products'
db.init_app(app)



@app.route('/products')
def get_products():
    """
    get_products

    command
        curl -v http://localhost:5000/products
    """
    log.debug('GET /products')
    log.debug('Hello')

    #return jsonify(products)

    try:
        products = [product.json for product in Product.find_all()]
        return jsonify(products)

    except exc.SQLAlchemyError:
        message = 'An exception occurred while retrieving all products'
        log.exception(message)
        return message, 500


@app.route('/product/<int:id>')
def get_product(id):
    """
    get_product

    command
        curl -v http://localhost:5000/product/1
    """
    log.debug(f'GET /product/{id}')


    #product_list = [product for product in products if product['id'] == id]
    #if len(product_list) == 0:
    #    return f'Product with id {id} not found', 404
    #return jsonify(product_list[0])

    try:
        product = Product.find_by_id(id)
    
        if product:
            return jsonify(product.json)

        log.warning(f'GET /product/{id}: Product not found')
        return f'Product with id {id} not found', 404

    except exc.SQLAlchemyError:
        message = f'An exception occurred while retrieving product {id}'
        log.exception(message)
        return message, 500


@app.route('/product', methods=['POST'])
def post_product():
    """
    post_product

    command
        curl --header "Content-Type: application/json" --request POST --data '{"name": "Product 3"}' -v http://localhost:5000/product
    """
    # Retrieve the product from the request body
    request_product = request.json
    log.debug(f'POST /product with product: {request_product}')

    # Generate an Id for the post
    #new_id = max([product['id'] for product in products]) + 1
    
    # Create a new product
    #new_product = {
    #    'id': new_id,
    #    'name': request_product['name']
    #}
    product = Product(None, request_product['name'])

    # Append the new product to our product list
    #products.append(new_product)

    try:
        # Save the Product to the database
        product.save_to_db()

        # return the new product back to the client
        return jsonify(product.json), 201

    except exc.SQLAlchemyError:
        message = f'An exception occurred while creating product with name: {product.name}'
        log.exception(message)
        return message, 500


@app.route('/product/<int:id>', methods=['PUT'])
def put_product(id):
    """
    put_product

    command
        curl --header "Content-Type: application/json" --request PUT --data '{"name": "Update Product 2"}' -v http://localhost:5000/product/2
    """
    log.debug(f'PUT /product/{id}')

    try:
        existing_product = Product.find_by_id(id)

        if existing_product:
            # Get the request payload
            updated_product = request.json
        
            # Find the product with the specified ID
            #for product in products:
            #    if product['id'] == id:
            #        # Update the product name
            #        product['name'] = updated_product['name']
            #        return jsonify(product), 200

            existing_product.name = updated_product['name']
            existing_product.save_to_db()

            return jsonify(existing_product.json), 200

        log.warning(f'PUT /product/{id}: Existing product not found')
        return f'Product with id {id} not found', 404

    except exc.SQLAlchemyError:
        message = f'An exception occurred while updating product with name: {updated_product.name}'
        loc.exception(message)
        return message, 500


@app.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    """
    delete_product

    command
        curl --request DELETE -v http://localhost:5000/product/2
    """
    log.debug(f'DELETE /product/{id}')

    try:
        # Find the product with the specified ID
        #product_list = [product for product in products if product['id'] == id]
        existing_product = Product.find_by_id(id)

        if existing_product:
            #if len(product_list) == 1:
            #    products.remove(product_list[0])
            #    return f'Product with id {id} deleted', 200
            existing_product.delete_from_db()
            return f'Product with id {id} deleted', 200

        log.warning(f'DELETE /product/{id}: Existing product not found')
        return f'Product with id {id} not found', 404

    except exc.SQLAlchemyError:
        message = f'An exception occurred while deleting the product with id: {id}'
        log.exception(message)
        return message, 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    #app.run(debug=True, host='10.0.0.25')
