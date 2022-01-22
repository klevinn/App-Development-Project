from flask_sqlalchemy import SQLAlchemy

# by joshua (products database)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
j_db = SQLAlchemy(app)

# models by joshua (products class, will seperate later)
class Product(j_db.Model):
    __searchable__ = ['name', 'short_description', 'long_description', 'category']

    id = j_db.Column(j_db.Integer, primary_key=True)
    img_file_name = j_db.Column(j_db.String) #nullable=False
    name = j_db.Column(j_db.String(40)) # nullable=False
    price = j_db.Column(j_db.Float) # nullable=False
    category = j_db.Column(j_db.String(50))
    short_description = j_db.Column(j_db.String(100))
    long_description = j_db.Column(j_db.String)
    stock = j_db.Column(j_db.Integer)

# by joshua end

# joshua's work (store, all guest for now, i plan to make products crud for admin, figuring out images related stuff)

# app routes for store (for both user and logged in)
@app.route('/store', methods=["GET","POST"])
def store():
    products = Product.query.all()

    return render_template('user/guest/store/store.html', products=products)

@app.route('/search', methods=["GET","POST"])
def search():
    query = request.args.get('query')

    if query:
        products = Product.query.filter(Product.name.contains(query) |
        Product.short_description.contains(query) |
        Product.long_description.contains(query) |
        Product.category.contains(query))
    else:
        products = Product.query.all()

    return render_template('user/guest/store/search.html', products=products)

@app.route('/view_product', methods=["GET", "POST"])
def view_product():
    id = request.args.get('id')
    products = Product.query.filter(Product.id.contains(id))

    return render_template('user/guest/store/view_product.html', products=products)

# function to save picture (does not work)
def save_picture(form_picture):
    #random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = f_name + f_ext
    picture_path = os.path.join(app.root_path, 'static/images/productpics', picture_filename)
    form_picture.save(picture_path)

    return picture_filename

# crud for products (with authentication for logged in for now)
@app.route('/create_product', methods=["GET", "POST"])
def create_product():
    if "staff" in session:
        StaffName = session["staff"]
        valid_session, name = validate_session_open_file_admin(StaffName)

        userDict = {}
        db = shelve.open('user', 'c')
        try:
            if 'Users' in db:
                userDict = db['Users']
            else:
                db['Users']= userDict
        except:
            print("Error in retrieving Users from feedback db")
        
        db.close()

        if valid_session:
            create_product_form = Forms.CreateProduct(request.form)
            if request.method == 'POST' and create_product_form.validate():
                product = Product(img_file_name = create_product_form.img_file_name.data, name = create_product_form.name.data, price = create_product_form.price.data, category = create_product_form.category.data, short_description = create_product_form.short_description.data, long_description = create_product_form.long_description.data)
                j_db.session.add(product)
                j_db.session.commit()

                return redirect(url_for('retrieve_products'))

            return render_template('user/loggedin/CRUDProducts/create_product.html', form=create_product_form)
        else:
            session.clear()
            return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))

@app.route('/retrieve_products' , methods=["GET","POST"])
def retrieve_products():
    if "staff" in session:
        StaffName = session["staff"]
        valid_session, name = validate_session_open_file_admin(StaffName)

        userDict = {}
        db = shelve.open('user', 'c')
        try:
            if 'Users' in db:
                userDict = db['Users']
            else:
                db['Users']= userDict
        except:
            print("Error in retrieving Users from feedback db")
        
        db.close()

        if valid_session:
            products = Product.query.all()
            return render_template('user/staff/staffinventory.html', products=products)
            
            # return render_template('user/loggedin/CRUDProducts/retrieve_products.html', products=products)
        else:
            session.clear()
            return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))

