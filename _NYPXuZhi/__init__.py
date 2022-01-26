from flask import Flask, render_template, request, redirect, url_for
from Forms import CreateUserForm, CreateCustomerForm
import shelve, User, Customer

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html')


@app.route('/contactUs')
def contact_us():
    return render_template('contactUs.html')


@app.route('/createUser', methods=['GET', 'POST'])
def create_user():
    create_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'c')

        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from user.db.")

        user = User.User(create_user_form.first_name.data, create_user_form.last_name.data, create_user_form.gender.data, create_user_form.membership.data, create_user_form.remarks.data)
        users_dict[user.get_user_id()] = user
        db['Users'] = users_dict

        # Test codes
        users_dict = db['Users']
        user = users_dict[user.get_user_id()]
        print(user.get_first_name(), user.get_last_name(), "was stored in user.db successfully with user_id ==", user.get_user_id())

        db.close()

        return redirect(url_for('home'))
    return render_template('createUser.html', form=create_user_form)


@app.route('/createCustomer', methods=['GET', 'POST'])
def create_customer():
    create_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and create_customer_form.validate():
        customers_dict = {}
        db = shelve.open('customer.db', 'c')

        try:
            customers_dict = db['Customers']
        except:
            print("Error in retrieving Customers from customer.db.")

        customer = Customer.Customer(create_customer_form.first_name.data, create_customer_form.last_name.data,
                                     create_customer_form.gender.data, create_customer_form.membership.data,
                                     create_customer_form.remarks.data, create_customer_form.email.data,
                                     create_customer_form.date_joined.data,
                                     create_customer_form.address.data, )
        customers_dict[customer.get_customer_id()] = customer
        db['Customers'] = customers_dict

        db.close()

        return redirect(url_for('home'))
    return render_template('createCustomer.html', form=create_customer_form)


@app.route('/retrieveUsers')
def retrieve_users():
    users_dict = {}
    db = shelve.open('user.db', 'r')
    users_dict = db['Users']
    db.close()
    users_list = []


    for key in users_dict:

        user = users_dict.get(key)
        users_list.append(user)
        print(key)
    return render_template('retrieveUsers.html', count=len(users_list), users_list=users_list)


@app.route('/retrieveCustomer')
def retrieve_customers():
    customers_dict = {}
    db = shelve.open('customer.db', 'r')
    customers_dict = db['Customers']
    db.close()

    customers_list = []
    for key in customers_dict:
        customer = customers_dict.get(key)
        customers_list.append(customer)
        print(key)


    return render_template('retrieveCustomer.html', count=len(customers_list), customers_list=customers_list)


@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
def update_user(id):
    update_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'w')
        users_dict = db['Users']

        user = users_dict.get(id)
        user.set_first_name(update_user_form.first_name.data)
        user.set_last_name(update_user_form.last_name.data)
        user.set_gender(update_user_form.gender.data)
        user.set_membership(update_user_form.membership.data)
        user.set_remarks(update_user_form.remarks.data)

        db['Users'] = users_dict
        db.close()

        return redirect(url_for('retrieve_users'))
    else:
        users_dict = {}
        db = shelve.open('user.db', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(id)
        update_user_form.first_name.data = user.get_first_name()
        update_user_form.last_name.data = user.get_last_name()
        update_user_form.gender.data = user.get_gender()
        update_user_form.membership.data = user.get_membership()
        update_user_form.remarks.data = user.get_remarks()

        return render_template('updateUser.html', form=update_user_form)
@app.route('/updateCustomer/<int:id>/', methods=['GET', 'POST'])
def update_customer(id):
    update_customer_form = CreateUserForm(request.form)
    if request.method == 'POST' and update_customer_form.validate():
        users_dict = {}
        db = shelve.open('customer.db', 'w')

        customer_dict = db['Customers']

        customer = customer_dict.get(id)
        customer.set_first_name(update_customer_form.first_name.data)
        customer.set_last_name(update_customer_form.last_name.data)
        customer.set_gender(update_customer_form.gender.data)
        customer.set_membership(update_customer_form.membership.data)
        customer.set_remarks(update_customer_form.remarks.data)

        db['Customers'] = users_dict
        db.close()

        return redirect(url_for('retrieve_customers'))
    else:
        users_dict = {}
        oc = shelve.open('user.db', 'w')
        db = shelve.open('customer.db', 'r')
        customer_dict = db['Customers']

        users_dict = oc['Users']
        customer = customer_dict.get(id)
        user=users_dict.get(id)
        db.close()
        oc.close()

        update_customer_form.first_name.data = user.get_first_name()
        update_customer_form.last_name.data = user.get_last_name()
        update_customer_form.gender.data = user.get_gender()
        update_customer_form.membership.data = user.get_membership()
        update_customer_form.remarks.data = user.get_remarks()

        return render_template('updateCustomer.html', form=update_customer_form)



@app.route('/deleteUser/<int:id>', methods=['POST'])
def delete_user(id):
    users_dict = {}
    db = shelve.open('user.db', 'w')
    users_dict = db['Users']

    users_dict.pop(id)

    db['Users'] = users_dict
    db.close()

    return redirect(url_for('retrieve_users'))
@app.route('/deleteCustomer/<int:id>', methods=['POST'])
def delete_customer(id):
    users_dict = {}
    db = shelve.open('customer.db', 'w')
    customer_dict = db['Customers']

    customer_dict.pop(id)

    db['Customers'] = customer_dict
    db.close()

    return redirect(url_for('retrieve_customers'))


if __name__ == '__main__':
    app.run()
