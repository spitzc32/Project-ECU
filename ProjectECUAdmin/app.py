"""
	created by:   spitzc32
				  LowkeyProgrammer

	Dependencies: Database Usage: firebase_admin
				  				  pyrebase
				  Notifications:  onesignal
				  Geolocation:	  geocoder
				  				  goepy
				  Website:		  flask
	
	API's used:   Onesignal (https://documentation.onesignal.com/docs)
				  GoQR 	  (http://goqr.me/api/)
				  Google Maps Javascript API  (https://developers.google.com/maps/documentation/javascript/overview?utm_campaign=FY18-Q2-global-demandgen-paidsearchonnetworkhouseads-cs-maps_contactsal_saf&utm_term=KW_%2Bmaps+%2Bjavascript+%2Bapi-ST_%2Bmaps+%2Bjavascript+%2Bapi&gclid=Cj0KCQjwpNr4BRDYARIsAADIx9xMmu8a7d4cbVCNi5zsnymDvffv9cqynxmEhySNYfr4cwLOT88ZbuoaApxGEALw_wcB&utm_content=text-ad-none-none-DEV_c-CRE_434204568468-ADGP_Hybrid+%7C+AW+SEM+%7C+BKWS+%7E+Brand+%7C+BMM+%7C+Google+Maps+Javascript+API-KWID_43700053580897263-kwd-341556983684-userloc_9066820&utm_source=google&utm_medium=cpc)

	WEB APPLICATION: Project ECU for official Admin
	  -	This website is intended for the use of the head
		or someone in charge of the community that can 
		deploy volunteers and frontliners that can help 
		a person in need. The person who cna use this 
		website can be a head of an organization that 
		sets out to help a particular area as long as it 
		is nearby their vicinity. For establishments and 
		partnered hospitals see the other folders in the 
		source code and for individual users please use 
		the application. 

	Code intended use for Call for Code: COVID-19 Track
	  -	The credentials and the source code written are 
		meant for this sole application. We've written 
		several API keys here without security since this 
		application is only intended for this competition.




"""

#Database Imports
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pyrebase
#Push Notification Imports
import onesignal as onesignal_sdk
import requests
import json
#Geolocation
import geocoder
from geopy.distance import distance 
#Datetime
from datetime import datetime
# Website Imports
from flask import *
from flask import render_template, request, Flask



UserUID = "" #for Current User UID (Firebase Database)
#----------------Firebase Setup-------------------
firebaseConfig = {
	'apiKey': "AIzaSyB7ylmP4PvAByYA8--VbMSFonWvPa9ly_Q",
	'authDomain': "community-87c7d.firebaseapp.com",
	'databaseURL': "https://community-87c7d.firebaseio.com",
	'projectId': "community-87c7d",
	'storageBucket': "community-87c7d.appspot.com",
	'messagingSenderId': "978165544305",
	'appId': "1:978165544305:web:02736cf97efb7fb74632d0",
	'measurementId': "G-6PE507NV6F"
}
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

cred = credentials.Certificate('firebase-sdk.json')

firebase_admin.initialize_app(cred,{
	'databaseURL': 'https://community-87c7d.firebaseio.com/'
	})

#----------------Functionalities-----------------
def getLocation():
	g = geocoder.ip('me')
	return g.latlng


#-------------Website Functionalities------------
app = Flask(__name__)

#------------------Index-------------------------
@app.route('/', methods= ['GET'])
def index():
	if UserUID:
		req = UserUID 
		return render_template('index.html',req=req, lat=getLocation()[0],lng=getLocation()[1])
	else:
		return redirect(url_for('login'))


@app.route('/', methods= ['POST'])
def pushnotif():
	ref = db.reference('/')
	if request.method == 'POST':
		#getting credentials
		identity = request.form['userID']
		title = request.form['title']
		message = request.form['message']

		#Send notification
		r = ref.child('Approved').child(identity).get()

		#Create Notification
		header = {"Content-Type": "application/json; charset=utf-8",
          }

		payload = {"app_id": "5f3e9bd0-93f5-4551-9e07-37d102619eec",
	           "include_player_ids": list(map(lambda x: x.replace("\"", ''),r['volunteers'])),
	           "contents": {"en": message},
		   		}
	 
		req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))

		#store in firebase the update
		reff = db.reference('/')
		rr = reff.child('Approved').child(identity)
		rr.push({
					
						"Title": title,
						"Content": message,
						"Timestamp": str(datetime.now()).format("MM-dd-yyyy hh:mm:ss")
						
					
			})

		return redirect(url_for('index'))

		
