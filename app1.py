import pymysql
from flask import Flask, flash,render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash


import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'TIGER'

app.config['MYSQL_HOST'] = 'sql6.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql6406115'
app.config['MYSQL_PASSWORD'] = 'XcI8eG8Mcz'
app.config['MYSQL_DB'] = 'sql6406115'

mysql = MySQL(app)



@app.route('/user/login/', methods=['GET', 'POST'])
def login():
    msg = 'Please enter your username and password'
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM account1 WHERE username = %s AND password = %s', (username, password,))
        acc = cursor.fetchone()
        if acc:
            session['loggedin'] = True
            session['id'] = acc['id']
            session['username'] = acc['username']
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username or password!'
    return render_template('index1.html', msg=msg)

@app.route('/user/login/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   session.clear()
   return redirect(url_for('login'))

@app.route('/user/login/register', methods=['GET', 'POST'])
def register():
    msg = 'Sign up!'
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'phone' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM account1 WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not re.match(r'[0-9]+', phone):
            msg = 'phone no must contain only  numbers!'
        elif not username or not password or not email or not phone:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO account1 VALUES (NULL, %s, %s, %s,%s)', (username, password, email,phone,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)


@app.route('/admin/login/', methods=['GET', 'POST'])
def login2():
    msg = 'Please enter your username and password'
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM account2 WHERE username = %s AND password = %s', (username, password,))
        acc2 = cursor.fetchone()
        if acc2:
            session['loggedin'] = True
            session['username'] = acc2['username']
            return redirect(url_for('home2'))
        else:
            msg = 'Incorrect username or password!'
    return render_template('admindex.html', msg=msg)

@app.route("/home")
def home():
    if 'loggedin' in session:
        return render_template("index.html",username=session['username'])
    return redirect(url_for('login'))


@app.route("/adminhome")
def home2():
    if 'loggedin' in session:
        return render_template('admhome.html', username=session['username'])
    return redirect(url_for('login2'))

@app.route('/adminhome/profile')
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM account2 WHERE username = %s', (session['username'],))
        acc = cursor.fetchone()
        return render_template('profile.html', account=acc)
    return redirect(url_for('login2'))   

@app.route('/adminhome/logout')
def logout2():
   session.pop('loggedin', None)
   session.pop('username', None)
   session.clear()
   return redirect(url_for('login2'))

@app.route("/about")
def about():
    if 'loggedin' in session:
        return render_template("about.html")
    return redirect(url_for('login'))



@app.route("/products1")
def products1():
    if 'loggedin' in session:
        return render_template("products1.html")
    return redirect(url_for('login'))


@app.route("/payment")
def payment():
    if 'loggedin' in session:
        return render_template("payment.html")
    return redirect(url_for('login'))



@app.route("/store")
def store():
    if 'loggedin' in session:
        return render_template("store.html")
    return redirect(url_for('login'))    

@app.route("/menudb")
def menudbtest():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT (@row_number:=@row_number + 1) AS row_num, name,code,price FROM chinese1, (SELECT @row_number:=0) AS temp ORDER BY name')
        data1 = cursor.fetchall()
        return render_template('menu1.html', data=data1)
    return redirect(url_for('login2'))

@app.route('/menudb/addchinese', methods=['GET', 'POST'])
def chiadd():
    if 'loggedin' in session:
        msg = 'Please enter item to be added'
        if request.method == 'POST' and 'name' in request.form and 'code' in request.form and 'price' in request.form:
            name = request.form['name']
            price = request.form['price']
            code= request.form['code']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM chinese1 WHERE name = %s', (name,))
            data1 = cursor.fetchone()
            if data1:
                 msg = 'Account already exists!'
            elif not name or not price or not code :
                 msg = 'Please fill out the form!'
            else:
                 cursor.execute("INSERT INTO chinese1 VALUES ( %s, %s, %s)", (name,code,int(price)))
                 mysql.connection.commit()
                 msg = 'You have successfully added item!'
        elif request.method == 'POST':
            msg = 'Please fill out the form!'
        return render_template('chineseadd.html', msg=msg)
    return redirect(url_for('login2'))

@app.route('/menudb/deletechinese', methods=['GET', 'POST'])
def chidel():
    if 'loggedin' in session:
        msg = 'Please enter item to be deleted'
        if request.method == 'POST' and 'name' in request.form:
            name = request.form['name']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM chinese1 WHERE name = %s", (name,))
            data1 = cursor.fetchone()
            if data1:
                 cursor.execute("DELETE FROM chinese1 WHERE name = %s",(name,))
                 mysql.connection.commit()
                 msg = 'You have successfully deleted item!'
        elif request.method == 'POST':
            msg = 'Please fill out the form!'
        return render_template('chinesedel.html', msg=msg)
    return redirect(url_for('login2'))

@app.route("/menudb1")
def inddbtest():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT (@row_number:=@row_number + 1) AS row_num, name,code,price FROM indian1, (SELECT @row_number:=0) AS temp ORDER BY name')
        data1 = cursor.fetchall()
        return render_template('indianmenu1.html', data=data1)
    return redirect(url_for('login2'))

@app.route('/menudb1/addindian', methods=['GET', 'POST'])
def indadd():
    if 'loggedin' in session:
        msg = 'Please enter item to be added'
        if request.method == 'POST' and 'name' in request.form and'code' in request.form and 'price' in request.form:
            name = request.form['name']
            price = request.form['price']
            code= request.form['code']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM indian1 WHERE name = %s', (name,))
            data1 = cursor.fetchone()
            if data1:
                 msg = 'Account already exists!'
            elif not name or not code or not price :
                 msg = 'Please fill out the form!'
            else:
                 cursor.execute("INSERT INTO indian1 VALUES ( %s, %s, %s)", (name, code,int(price)))
                 mysql.connection.commit()
                 msg = 'You have successfully added item!'
        elif request.method == 'POST':
            msg = 'Please fill out the form!'
        return render_template('indianadd.html', msg=msg)
    return redirect(url_for('login2'))

@app.route('/menudb1/deleteindian', methods=['GET', 'POST'])
def inddel():
    if 'loggedin' in session:
        msg = 'Please enter item to be deleted'
        if request.method == 'POST' and 'name' in request.form :
            name = request.form['name']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM indian1 WHERE name = %s', (name,))
            data1 = cursor.fetchone()
            if data1:
                 cursor.execute('DELETE FROM indian1 WHERE name = %s',(name,))
                 mysql.connection.commit()
                 msg = 'You have successfully deleted item!'
        elif request.method == 'POST':
            msg = 'Please fill out the form!'
        return render_template('indiandel.html', msg=msg)
    return redirect(url_for('login2'))

@app.route("/menudb2")
def lbdbtest():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT (@row_number:=@row_number + 1) AS row_num, name,code,price FROM lunch1, (SELECT @row_number:=0) AS temp ORDER BY name')
        data1 = cursor.fetchall()
        return render_template('lunchbev1.html', data=data1)
    return redirect(url_for('login2'))

@app.route('/menudb2/addlb', methods=['GET', 'POST'])
def lbadd():
    if 'loggedin' in session:
        msg = 'Please enter item to be added'
        if request.method == 'POST' and 'name' in request.form and 'code' in request.form and 'price' in request.form:
            name = request.form['name']
            code = request.form['code']
            price = request.form['price']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM lunch1 WHERE name = %s', (name,))
            data1 = cursor.fetchone()
            if data1:
                 msg = 'Account already exists!'
            elif not name or not code or not price :
                 msg = 'Please fill out the form!'
            else:
                 cursor.execute("INSERT INTO lunch1 VALUES ( %s, %s,%s)", (name, code, int(price)))
                 mysql.connection.commit()
                 msg = 'You have successfully added item!'
        elif request.method == 'POST':
            msg = 'Please fill out the form!'
        return render_template('lbadd.html', msg=msg)
    return redirect(url_for('login2'))

@app.route('/menudb2/deletelb', methods=['GET', 'POST'])
def lbdel():
    if 'loggedin' in session:
        msg = 'Please enter item to be deleted'
        if request.method == 'POST' and 'name' in request.form :
            name = request.form['name']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM lunch1 WHERE name = %s', (name,))
            data1 = cursor.fetchone()
            if data1:
                 cursor.execute('DELETE FROM lunch1 WHERE name = %s',(name,))
                 mysql.connection.commit()
                 msg = 'You have successfully deleted item!'
        elif request.method == 'POST':
            msg = 'Please fill out the form!'
        return render_template('lbdel.html', msg=msg)
    return redirect(url_for('login2'))
'''
@app.route('/cart/add', methods=['POST'])
def add_product_to_cart():
    if 'loggedin' in session: 
            
        

            if 'quantity' in request.form and 'code' in request.form and request.method == 'POST':
                _quantity = int(request.form['quantity'])
                _code = request.form['code']
                # validate the received values
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT * FROM chinese1 WHERE code=%s UNION SELECT * FROM lunch1 WHERE code=%s UNION SELECT * FROM indian1 WHERE code=%s", (_code,_code,_code,))
                row = cursor.fetchone()
                
                itemArray = { row['code'] : {'name' : row['name'], 'code' : row['code'], 'quantity' : _quantity, 'price' : row['price'], 'total_price': _quantity * row['price']}}
                
                all_total_price = 0
                all_total_quantity = 0
                
                session.modified = True
                if 'cart_item' in session:
                    if row['code'] in session['cart_item']:
                        for key, value in session['cart_item'].items():
                            if row['code'] == key:
                                #session.modified = True
                                #if session['cart_item'][key]['quantity'] is not None:
                                #   session['cart_item'][key]['quantity'] = 0
                                old_quantity = session['cart_item'][key]['quantity']
                                total_quantity = old_quantity + _quantity
                                session['cart_item'][key]['quantity'] = total_quantity
                                session['cart_item'][key]['total_price'] = total_quantity * row['price']
                    else:
                        session['cart_item'] = array_merge(session['cart_item'], itemArray)

                    for key, value in session['cart_item'].items():
                        individual_quantity = int(session['cart_item'][key]['quantity'])
                        individual_price = float(session['cart_item'][key]['total_price'])
                        all_total_quantity = all_total_quantity + individual_quantity
                        all_total_price = all_total_price + individual_price
                else:
                    session['cart_item'] = itemArray
                    all_total_quantity = all_total_quantity + _quantity
                    all_total_price = all_total_price + _quantity * row['price']
                
                session['all_total_quantity'] = all_total_quantity
                session['all_total_price'] = all_total_price
                
                return redirect(url_for('.products'))
            else:           
                return 'Error while adding item to cart'
        
        
    return redirect(url_for('login'))    
 '''

@app.route('/indianmenu/add', methods=['POST'])
def add_product_to_cart1():
    if 'loggedin' in session: 
            
        

            if 'quantity' in request.form and 'code' in request.form and request.method == 'POST':
                _quantity = int(request.form['quantity'])
                _code = request.form['code']
                # validate the received values
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT * FROM indian1 WHERE code=%s ", (_code,))
                row = cursor.fetchone()
                
                itemArray = { row['code'] : {'name' : row['name'], 'code' : row['code'], 'quantity' : _quantity, 'price' : row['price'], 'total_price': _quantity * row['price']}}
                
                all_total_price = 0
                all_total_quantity = 0
                
                session.modified = True
                if 'cart_item' in session:
                    if row['code'] in session['cart_item']:
                        for key, value in session['cart_item'].items():
                            if row['code'] == key:
                                #session.modified = True
                                #if session['cart_item'][key]['quantity'] is not None:
                                #   session['cart_item'][key]['quantity'] = 0
                                old_quantity = session['cart_item'][key]['quantity']
                                total_quantity = old_quantity + _quantity
                                session['cart_item'][key]['quantity'] = total_quantity
                                session['cart_item'][key]['total_price'] = total_quantity * row['price']
                    else:
                        session['cart_item'] = array_merge(session['cart_item'], itemArray)

                    for key, value in session['cart_item'].items():
                        individual_quantity = int(session['cart_item'][key]['quantity'])
                        individual_price = float(session['cart_item'][key]['total_price'])
                        all_total_quantity = all_total_quantity + individual_quantity
                        all_total_price = all_total_price + individual_price
                else:
                    session['cart_item'] = itemArray
                    all_total_quantity = all_total_quantity + _quantity
                    all_total_price = all_total_price + _quantity * row['price']
                
                session['all_total_quantity'] = all_total_quantity
                session['all_total_price'] = all_total_price
                
                return redirect(url_for('.indianmenu'))
            else:           
                return 'Error while adding item to cart'
        
        
    return redirect(url_for('login'))

@app.route('/menu/add', methods=['POST'])
def add_product_to_cart2():
    if 'loggedin' in session: 
            
        

            if 'quantity' in request.form and 'code' in request.form and request.method == 'POST':
                _quantity = int(request.form['quantity'])
                _code = request.form['code']
                # validate the received values
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT * FROM chinese1 WHERE code=%s ", (_code,))
                row = cursor.fetchone()
                
                itemArray = { row['code'] : {'name' : row['name'], 'code' : row['code'], 'quantity' : _quantity, 'price' : row['price'], 'total_price': _quantity * row['price']}}
                
                all_total_price = 0
                all_total_quantity = 0
                
                session.modified = True
                if 'cart_item' in session:
                    if row['code'] in session['cart_item']:
                        for key, value in session['cart_item'].items():
                            if row['code'] == key:
                                #session.modified = True
                                #if session['cart_item'][key]['quantity'] is not None:
                                #   session['cart_item'][key]['quantity'] = 0
                                old_quantity = session['cart_item'][key]['quantity']
                                total_quantity = old_quantity + _quantity
                                session['cart_item'][key]['quantity'] = total_quantity
                                session['cart_item'][key]['total_price'] = total_quantity * row['price']
                    else:
                        session['cart_item'] = array_merge(session['cart_item'], itemArray)

                    for key, value in session['cart_item'].items():
                        individual_quantity = int(session['cart_item'][key]['quantity'])
                        individual_price = float(session['cart_item'][key]['total_price'])
                        all_total_quantity = all_total_quantity + individual_quantity
                        all_total_price = all_total_price + individual_price
                else:
                    session['cart_item'] = itemArray
                    all_total_quantity = all_total_quantity + _quantity
                    all_total_price = all_total_price + _quantity * row['price']
                
                session['all_total_quantity'] = all_total_quantity
                session['all_total_price'] = all_total_price
                
                return redirect(url_for('.menu'))
            else:           
                return 'Error while adding item to cart'
        
        
    return redirect(url_for('login'))

@app.route('/lunchbev/add', methods=['POST'])
def add_product_to_cart3():
    if 'loggedin' in session: 
            
        

            if 'quantity' in request.form and 'code' in request.form and request.method == 'POST':
                _quantity = int(request.form['quantity'])
                _code = request.form['code']
                # validate the received values
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT * FROM lunch1 WHERE code=%s ", (_code,))
                row = cursor.fetchone()
                
                itemArray = { row['code'] : {'name' : row['name'], 'code' : row['code'], 'quantity' : _quantity, 'price' : row['price'], 'total_price': _quantity * row['price']}}
                
                all_total_price = 0
                all_total_quantity = 0
                
                session.modified = True
                if 'cart_item' in session:
                    if row['code'] in session['cart_item']:
                        for key, value in session['cart_item'].items():
                            if row['code'] == key:
                                #session.modified = True
                                #if session['cart_item'][key]['quantity'] is not None:
                                #   session['cart_item'][key]['quantity'] = 0
                                old_quantity = session['cart_item'][key]['quantity']
                                total_quantity = old_quantity + _quantity
                                session['cart_item'][key]['quantity'] = total_quantity
                                session['cart_item'][key]['total_price'] = total_quantity * row['price']
                    else:
                        session['cart_item'] = array_merge(session['cart_item'], itemArray)

                    for key, value in session['cart_item'].items():
                        individual_quantity = int(session['cart_item'][key]['quantity'])
                        individual_price = float(session['cart_item'][key]['total_price'])
                        all_total_quantity = all_total_quantity + individual_quantity
                        all_total_price = all_total_price + individual_price
                else:
                    session['cart_item'] = itemArray
                    all_total_quantity = all_total_quantity + _quantity
                    all_total_price = all_total_price + _quantity * row['price']
                
                session['all_total_quantity'] = all_total_quantity
                session['all_total_price'] = all_total_price
                
                return redirect(url_for('.lunchbev'))
            else:           
                return 'Error while adding item to cart'
        
        
    return redirect(url_for('login'))

@app.route('/cart')
def products():
    if 'loggedin' in session:

        return render_template('cart.html')         
            
    return redirect(url_for('login')) 

@app.route("/indianmenu")
def indianmenu():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT (@row_number:=@row_number + 1) AS row_num, name,price,code FROM indian1, (SELECT @row_number:=0) AS temp ORDER BY name')
        data2 = cursor.fetchall()
        return render_template('indianmenu.html', data=data2)
    return redirect(url_for('login'))

@app.route("/lunchbev")
def lunchbev():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT (@row_number:=@row_number + 1) AS row_num, name,price,code FROM lunch1, (SELECT @row_number:=0) AS temp ORDER BY name')
        data2 = cursor.fetchall()
        return render_template('lunchbev.html', data=data2)
    return redirect(url_for('login'))

@app.route("/menu")
def menu():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT (@row_number:=@row_number + 1) AS row_num, name,price,code FROM chinese1, (SELECT @row_number:=0) AS temp ORDER BY name')
        data2 = cursor.fetchall()
        return render_template('menu.html', data=data2)
    return redirect(url_for('login'))

@app.route('/empty')
def empty_cart():
     if 'loggedin' in session:
        try:  
            session['loggedin']=True
            username=session['username']
            uid=session['id']          
            session.clear()
            session['loggedin']=True
            session['username']=username
            session['id']=uid
            return redirect(url_for('.home'))
        except Exception as e:
            print(e)
     return redirect(url_for('login'))
      
@app.route('/cart/delete/<string:code>')
def delete_product(code):
    if 'loggedin' in session:
        try:
            all_total_price = 0
            all_total_quantity = 0
            session.modified = True
            
            for item in session['cart_item'].items():
                if item[0] == code:             
                    session['cart_item'].pop(item[0], None)
                    if 'cart_item' in session:
                        for key, value in session['cart_item'].items():
                            individual_quantity = int(session['cart_item'][key]['quantity'])
                            individual_price = float(session['cart_item'][key]['total_price'])
                            all_total_quantity = all_total_quantity + individual_quantity
                            all_total_price = all_total_price + individual_price
                    break
            
            
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price
            
            #return redirect('/')
            return redirect(url_for('.products'))
        except Exception as e:
            print(e)
    return redirect(url_for('login'))
    

@app.route('/addtodb')
def addtodb():
    if 'loggedin' in session:
        try: 
                from datetime import datetime
                import pytz
                ist =pytz.timezone('Asia/Calcutta')
                str=datetime.now(ist)
                curtime = str.strftime("%y-%m-%d %H:%M:%S")
                for item in session['cart_item'].items():
                    if 'cart_item' in session:
                        for key, value in session['cart_item'].items():
                         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                         
                         
                         
                        
                         cursor.execute("INSERT INTO order1 VALUES ( %s,%s,%s, %s, %s,%s,%s,%s)", (session['username'],session['cart_item'][key]['name'],session['cart_item'][key]['code'],int(session['cart_item'][key]['quantity']),int(session['cart_item'][key]['price']),int(session['cart_item'][key]['total_price']),curtime,'Not Ready'))

                         mysql.connection.commit()
                
                    break
                return redirect(url_for('.thanku'))
        except Exception as e:
            print(e)

    return redirect(url_for('login'))

@app.route("/thanku")
def thanku():
    if 'loggedin' in session:
        return render_template("thanku.html")
    return redirect(url_for('login'))    

@app.route('/emp/login/', methods=['GET', 'POST'])
def login3():
    msg = 'Please enter your username and password'
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM account3 WHERE username = %s AND password = %s', (username, password,))
        acc2 = cursor.fetchone()
        if acc2:
            session['loggedin'] = True
            session['username'] = acc2['username']
            return redirect(url_for('home3'))
        else:
            msg = 'Incorrect username or password!'
    return render_template('empindex.html', msg=msg)

@app.route("/emplohome")
def home3():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM order1 WHERE `state`=%s OR `state`=%s ORDER BY `time`,username ASC',('Not Ready','Ready',))
        data1 = cursor.fetchall()
        return render_template('emplo.html', data=data1,username=session['username'])
    return redirect(url_for('login3'))

@app.route('/emplohome/ready', methods=['POST'])
def ready():
    if 'loggedin' in session:
        
            if  'state' in request.form and'code' in request.form and 'username' in request.form and 'time' in request.form and request.method == 'POST':
                _state = request.form['state']
                _code = request.form['code']
                _time = request.form['time']
                _username = request.form['username']
                # validate the received values
                if _state=="Not Ready":
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute("UPDATE order1 SET `state`=%s,`time`=%s WHERE code=%s AND username=%s AND `time`=%s ", ('Ready',_time,_code,_username,_time,))
                    mysql.connection.commit()
                elif _state=="Ready":
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute("UPDATE order1 SET `state`=%s,`time`=%s WHERE code=%s AND username=%s AND `time`=%s ", ('Recieved',_time,_code,_username,_time,))
                    mysql.connection.commit()
                return redirect(url_for('.home3'))
            else:           
                return 'Error while changing status'
        
    return redirect(url_for('login3'))

'''@app.route('/emplohome/recieved', methods=['POST'])
def recieved():
    if 'loggedin' in session:
        
            if  'code' in request.form and 'username' in request.form and 'time' in request.form and request.method == 'POST':
                
                _code = request.form['code']
                _time = request.form['time']
                _username = request.form['username']
                # validate the received values
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("UPDATE order1 SET `state`=%s WHERE code=%s AND username=%s AND `time`=%s ", ('Recieved',_code,_username,_time,))
                mysql.connection.commit()
                
                return redirect(url_for('.home3'))
            else:           
                return 'Error while changing status'
        
    return redirect(url_for('login'))
'''


@app.route('/emplohome/logout')
def logout3():
   session.pop('loggedin', None)
   session.pop('username', None)
   session.clear()
   return redirect(url_for('login3'))

@app.route('/user/profile')
def pro():
    if 'loggedin' in session:
       
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM order1 WHERE username = %s ORDER BY `time` DESC', (session['username'],))
        data1 = cursor.fetchall()
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT (@row_number:=@row_number + 1) AS row_num,`time`,date(`time`) as dt,time(`time`) as tt FROM order1, (SELECT @row_number:=0) AS temp WHERE username = %s GROUP BY `time` ORDER BY `time` DESC ', (session['username'],))
        data2 = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT (@row_number:=@row_number + 1) AS row_num,date(`time`) as dt FROM order1, (SELECT @row_number:=0) AS temp WHERE username = %s GROUP BY dt ORDER BY dt DESC ', (session['username'],))
        data3 = cursor.fetchall()
        
        return render_template('userpro1.html', data=data1,data2=data2,data3=data3,username=session['username'])
    return redirect(url_for('login'))

@app.route("/orderhistory1")
def orderhistory1():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM order1 ORDER BY `time` DESC')
        data1 = cursor.fetchall()
      
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT (@row_number:=@row_number + 1) AS row_num,`time`,date(`time`) as dt,time(`time`) as tt FROM order1, (SELECT @row_number:=0) AS temp GROUP BY `time` ORDER BY `time` DESC ' )
        data2 = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT (@row_number:=@row_number + 1) AS row_num,date(`time`) as dt FROM order1, (SELECT @row_number:=0) AS temp GROUP BY dt ORDER BY dt DESC ' )
        data3 = cursor.fetchall()
      
        return render_template('orderhistory1.html', data=data1,data2=data2,data3=data3,username=session['username'])
    return redirect(url_for('login3'))
      

   
@app.route("/orderhistory")
def orderhistory():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM order1 ORDER BY username,`time` DESC')
        data1 = cursor.fetchall()
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT (@row_number:=@row_number + 1) AS row_num,`time`,date(`time`) as dt,time(`time`) as tt FROM order1, (SELECT @row_number:=0) AS temp GROUP BY `time` ORDER BY `time` DESC ' )
        data2 = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT (@row_number:=@row_number + 1) AS row_num,date(`time`) as dt FROM order1, (SELECT @row_number:=0) AS temp GROUP BY dt ORDER BY dt DESC ' )
        data3 = cursor.fetchall()
      
        return render_template('orderhistory.html', data=data1,data2=data2,data3=data3,username=session['username'])
    return redirect(url_for('login2'))

@app.route("/historysum")
def historysum():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT date(`time`),SUM(`price`)`totalprice` FROM order1 GROUP BY date(`time`) ORDER BY date(`time`) DESC')
        data1= cursor.fetchall()
        return render_template('historysum.html', data=data1)
    return redirect(url_for('login2'))

@app.route("/historysum2")
def historysum2():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT EXTRACT(YEAR FROM `time`),EXTRACT(MONTH FROM `time`),SUM(`price`)`totalprice` FROM order1 GROUP BY EXTRACT(YEAR_MONTH FROM `time`) ORDER BY EXTRACT(YEAR_MONTH FROM `time`) DESC')
        data1= cursor.fetchall()
        return render_template('historysum2.html', data=data1)
    return redirect(url_for('login2'))    

@app.route("/historysum3")
def historysum3():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT EXTRACT(YEAR FROM `time`),EXTRACT(MONTH FROM `time`),EXTRACT(WEEK FROM `time`),SUM(`price`)`totalprice` FROM order1 GROUP BY EXTRACT(WEEK FROM `time`),EXTRACT(YEAR FROM `time`) ORDER BY EXTRACT(YEAR FROM `time`) DESC ,EXTRACT(WEEK FROM `time`) DESC')
        data1= cursor.fetchall()
        return render_template('historysum3.html', data=data1)
    return redirect(url_for('login2'))      
      


def array_merge( first_array , second_array ):
    if isinstance( first_array , list ) and isinstance( second_array , list ):
        return first_array + second_array
    elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
        return dict( list( first_array.items() ) + list( second_array.items() ) )
    elif isinstance( first_array , set ) and isinstance( second_array , set ):
        return first_array.union( second_array )
    return False        

if __name__=="__main__":
    app.run(debug=True);    

