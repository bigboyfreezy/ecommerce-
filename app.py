from flask import *

#create a flask application


import pymysql
app = Flask(__name__)
#sessions_used in identifying a user
#You secure it by setting a unique secre key
#above_key is used to encrypt user session
app.secret_key = '1_@Mt8vU!_pRb_*B'

@app.route('/', methods=['POST','GET'])
def home():
    if request.method=='POST':
        search = request.form['search']
        # Connect to database
        connection = pymysql.connect(host='localhost', user='root', password='',
                                     database='northwind')

        # Create a cursor to execute SQL Query
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Items')
        # AFter executing the query above, get all rows
        rows = cursor.fetchall()

        # after getting the rows forward them to home.html for users to see them
        return render_template('home.html', rows=rows)



    else:
        # Connect to database
        connection = pymysql.connect(host='localhost', user='root', password='',
                                     database='northwind')

        # Create a cursor to execute SQL Query
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Items')
        # AFter executing the query above, get all rows
        rows = cursor.fetchall()

        # after getting the rows forward them to home.html for users to see them
        return render_template('home.html', rows=rows)

#we create /single/
@app.route('/single/<id>')
def single(id):
    if  'key' in session:
            # Connect to database
            connection = pymysql.connect(host='localhost', user='root', password='',
                                         database='northwind')

            # Create a cursor to execute SQL Query
            cursor = connection.cursor()
            #below %s is a placeholder o make sure that the id is actually detected
            cursor.execute('SELECT * FROM Items WHERE ProductID= %s ', (id))
            # AFter executing the query above, to get one row
            row = cursor.fetchone()

            # after getting the row forward it to single.html for users to access it
            return render_template('single.html', row=row)

    else:
        return redirect('/signin')


@app.route('/signup', methods= ['POST','GET'])
def signup():
    if request.method =='POST':
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']
        phone = request.form['phone']
        # above, we extracted the 4 inputs from the form
        if password != confirm:
            return render_template('signup.html', error='Passwords do not Match')

        elif len(password) < 8:
            return render_template('signup.html', error= 'Password must be More than 8 characters')

        else:
            # we now save our email, password, phone
            connection = pymysql.connect(host='localhost', user='root', password='',
                                         database='northWind')

            cursor = connection.cursor()
            # create an insert query to insert data to shop_users
            cursor.execute('insert into shop_users(email,password,phone)values(%s,%s,%s)',
                           (email, password, phone))
            connection.commit() # write the record to the table
            return render_template('signup.html', success='Thank you for Registering.')

    else: # this shows the form if user is not posting
        return render_template('signup.html')

@app.route('/signin', methods= ['POST','GET'])
def signin():
    if request.method =='POST':
        email = request.form['email']
        password = request.form['password']

        connection = pymysql.connect(host='localhost', user='root', password='',
                                     database='northWind')

        cursor = connection.cursor()

        cursor.execute('SELECT * FROM shop_users where email = %s and password = %s',(email,password))
    #Check if the above query has found a match
        if cursor.rowcount == 0:
            return render_template('signin.html', error='Wrong credentials')

        else:
            session['key']=email

            return redirect('/')


        #when someone has not logged in
    else:
        return render_template('signin.html')


import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth


@app.route('/mpesa_payment', methods=['POST', 'GET'])
def mpesa_payment():
    if request.method == 'POST':
        phone = str(request.form['phone'])
        amount = str(request.form['amount'])
        # GENERATING THE ACCESS TOKEN
        #You first create an account on daraja
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"

        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']

        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379" #testpaybill not the real one
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')#unreadable pass

        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": "1",  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
            "AccountReference": "account",
            "TransactionDesc": "account"
        }

        # POPULATING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL

        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        return render_template('mpesa_payment.html', msg='Please Complete Payment in Your Phone')
    else:
        return render_template('mpesa_payment.html', total_amount=total_amount)





#assignment....code for my bikes
@app.route('/bikes')
def bikes():
    if 'key' in session:  # check if user has a key, meaning if his logged in, if they have let them access bikes
        # Connect to database
        connection = pymysql.connect(host='localhost', user='root', password='',
                                     database='northwind')

        # Create a cursor to execute SQL Query
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM bikes')
        # AFter executing the query above, get all rows
        rows = cursor.fetchall()

        # after getting the rows forward them to home.html for users to see them
        return render_template('bikes.html', rows=rows)


    else:
        return redirect('/signin')  # take the back to login incase no key is available



#we create /single/
@app.route('/single2/<id>')
def single2(id):
    # Connect to database
    connection = pymysql.connect(host='localhost', user='root', password='',
                                 database='northwind')

    # Create a cursor to execute SQL Query
    cursor = connection.cursor()
    #below %s is a placeholder o make sure that the id is actually detected
    cursor.execute('SELECT * FROM bikes WHERE ProductID= %s ', (id))
    # AFter executing the query above, to get one row
    row = cursor.fetchone()

    # after getting the row forward it to single.html for users to access it
    return render_template('single2.html', row=row)



@app.route('/signout')
def signout():
    session.pop('key', None)
    return redirect('/')

#confirm if _name_ is = _main_

if __name__ == '__main__':
    app.run(debug=True)