#--------------Volunteering Service--------------
@app.route('/Volunteers', methods= ['GET'])
def Volunteer():
	if UserUID:
		req = UserUID 
		return render_template('Volunteer.html',req=req)
	else:
		return redirect(url_for('login'))
	


#----------------Delivery Services---------------
@app.route('/Deliveries', methods= ['GET'])
def deliveryService():
	if UserUID:
		req = UserUID 
		return render_template('deliveryService.html',req=req)
	else:
		return redirect(url_for('createServicePOST'))
	

@app.route('/Deliveries', methods= ['POST'])
def createServicePOST():
	ref = db.reference('/')
	if request.method == 'POST':
		ServiceName = request.form['ServiceName']
		Organization = request.form['Organization']
		RAR = request.form['RAR']
		Link = request.form['Link']
		RangeDate = request.form['RangeDate']
		tagsinput = request.form['tagsinput']
		Latitude = getLocation()[0]
		Longitude = getLocation()[1]



		# Storage
		r = ref.child('DeliveryServices')
		r.update({
			ServiceName : 
				{
				'Organization': Organization,
				'RolesAndResponsiblities': RAR,
				'RangeDate': RangeDate,
				'Link': Link,
				'ContactNo': tagsinput,
				'Latitude': Latitude,
				'Longitude': Longitude
				}
			})
		return redirect(url_for('index'))	

@app.route('/AvailableDeliveries', methods= ['GET'])
def availableDelivery():
	if request.method == 'GET' and UserUID:
		ref = db.reference('/')
		r = ref.child('DeliveryServices').get()
		return render_template('availableDelivery.html', req=r, ref=UserUID)
	else:
		redirect(url_for('login'))

@app.route("/AvailableDeliveries", methods=['POST'])
def updateDelivery():
	if request.method == 'POST':
		if request.form['btn'] == 'Update':
			ID = request.form["User"]
			Organization = request.form["Organization"]
			Contact = request.form["Contact"]
			Link = request.form["Link"]

			ref = db.reference('/DeliveryServices')
			ref.update({ID: { 'Organization': Organization,
							  }})
			ref.update({ID:{'ContactNo': Contact}})
			ref.update({ID:{'Link': Link}})
			req = ref.get()
			return render_template('availableDelivery.html', req=req, ref=UserUID)
		else:
			ID = request.form["User"]
			ref = db.reference('/DeliveryServices')
			ref.child(ID).delete()
			req = ref.get()
			return render_template('availableDelivery.html', req=req, ref=UserUID)

#---------------Partnered Hospitals-------------- 
@app.route('/AddHospital', methods= ['GET'])
def partneredHospital():
	if UserUID:
		req = UserUID 
		return render_template('PHospital.html',req=req)
	else:
		return redirect(url_for('login'))
	
@app.route('/AddHospital', methods= ['POST'])
def createHospital():
	ref = db.reference('/')
	if request.method == 'POST':
		HosName = request.form['HosName']
		Address = request.form['Address']
		Description = request.form['Description']
		OpeningHours = request.form['OpeningHours']
		Link = request.form['Link']
		
		# Storage
		r = ref.child('DeliveryServices')
		r.update({
			ServiceName : 
				{
				'HospitalName': HosName,
				'Address': Address,
				'Description': Description,
				'OpeningHours': OpeningHours,
				'Link': Link
				}
			})
		return redirect(url_for('index'))


#---------------Emeregency Requests--------------
@app.route('/ERequest', methods= ['GET'])
def eRequest():
	if request.method == 'GET' and UserUID:
		ref = db.reference('/')
		r = ref.child('EmergencyRequest').get()
		return render_template('blank.html', req=r, ref=UserUID)
	else:
		return redirect(url_for('login'))
		