@app.route('/edit_product', methods=["GET", "POST"])
def edit_product():
    if "staff" in session:
        StaffName = session["staff"]
        valid_session, name = validate_session_open_file_admin(StaffName)

        userDict = {}
        db = shelve.open('user', 'c')
        try:
            if 'Users' in db:
                userDict = db['Users']
            else:
                db['Users']= userDict
        except:
            print("Error in retrieving Users from feedback db")
        
        db.close()

        if valid_session:
            id = request.args.get('id')
            product = Product.query.filter(Product.id.contains(id)).first()
            create_product_form = Forms.CreateProduct(request.form)

            # saving changes
            if request.method == 'POST' and create_product_form.validate():
                # trying to save picture, dont work
                # if create_product_form.picture.data:
                    # picture_file = save_picture(create_product_form.picture.data)
                    # product.img_file_name = picture_file
                product.img_file_name = create_product_form.img_file_name.data    
                product.name = create_product_form.name.data
                product.price = create_product_form.price.data
                product.category = create_product_form.category.data
                product.short_description = create_product_form.short_description.data
                product.long_description = create_product_form.long_description.data
                product.stock = create_product_form.stock.data
                j_db.session.commit()
                return redirect(url_for('retrieve_products'))

            # filling form with current product's data
            elif request.method =='GET':
                create_product_form.img_file_name.data = product.img_file_name
                create_product_form.name.data = product.name
                create_product_form.price.data = product.price
                create_product_form.category.data = product.category
                create_product_form.short_description.data = product.short_description
                create_product_form.long_description.data = product.long_description
                create_product_form.stock.data = product.stock

            # deleting
            elif request.method == 'POST':
                j_db.session.delete(product)
                j_db.session.commit()
                return redirect(url_for('retrieve_products'))

            return render_template('user/loggedin/CRUDProducts/edit_product.html', product=product, form=create_product_form)
        else:
            session.clear()
            return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))

# all crud stuff without any authentitcation
"""
@app.route('/create_product', methods=["GET", "POST"])
def create_product():
    create_product_form = Forms.CreateProduct(request.form)
    if request.method == 'POST' and create_product_form.validate():
        product = Product(img_file_name = create_product_form.img_file_name.data, name = create_product_form.name.data, price = create_product_form.price.data, category = create_product_form.category.data, short_description = create_product_form.short_description.data, long_description = create_product_form.long_description.data)
        j_db.session.add(product)
        j_db.session.commit()

        return redirect(url_for('retrieve_products'))

    return render_template('user/loggedin/CRUDProducts/create_product.html', form=create_product_form)
"""

"""
@app.route('/retrieve_products', methods=["GET", "POST"])
def retrieve_products():
    products = Product.query.all()

    return render_template('user/loggedin/CRUDProducts/retrieve_products.html', products=products)
"""

"""
@app.route('/edit_product', methods=["GET", "POST"])
def edit_product():
    id = request.args.get('id')
    product = Product.query.filter(Product.id.contains(id)).first()
    create_product_form = Forms.CreateProduct(request.form)

    if request.method == 'POST' and create_product_form.validate():
        product.img_file_name = create_product_form.img_file_name.data
        product.name = create_product_form.name.data
        product.price = create_product_form.price.data
        product.category = create_product_form.category.data
        product.short_description = create_product_form.short_description.data
        product.long_description = create_product_form.long_description.data
        j_db.session.commit()
        return redirect(url_for('retrieve_products'))

    elif request.method =='GET':
        create_product_form.img_file_name.data = product.img_file_name
        create_product_form.name.data = product.name
        create_product_form.price.data = product.price
        create_product_form.category.data = product.category
        create_product_form.short_description.data = product.short_description
        create_product_form.long_description.data = product.long_description

    elif request.method == 'POST':
        j_db.session.delete(product)
        j_db.session.commit()
        return redirect(url_for('retrieve_products'))

    return render_template('user/loggedin/CRUDProducts/edit_product.html', product=product, form=create_product_form)
"""

# joshua's work end

if __name__ == '__main__':
    j_db.create_all