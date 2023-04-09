from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import bcrypt
import secrets
from werkzeug.utils import secure_filename
import os
from datetime import datetime


app = Flask(__name__)
# Configure session
app.secret_key = 'your-secret-key-here'
app = Flask(__name__)

# database connection setting
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'projectdb'
app.config['UPLOAD_FOLDER'] = './productImage'

# Configure session
app.secret_key = secrets.token_hex(16)

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute('SELECT id, role_id, username, password FROM users WHERE username = %s', [username])
        user = cur.fetchone()

        if user and bcrypt.checkpw(password, user[3].encode('utf-8')):
            session['user_id'] = user[0]
            session['username'] = user[2]
            session['role_id'] = user[1]
            return redirect(url_for('profile'))

        else:
            error = 'Invalid username or password'
            return render_template('index.html', error=error)

    else:
        return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        confirm_password = request.form['confirm_password'].encode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute('SELECT id FROM users WHERE username = %s', [username])
        user = cur.fetchone()

        if user:
            error = 'Username already taken'
            return render_template('signup.html', error=error)

        elif password != confirm_password:
            error = 'Passwords do not match'
            return render_template('signup.html', error=error)

        else:
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            cur.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username,  hashed_password))
            mysql.connection.commit()
            session['user_id'] = cur.lastrowid
            session['username'] = username
            session['role_id'] = 2;
            return redirect(url_for('profile'))

    else:
        return render_template('signup.html')

@app.route('/profile')
def profile():
    if 'user_id' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT id, username, create_time FROM users WHERE id = %s', [session['user_id']])
        user = cur.fetchone()

        if user:
            return render_template('profile.html', user=user)

    return redirect(url_for('login'))

@app.route('/admin')
def admin():
    if 'user_id' in session and session['role_id']==1:
        cur = mysql.connection.cursor()
        cur.execute('SELECT id, username FROM users where role_id=2;')
        users = cur.fetchall()
        histories={}
        for user in users:
            cur.execute('SELECT products.name, products.price,cart_items.quantity,products.image FROM products,cart_items, users where cart_items.hasCheckout=1 and products.id=cart_items.product_id and users.id=cart_items.user_id and users.id=%s;',[user[0]])
            history = cur.fetchall()
            total = 0
            for his in history:
                total += his[1]*his[2]
            histories[user[1]]=(history,total)
        return render_template('admin.html',histories = histories)   

    return render_template('index.html',error='You are not #authorized to access admin page.')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/products')
def products():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, name, description,price, image FROM products')
    products = cur.fetchall()
    return render_template('products.html',products=products)