@app.route('/ERequest', methods=['POST'])
def finishedER():
	if request.method == 'POST':
		if request.form['btn'] == 'Accept':
			#Changing Stat to Approved
			ID = request.form["user"]
			urgency = request.form["Urgency"]
			ref = db.reference('/EmergencyRequest')
			ref.child(ID).update({ 'Urgency': urgency,
									'Response': 'Accepted'})

			#Getting userids
			r = db.reference('/').child('Users').get()
			users = []
			for item in r.keys():
				coord1 = tuple(getLocation())
				coord2 = (r[item]['Latitude'],r[item]['Longitude'])
				if distance(coord1, coord2).mi  <= 20:
					users.append(r[item]['UserID'])

			#Updating App reference to ledger
			Contact = request.form['Contact']
			Description = request.form['Description']
			Apref = db.reference('/Approved')
			
			Apref.update({
			ID:{
				'volunteers':users,
				'Latitude': getLocation()[0],
				'Longitude': getLocation()[1],
				'D1':{
						"Title": "Start of Request",
						"Content": f"Description: {Description} \nContact No:{Contact}" ,
						"Date": str(datetime.now()).format("MM-dd-yyyy hh:mm:ss")
						}
					}
			})

			req = ref.get()
			return render_template('blank.html', req=req, ref=UserUID)
		else:
			ID = request.form["user"]
			print(ID,"Hello")
			ref = db.reference('/EmergencyRequest')
			ref.child(ID).delete()
			return redirect(url_for('index'))

#---------------------Logout----------------------
@app.route('/Logout', methods= ['GET'])
def expireSession():
	UserUID = ""
	return render_template('login.html')

#---------------------Login----------------------
@app.route('/login', methods= ['GET'])
def login():
	return render_template('login.html')

@app.route('/login', methods= ['POST'])
def VerifyCred():
	global UserUID
	if request.method == 'POST':
		email = request.form['Username']
		password = request.form['password']
		user = auth.sign_in_with_email_and_password(email, password)
		if user['localId']:
			r = user['localId']
			UserUID = user['localId']
			return redirect(url_for('index', req=r ))
		else:
			return render_template('login.html')



#------------------Sign Up-----------------------
@app.route('/SignUp', methods= ['GET'])
def signup():
	return render_template('signup.html')

@app.route('/SignUp', methods= ['POST'])
def SignUser():
	if request.method == 'POST':
		email = request.form['Username']
		password = request.form['password']
		auth.create_user_with_email_and_password(email,password)
		return redirect(url_for('login'))
	

#------------------Feedbacks---------------------
@app.route('/FeedBacks')
def feeds():
	if UserUID:
		ref = db.reference('/')
		r = ref.child('Feeds').get()
		return render_template('positive_feedbacks.html', req=r, ref=UserUID)
	else:
		return redirect(url_for('login'))

#------------------Notification---------------------
@app.route('/Contact')
def contacts():
	if UserUID:
		return render_template('contact.html', ref=UserUID)
	else:
		return redirect(url_for('login'))
	
@app.route('/Contact', methods=['POST'])
def getcontacts():
	ref = db.reference('/')
	if request.method == 'POST':
		name = request.form['name']
		subject = request.form['subject']
		message = request.form['message']
		num = request.form['num']
		Latitude = getLocation()[0]
		Longitude = getLocation()[1]

		#Getting userids
		r = ref.child('Users').get()
		users = []
		for item in r.keys():
			coord1 = tuple(getLocation())
			coord2 = (r[item]['Latitude'],r[item]['Longitude'])
			if distance(coord1, coord2).km  <= float(num):
				users.append(r[item]['UserID'].replace("\"", ''))

		#Create Notification
		header = {"Content-Type": "application/json; charset=utf-8"}
          
		payload = {"app_id": "5f3e9bd0-93f5-4551-9e07-37d102619eec",
	           "include_player_ids": users,
	           "contents": {"en": message},
		   		}
	 
		req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
		return render_template('contact.html')



#------------------Events------------------------
@app.route('/reliefEvents', methods= ['GET'])
def reliefEvents():
	if UserUID:
		return render_template('reliefEvents.html', ref=UserUID)
	else:
		return redirect(url_for('login'))
	

@app.route('/reliefEvents', methods= ['POST'])
def createEventPOST():
	ref = db.reference('/')
	if request.method == 'POST':
		eventName = request.form['EventName']
		eventHost = request.form['EventHost']
		Description = request.form['Description']
		Qualifications = request.form['Qualifications']
		RangeDate = request.form['RangeDate']
		Latitude = getLocation()[0]
		Longitude = getLocation()[1]

		# Storage
		r = ref.child('Locations')
		r.update({
			eventName : 
				{
				'EventHost': eventHost,
				'Description': f"\"{Description}\"",
				'Qualifications': f"\"{Qualifications}\"",
				'RangeDate': f"\"{RangeDate}\"",
				'Latitude': Latitude,
				'Longitude': Longitude
				}
			})

		return redirect(url_for('index'))



if __name__ == '__main__':
	app.run(debug=True)
