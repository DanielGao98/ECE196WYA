import pyrebase

config = {
  "apiKey": "AIzaSyDQUF3pJGSI_CEflk2n8OV1DOa3m_R72uE",
  "authDomain": "ece196wya.firebaseapp.com",
  "databaseURL": "https://ece196wya.firebaseio.com",
  "storageBucket": "ece196wya.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()


while True:
    arr = db.child("arr").get().val()
    print("arr = ", arr)

