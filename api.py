import pymysql
import os
import datetime
from flask import Flask, jsonify, request
from flaskext.mysql import MySQL

from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app = Flask(__name__)

# MySQL Stuff
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
app.config['MYSQL_DATABASE_USER'] = 'petstore'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Ver@c0de'
app.config['MYSQL_DATABASE_DB'] = 'flask_api'
mysql.init_app(app)

# JWT Stuff
app.config["JWT_SECRET_KEY"] = "veracode"
app.config["JWT_ACCESS_TOKEN_EXPIRES "] = datetime.timedelta(days=365) 
jwt = JWTManager(app)

###############################################################
### CREATE A USER ###
@app.route('/api/v1/user', methods=['POST'])
def addUser():
    try:
        _json = request.json
        _username = _json['username']
        _firstname = _json['firstname']
        _lastname = _json['lastname']
        _email = _json['email']
        _password = _json['password']
        _phone = _json['phone']
        conn = mysql.connect()
        cursor = conn.cursor()
        if _username and _firstname and _lastname and _email and _password and _phone and request.method == 'POST':
            cursor.execute("select username FROM users WHERE username='%s'" % (_username))
            testUser = cursor.fetchone()
            if testUser:
                return jsonify(message="User Already Exist"), 409
            else:
                insertQuery = f"INSERT INTO users (username, firstname, lastname, email, password, phone ) VALUES (%s, %s, %s, %s, %s, %s )"
                insertValues = ( _username, _firstname, _lastname, _email, _password, _phone )
                cursor.execute(insertQuery, insertValues)
                conn.commit()
                return jsonify({'message':'User added successfully!', 'id':cursor.lastrowid}), 201
        else:
            return jsonify(message="Server Error"), 500
    except Exception as e:
        print(e)

### Login Route ###
@app.route("/api/v1/user/login", methods=["POST"])
def login():
    try:
        _username = request.json["username"]
        _password = request.json["password"]
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select username, password FROM users WHERE username='%s' AND password='%s'" % (_username, _password))
        userRow = cursor.fetchone()
        if userRow:
            access_token = create_access_token(identity=_username, fresh=True, expires_delta=False )
            return jsonify(message="Login Succeeded!", access_token=access_token), 201
        else:
            return jsonify(message="Bad Username or Password"), 401
    except Exception as e:
        print(e)

### UPDATE A USER ###
# SQL Injections
@app.route('/api/v1/user/<username>', methods=['PUT'])
def updateUser(username):
    try:
        _json = request.json
        _firstname = _json['firstname']
        _lastname = _json['lastname']
        _email = _json['email']
        _password = _json['password']
        _phone = _json['phone']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select username FROM users WHERE username='%s'" % (username))
        testUpdate = cursor.fetchone()
        if testUpdate:
            cursor.execute("UPDATE users SET firstname='%s', lastname='%s', email='%s', password='%s', phone='%s' WHERE username='%s'" % (_firstname, _lastname, _email, _password, _phone, username))
            conn.commit()
            response = jsonify(message="User updated successfully!"), 200
            return response
        else:
            return jsonify(message="User does not exist"), 404
    except Exception as e:
        print(e)

### GET ALL USERS ###
@app.route('/api/v1/user')
#@jwtRequired
def allUsers():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM users")
        userRows = cursor.fetchall()
        return jsonify(userRows), 200
    except Exception as e:
        print(e)

### GET A USER BY USERNAME
@app.route('/api/v1/user/<username>', methods=['GET', 'TRACE', 'OPTIONS'])
def oneUser(username):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE username =%s", username)
        userRow = cursor.fetchone()
        if userRow:
            return jsonify(userRow), 200
        else:
            return jsonify(message="User does not exist"), 404
    except Exception as e:
        print(e)

### DELETE A USER BY USERNAME
@app.route('/api/v1/user/<username>', methods=['DELETE'])
def deleteUser(username):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("select username FROM users WHERE username='%s'" % (username))
        testDelete = cursor.fetchone()
        if testDelete:
            cursor.execute("DELETE FROM users WHERE username =%s", (username))
            conn.commit()
            res = jsonify({'message':'User deleted successfully'})
            res.status_code = 200
            return res
        else:
            return jsonify(message="User does not exist"), 404
    except Exception as e:
        print(e)

# Command Injection
# example of request: curl 'http://127.0.0.1:5000/admin/sleep%2010'
@app.route('/admin/run/<command>')
@jwt_required()
def run(command):
    out = os.popen(command).read()
    return jsonify(out)

def createTableStructure():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute( 
            """CREATE TABLE IF NOT EXISTS users (
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(45) NOT NULL,
            firstname VARCHAR(45) NULL,
            lastname VARCHAR(45) NULL,
            email VARCHAR(45) NULL,
            password VARCHAR(255) NULL,
            phone VARCHAR(45) NULL,
            userStatus INT(11) NULL);"""
        )
        conn.commit()
        cursor.execute("select id FROM users WHERE id=1")
        testWeld = cursor.fetchone()
        if testWeld:
                pass
        else:
            cursor.execute(
                """INSERT INTO users (
                id, username, firstname, lastname, email, password, phone, userStatus) 
                VALUES (
                1, "weld_pond", "Chris", "Wysopal", "weld_pond@veracode.com", "V3RAC0d3", "555.111.2222", 1 );"""
            )
            conn.commit()
    except Exception as e:
        print(e)

# set debug=False to prevent memory growth/leak.  If debug=True, on every exception (?), 
# which our scanner will cause many of, the recording of the exception seems to cause a huge spike
# in the consumed memory
if __name__ == "__main__":
    createTableStructure()
    app.run(host='0.0.0.0', port=5000, debug=False)