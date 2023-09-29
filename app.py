from flask import Flask, request, jsonify, render_template,make_response,url_for,redirect,session
from selenium.webdriver.common.keys import Keys  
from werkzeug.utils import secure_filename
from flask_restful import Api, Resource,reqparse
from os import system,path,makedirs
import SQLite
import random
import string

system("clear")
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'webp'])

USERNAME = "ken"
PASSWORD = "Mst@2069"
adminUser = False

#Create a Folder to Store Item Images 
if not path.exists("static/items/lostImg"):
  makedirs("static/items/lostImg")
if not path.exists("static/items/foundImg"):
  makedirs("static/items/foundImg")  
if not path.exists("Database"):
  makedirs("Database") 

#Implament The DB & Tables
found_db = SQLite.SQLiteDatabase("Database/found.db")
found_db.createTable()
lost_db = SQLite.SQLiteDatabase("Database/lost.db")
lost_db.createTable()

#Generate random Item id's
def genId():
  letters = string.ascii_letters
  return ''.join(random.choice(letters) for _ in range(6))

# Upload only allowed extentions
def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 

#print(found_db.fetchAll())
app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'UA35x2T7BT7uFKeADmi4'
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024 

# Configure the session cookie settings
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True  # Make sure secure cookies are enabled

@app.route('/')
def root():
    return redirect('/found/')

class home(Resource):
    def get(self, type):
      if type == 'found':
        #print(found_db.fetchAll())
        return make_response(render_template("found.html"))
      elif type == 'lost':
        #print(lost_db.fetchAll())
        return make_response(render_template("lost.html"))    

class uploadItem(Resource):
    def post(self):
      name = request.form.get('name')
      itemName = request.form.get('itemName')
      contact = request.form.get('contact')
      location = request.form.get('location')
      date = request.form.get('date')
      statusType = request.form.get('statusType')
      itemId = genId()
      image = request.form.get('image')

      if image != "default":
        f = request.files['image']
        if statusType == "LOST":
          f.save(f"static/items/lostImg/{f.filename}")
          if f and allowed_file(f.filename):
            f_name = secure_filename(f.filename) 
            ext = f_name.split(".")[-1]
            img_name = f"{itemId}.{ext}"
            system(f"cd static/items/lostImg/ && mv {f_name} {img_name}")
            response = lost_db.insertData(itemId,name,itemName,ext,contact,location,date,statusType) 
            if response==True:
              return {'message': 'Data Uploaded Sucessfully'}
            else:
              return response 

          else :
            app.flash('Allowed image types are - png, jpg, jpeg, gif')
            return redirect(request.url) 

        elif statusType == "FOUND":
          f.save(f"static/items/foundImg/{f.filename}") 
          if f and allowed_file(f.filename):
            f_name = secure_filename(f.filename) 
            ext = f_name.split(".")[-1]
            img_name = f"{itemId}.{ext}"
            system(f"cd static/items/foundImg/ && mv {f_name} {img_name}")
            response = found_db.insertData(itemId,name,itemName,ext,contact,location,date,statusType)
            if response==True:
              return {'message': 'Data Uploaded Sucessfully'}
            else:
              return response  

          else :
            app.flash('Allowed image types are - png, jpg, jpeg, gif')
            return redirect(request.url)   
      else:
        ext = "jpg"
        img_name = f"{itemId}.{ext}"
        if statusType == "LOST":
          system(f"cp static/images/noimage.jpeg static/items/lostImg/{img_name}")
          response = lost_db.insertData(itemId,name,itemName,ext,contact,location,date,statusType)  
        elif statusType == "FOUND":
          system(f"cp static/images/noimage.jpeg static/items/foundImg/{img_name}")
          response = found_db.insertData(itemId,name,itemName,ext,contact,location,date,statusType)
          return {'message': 'Data Uploaded Sucessfully'}  
            
         

class markItem(Resource):
    def post(self):
        itemId = request.form.get('itemId')
        statusType = request.form.get('statusType')
        if statusType == "FOUND":
          return found_db.markFound(itemId)
        else:
          return lost_db.markFound(itemId)
        

class fetchAll(Resource):
    def get(self):
      statusType = request.args.get('statusType')
      if statusType == "FOUND":
        fetched_data = found_db.fetchAll()  # Assuming this function retrieves your data
        response_data = {
            "fetched_data": fetched_data,
            "usertype": adminUser
        }
        return jsonify(response_data)
      else:
        fetched_data = lost_db.fetchAll()  # Assuming this function retrieves your data
        response_data = {
            "fetched_data": fetched_data,
            "usertype": adminUser
        }
        return jsonify(response_data)  

class report(Resource):
    def get(self):
      return make_response(render_template("report.html")) 

class delete(Resource):
    def post(self):
        itemId = request.form.get('itemId')
        statusType = request.form.get('statusType')
        #print(statusType)
        if statusType == "FOUND":
          return found_db.deleteItem(itemId)
        elif statusType == "LOST":
          return lost_db.deleteItem(itemId) 

class revert(Resource):
    def post(self):
        itemId = request.form.get('itemId')
        statusType = request.form.get('statusType')
        #print(statusType)
        if statusType == "FOUND":
          return found_db.revertItem(itemId)
        elif statusType == "LOST":
          return lost_db.revertItem(itemId)         

class login(Resource):
  def get(self):
    return make_response(render_template("login.html"))
  def post(self):
    username = request.form.get('uname')
    password = request.form.get('passw') 
    if username == USERNAME and password == PASSWORD :  
      global adminUser
      session['user'] = username 
      #return {"message":"Login Successful"}
      adminUser = True
      return {"message":"LoginSuccessful"}
    return {"message":"LoginFailed"}  
    #return make_response(render_template('login.html'))  

class logout(Resource):
  def get(self):
    global adminUser
    if 'user' in session:
        adminUser = False
        #print("Session popped")
        session.pop('user', None)
    return redirect('/')            
   

api.add_resource(home, '/<string:type>/')
api.add_resource(uploadItem, '/upload/')
api.add_resource(markItem, '/markFound/')
api.add_resource(fetchAll, '/fetch/')
api.add_resource(report, '/report/')
api.add_resource(delete, '/delete/')
api.add_resource(revert, '/revert/')
api.add_resource(login, '/login/')
api.add_resource(logout, '/logout/')

if __name__ == '__main__':
    app.run(debug=False,port=5000,host='0.0.0.0')