@app.route('/product/<int:product_id>')
def product(product_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, name, description,price, image FROM products WHERE id = %s', [product_id])
    product = cur.fetchone()
    if product:
        cur.execute('SELECT users.username, comments.content, comments.time from comments, users where users.id=comments.user_id and comments.product_id = %s ORDER BY time ASC;', [product_id])
        comments = cur.fetchall()
        print('comments',comments)

    return render_template('product.html', product = product, comments=comments)

@app.route('/comment',methods=['POST'])
def comment():
    if session['user_id']:
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO `comments`( `content`, `product_id`, `user_id`) VALUES (%s, %s, %s)', (request.form['content'], request.form['product_id'],session['user_id']))
        mysql.connection.commit()
        flash('You commented sucessfully.')
        return redirect('product/'+str(request.form['product_id']))
    else:
        return redirect('product/'+str(request.form['product_id']), error="You need to login before commenting.")

@app.route('/cart',methods=['POST','GET'])
def cart():
    if request.method=="POST":
        if session['user_id'] and request.form['product_id']:
            cur = mysql.connection.cursor()
            cur.execute('SELECT id, quantity FROM cart_items WHERE hasCheckOut=0 and user_id = %s and product_id = %s', [session['user_id'], request.form['product_id']])
            cart_item = cur.fetchone()

            if cart_item:
                cur.execute("UPDATE `cart_items` SET `quantity` = %s WHERE `cart_items`.`id` = %s;", (int(cart_item[1])+int(request.form['quantity']),cart_item[0]))
                mysql.connection.commit()
                flash('Add to existing cart item sucessfully.')
            else:
                cur.execute('INSERT INTO `cart_items`( `user_id`, `product_id`, `quantity`) VALUES (%s, %s, %s)', (session['user_id'], request.form['product_id'],request.form['quantity']))
                mysql.connection.commit()
                flash('New Item has been added to cart sucessfully.')
            return redirect(url_for('cart'))
        else:
            return redirect('product/'+str(request.form['product_id']), error="You need to login/select product before adding to cart.")
    else:
        if 'user_id' in session:
            cur = mysql.connection.cursor()
            cur.execute('SELECT cart_items.id, products.name, cart_items.quantity,products.image,products.price FROM cart_items, products where hasCheckOut=0 and products.id = cart_items.product_id and cart_items.user_id = %s',[session['user_id']])
            cart_items = cur.fetchall()
            total = 0
            for i in range(len(cart_items)):
                total += cart_items[i][2]*cart_items[i][4]
            return render_template('cart.html',cart_items=cart_items, total=total)
        else:
            cur = mysql.connection.cursor()
            cur.execute('SELECT id, name, description,price, image FROM products')
            products = cur.fetchall()
            return render_template('products.html',products=products, error="You need to login/select product before adding to cart.")

@app.route('/checkout',methods=['POST'])
def checkout():
    if 'user_id' in session:
        cur = mysql.connection.cursor()
        cur.execute('UPDATE `cart_items` SET `hasCheckout` = 1 WHERE `cart_items`.`user_id` = %s;', [session['user_id']])
        mysql.connection.commit()
        flash('All items in the cart had been checked out!')
        return render_template('cart.html',cart_items=())
    else:
        cur = mysql.connection.cursor()
        cur.execute('SELECT id, name, description,price, image FROM products')
        products = cur.fetchall()
        return render_template('products.html',products=products, error="You need to login/select product before adding to cart.")

@app.route('/remove_from_cart/<int:item_id>',methods=['POST'])
def remove_from_cart(item_id):
    if 'user_id' in session:
        cur = mysql.connection.cursor()
        cur.execute('delete from cart_items WHERE hasCheckOut=0 and id = %s and user_id=%s', [item_id, session['user_id']])
        mysql.connection.commit()
        cur = mysql.connection.cursor()
        cur.execute('SELECT cart_items.id, products.name, cart_items.quantity,products.image,products.price FROM cart_items, products where hasCheckOut=0 and products.id = cart_items.product_id and cart_items.user_id = %s',[session['user_id']])
        cart_items = cur.fetchall()
        total = 0
        for i in range(len(cart_items)):
            total += cart_items[i][2]*cart_items[i][4]
        return render_template('cart.html',cart_items=cart_items, total=total)
    else:
        cur = mysql.connection.cursor()
        cur.execute('SELECT id, name, description,price, image FROM products')
        products = cur.fetchall()
        return render_template('products.html',products=products, error="You need to login/select product before adding to cart.")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/addProduct', methods=['GET','POST'])
def addProduct():
    if 'username' not in session or session['role_id'] != 1:
        flash('You do not have permission to access that page.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Get form data from request object
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        image = request.files['image']

        cur = mysql.connection.cursor()
        cur.execute('SELECT id FROM products WHERE name = %s', [name])
        product = cur.fetchone()

        if product:
            return render_template('addProduct.html',error='Product Name:'+name+' already existed.')
        # Validate form data
        if not name or not description or not price or not image:
            flash('Please fill out all form fields.', 'danger')
            return redirect(url_for('addProduct'))

        # Save product to database
        filename = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")+secure_filename(image.filename)
        image.save(os.path.join('static',app.config['UPLOAD_FOLDER'], filename))
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO products (name, description, price, image) VALUES (%s, %s, %s, %s)', (name, description,price,filename))
        mysql.connection.commit()
        # Redirect to product page
        flash('Product created successfully!', 'success')
        return redirect(url_for('products'))
    flash('Tips: Products cannot have same name.')
    return render_template('addProduct.html')

@app.route('/deleteProduct/<int:product_id>')
def deleteProduct(product_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, name,image FROM products WHERE id = %s', [product_id])
    product = cur.fetchone()
    if product:
        try:
            cur.execute('delete FROM products WHERE id = %s', [product_id])
            mysql.connection.commit()
            try:
                os.remove(os.path.join('static',app.config['UPLOAD_FOLDER'], product[2]))
                flash('Product '+product[1]+' was deleted!')
            except:
                flash('Product '+product[1]+' image was deleted before!')
            
            return redirect(url_for('products'))
        except:
            cur = mysql.connection.cursor()
            cur.execute('SELECT id, name, description,price, image FROM products')
            products = cur.fetchall()
            return render_template('products.html',products=products,error='Product '+product[1]+' cannot be deleted since it has been bought by customers.')
    else:
        return redirect(url_for('products'), error="Already deleted.")

@app.route('/updateProduct/<int:product_id>', methods=['GET','POST'])
def updateProduct(product_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, name, description,price, image FROM products WHERE id = %s', [product_id])
    product = cur.fetchone()
    productList = list(product)
    if request.method=='POST':
        if product:
            if request.form['name']:
                if request.form['name']!=product[1]:
                    cur.execute('SELECT id FROM products WHERE name = %s', [request.form['name']])
                    otherproduct = cur.fetchone()
                    if otherproduct:
                        return render_template('updateProduct.html',product= product, error="Product Name "+product[1]+"  already exists.")
                    else:
                        #update product
                        productList[1]=request.form['name']
                if request.form['description']:
                    productList[2]=request.form['description']
                if request.form['price']:
                    productList[3]=request.form['price']
                if request.files['image']:
                    try:
                        os.remove(os.path.join('static',app.config['UPLOAD_FOLDER'], product[4]))
                    except:
                        flash('Product '+product[1]+' image was deleted before!')
                    image = request.files['image']
                    productList[4] = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")+secure_filename(image.filename)
                    image.save(os.path.join('static',app.config['UPLOAD_FOLDER'], productList[4]))
                cur.execute('UPDATE `products` SET `name`=%s,`description`=%s,`price`=%s,`image`=%s WHERE id= %s', (productList[1],productList[2],productList[3],productList[4],productList[0]))
                mysql.connection.commit()
                flash('Update successfully.')
                return render_template('updateProduct.html',product= productList)
        else:
            return render_template('products.html', error="No such product")
    else:
        if product:
            return render_template('updateProduct.html',product= product)
        else:
            return render_template('products.html', error="No such product")

if __name__ == '__main__':
    app.run(debug=True)
