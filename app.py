from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

dishes = [
    {'id': 1, 'name': 'Pasta', 'price': 10.99, 'availability': True},
    {'id': 2, 'name': 'Pizza', 'price': 12.99, 'availability': True},
    {'id': 3, 'name': 'Burger', 'price': 8.99, 'availability': False},
    # Add more dishes if you like
]

orders = []

@app.route('/')
def home():
    return 'Welcome to Zesty Zomato!'

@app.route('/menu')
def menu():
    return render_template('menu.html', dishes=dishes)

@app.route('/add_dish', methods=['GET', 'POST'])
def add_dish():
    if request.method == 'POST':
        # Get the form data submitted by the user
        dish_id = int(request.form['dish_id'])
        dish_name = request.form['dish_name']
        dish_price = float(request.form['dish_price'])
        availability = True if request.form.get('availability') else False

        # Create a new dish dictionary
        new_dish = {'id': dish_id, 'name': dish_name, 'price': dish_price, 'availability': availability}

        # Add the new dish to the dishes list
        dishes.append(new_dish)

        # Redirect to the menu page
        return redirect(url_for('menu'))

    return render_template('add_dish.html')

@app.route('/remove_dish/<int:dish_id>', methods=['POST'])
def remove_dish(dish_id):
    # Find the dish with the given ID and remove it from the dishes list
    for dish in dishes:
        if dish['id'] == dish_id:
            dishes.remove(dish)
            break

    # Redirect to the menu page
    return redirect(url_for('menu'))

@app.route('/update_availability/<int:dish_id>/<availability>', methods=['POST'])
def update_availability(dish_id, availability):
    # Find the dish with the given ID and update its availability
    for dish in dishes:
        if dish['id'] == dish_id:
            dish['availability'] = True if availability == 'available' else False
            break

    # Redirect to the menu page
    return redirect(url_for('menu'))

@app.route('/take_order', methods=['GET', 'POST'])
def take_order():
    if request.method == 'POST':
        # Get the form data submitted by the user
        customer_name = request.form['customer_name']
        dish_ids = request.form.getlist('dish_ids')

        # Check if all the selected dishes are available
        available_dish_ids = [dish['id'] for dish in dishes if dish['availability']]
        invalid_dish_ids = [dish_id for dish_id in dish_ids if dish_id not in available_dish_ids]

        if invalid_dish_ids:
            error_message = f"Invalid dish IDs: {', '.join(invalid_dish_ids)}"
            return render_template('take_order.html', dishes=dishes, error_message=error_message)

        # Generate a unique order ID
        order_id = len(orders) + 1

        # Create a new order dictionary
        new_order = {'order_id': order_id, 'customer_name': customer_name, 'dish_ids': dish_ids, 'status': 'received'}

        # Add the new order to the orders list
        orders.append(new_order)

        # Redirect to the orders page
        return redirect(url_for('orders'))

    return render_template('take_order.html', dishes=dishes)



@app.route('/new_order', methods=['GET', 'POST'])
def new_order():
    if request.method == 'POST':
        # Get the form data submitted by the user
        customer_name = request.form['customer_name']
        dish_ids = request.form.getlist('dish_ids')

        # Validate the dish IDs
        invalid_dish_ids = []
        valid_dishes = []
        for dish_id in dish_ids:
            dish = next((d for d in dishes if d['id'] == int(dish_id)), None)
            if dish is None or not dish['availability']:
                invalid_dish_ids.append(dish_id)
            else:
                valid_dishes.append(dish)

        if invalid_dish_ids:
            error_message = f"The following dish IDs are invalid or unavailable: {', '.join(invalid_dish_ids)}"
            return render_template('new_order.html', error_message=error_message)

        # Generate a unique order ID
        order_id = len(orders) + 1

        # Create a new order dictionary
        new_order = {'order_id': order_id, 'customer_name': customer_name, 'status': 'received', 'dishes': valid_dishes}

        # Add the new order to the orders list
        orders.append(new_order)

        # Redirect to the menu page
        return redirect(url_for('menu'))

    return render_template('new_order.html')

@app.route('/view_order/<int:order_id>')
def view_order(order_id):
    # Find the order with the given ID
    order = next((o for o in orders if o['order_id'] == order_id), None)

    # Render the order details template
    return render_template('view_order.html', order=order)

@app.route('/update_status/<int:order_id>/<status>', methods=['POST'])
def update_status(order_id, status):
    # Find the order with the given ID and update its status
    for order in orders:
        if order['order_id'] == order_id:
            order['status'] = status
            break

    # Redirect to the menu page
    return redirect(url_for('menu'))


@app.route('/orders')
def all_orders():
    return render_template('all_orders.html', orders=orders)


if __name__ == '__main__':
    app.run(debug=True)

