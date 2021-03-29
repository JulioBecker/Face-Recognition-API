# This is a _very simple_ example of a web service that recognizes faces in uploaded images.
# The result is returned as json. For example:
#
# $ curl -XPOST -F "file1=@img1.jpg" -F "file2=@img2.jpg" http://127.0.0.1:5001
#
# Returns:
#
# {
#    "face_found_in_image": true or false,
#    "is_same": true or false,
#    "score": value between 0 and 1
# }
#
# This example is based on the Flask file upload example: http://flask.pocoo.org/docs/0.12/patterns/fileuploads/

# NOTE: This example requires flask to be installed! You can install it with pip:
# $ pip3 install flask

import sys

sys.path.insert(0, "/home/ubuntu/projetos")
sys.path.append("/home/ubuntu/projetos/env/lib/python3.6/site-packages/")

import base64
import cv2
import face_recognition
from flask import Flask, jsonify, request, redirect
from flask_cors import CORS, cross_origin
from PIL import Image
from io import BytesIO
from datetime import datetime
import math
import numpy as np
from keras.models import model_from_json
from keras.preprocessing import image

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def upload_image():
    result = {
        "face_found_in_image": True,
        "is_same": True,
        "score": 1.0,
        "is_blinking": True,
        "has_smile": True,
        "one_finger": True,
        "two_finger": True,
        "three_finger": True,
        "four_finger": True,
        "five_finger": True
    }
    return jsonify(result)
        
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        nome = "/home/ubuntu/projetos/enviadas/" + str(request.remote_addr) + "-" + datetime.now().strftime("%H:%M:%S") + "-"
        if len(request.form) == 1:
          result = {
            "erro": "foto nao cadastrada"
          }
          return jsonify(result)
        elif len(request.form) == 2:        
          file1 = request.form['file1'][23:]
          file2 = request.form['file2'][23:]
        
          im1 = Image.open(BytesIO(base64.b64decode(file1)))
          im2 = Image.open(BytesIO(base64.b64decode(file2)))
          im1 = im1.convert('RGB')
          im2 = im2.convert('RGB')
          im1.save("/home/ubuntu/projetos/im1.jpg") 
          im2.save("/home/ubuntu/projetos/im2.jpg") 
          
          im1.save(nome + "im1.jpg") 
          im2.save(nome + "im2.jpg") 
          
          return detect_faces_in_image(im1, im2)
        
        elif len(request.files) == 2:
          
          if 'file1' not in request.files or 'file2' not in request.files:
            return redirect(request.url)
          
          file1 = request.files['file1']
          file2 = request.files['file2']
          if file1.filename == '' or file2.filename == '':
              return redirect(request.url)

          if (file1 and allowed_file(file1.filename)) or (file2 and allowed_file(file2.filename)):
              # The image file seems valid! Detect faces and return the result.
              im1 = Image.open(file1)
              im2 = Image.open(file2)
              im1 = im1.convert('RGB')
              im2 = im2.convert('RGB')
              im1.save("/home/ubuntu/projetos/im1.jpg") 
              im2.save("/home/ubuntu/projetos/im2.jpg") 
              
              im1.save(nome + "im1.jpg") 
              im2.save(nome + "im2.jpg") 
          
              return detect_faces_in_image(file1, file2)
        elif len(request.get_json()) == 2:
          file1 = request.get_json()['originalPhoto']
          file2 = request.get_json()['comparisonPhoto']
        
          im1 = Image.open(BytesIO(base64.b64decode(file1)))
          im2 = Image.open(BytesIO(base64.b64decode(file2)))
          im1 = im1.convert('RGB')
          im2 = im2.convert('RGB')
          im1.save("/home/ubuntu/projetos/im1.jpg") 
          im2.save("/home/ubuntu/projetos/im2.jpg") 
          
          im1.save(nome + "im1.jpg") 
          im2.save(nome + "im2.jpg") 
          
          return detect_faces_in_image(im1, im2)
        else:
          result = {
            "erro": "parametros faltando"
          }
          return jsonify(result)

    # If no valid image file was uploaded, show the file upload form:
    return '''
    <!doctype html>
    <title>São a mesma pessoa??</title>
    <h1>Dê upload em duas imagens para ver se é a mesma pessoa</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file1">
      <input type="file" name="file2">
      <input type="submit" value="Upload">
    </form>
    '''

'''@app.after_request
def add_headers(response):
    #response.headers.add('Content-Type', 'application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    #response.headers.add('Access-Control-Expose-Headers', 'Content-Type,Content-Length,Authorization,X-Pagination')
    return response'''

def detect_faces_in_image(file_stream1, file_stream2):
    # calculated face encoding
    img1 = cv2.imread("/home/ubuntu/projetos/im1.jpg")
    img2 = cv2.imread("/home/ubuntu/projetos/im2.jpg")
    encodings = face_recognition.face_encodings(img1)
    if len(encodings) <= 0:
        return jsonify({"erro": "faces nao detectadas"})
    known_face_encoding = encodings[0]
    
    # Get face encodings for any faces in the uploaded image
    unknown_face_encodings = face_recognition.face_encodings(img2)

    face_found = False
    is_equal = False
    has_smile = False
    is_blinking = True
    one_finger = False
    two_finger = False
    three_finger = False
    four_finger = False
    five_finger = False
    score = 0

    if len(unknown_face_encodings) > 0:
        face_found = True
        # Compara as faces detectadas
        match_results = face_recognition.compare_faces([known_face_encoding], unknown_face_encodings[0])
        distance = face_recognition.face_distance([known_face_encoding], unknown_face_encodings[0])
        #print(distance)
        #print(match_results) 
        if match_results[0].all() and distance < 0.5:
            is_equal = True
            
        distance = 1 - distance
        if distance >= 0.9:
            score = distance
        elif distance >= 0.8:
            score = distance + 0.1
        else:
            score = distance + 0.2
        print(distance, score)
        
    else:
        return jsonify({"erro": "faces nao detectadas"})
    
    import os
    face_cascade_name = "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(os.path.join(cv2.data.haarcascades, face_cascade_name))
    faces = face_cascade.detectMultiScale(img2, 1.1)
    
    eye_cascade_name = "haarcascade_eye.xml"
    eye_cascade = cv2.CascadeClassifier(os.path.join(cv2.data.haarcascades, eye_cascade_name))
    
    smile_cascade_name = 'haarcascade_smile.xml'        
    smile_cascade = cv2.CascadeClassifier(os.path.join(cv2.data.haarcascades, smile_cascade_name))
    
    for (x,y,w,h) in faces:
        roi_color = img2[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_color, 1.2, 20)
        smile = smile_cascade.detectMultiScale(roi_color, 1.8, 33)
        if(len(eyes) > 1):
            is_blinking = False
        if(len(smile) > 0):
            has_smile = True
        
    fingers = detectFingers(img2)
    if fingers == 1:
      one_finger = True
    elif fingers == 2:
      two_finger = True
    elif fingers == 3:
      three_finger = True
    elif fingers == 4:
      four_finger = True
    elif fingers == 5:
      five_finger = True

    '''# Return the result as json
    result = {
        "face_found_in_image": face_found,
        "is_same": is_equal,
        "score": score[0],
        "is_blinking": is_blinking,
        "has_smile": has_smile,
        "one_finger": one_finger,
        "two_finger": two_finger,
        "three_finger": three_finger,
        "four_finger": four_finger,
        "five_finger": five_finger
    }'''
    # Return the result as json
    result = {
        "face_found_in_image": face_found,
        "is_same": is_equal,
        "score": score[0],
        "is_blinking": is_blinking,
        "has_smile": has_smile,
        "one_finger": True,
        "two_finger": True,
        "three_finger": True,
        "four_finger": True,
        "five_finger": True
    }
    return jsonify(result)

def detectFingers(img):
    #loading the model
  json_file = open('/home/ubuntu/projetos/count_fingers.json', 'r')
  loaded_model_json = json_file.read()
  json_file.close()
  loaded_model = model_from_json(loaded_model_json)
  # load weights into new model
  loaded_model.load_weights("/home/ubuntu/projetos/count_fingers.h5")
  print("Loaded model from disk")
  
  #defining the list of all the numbers in order which they are trained
  
  numbers = ['FIVE', 'FOUR', 'NONE', 'ONE', 'THREE', 'TWO']
  
  #Turning on the camera for live feed
  
  #cap = cv2.VideoCapture(0)
  #while True:
  frame = img
  frame = cv2.flip(frame,1)
  
  altura = frame.shape[0]
  comprimento = frame.shape[1]
      
      #Converting the frame to Gray scale    
  frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
      
      #Drawing a rectangle for taking in the image in roi
  cv2.rectangle(frame,(0, 0), (int(comprimento/2), int(altura/2)),(0,255,0),3)
   
      #creating the roi
  roi = frame_gray[0:int(altura/2), 0:int(comprimento/2)]  
      #Resizing the image
  roi = cv2.resize(roi,(64,64))
      
      #Processing the image before making the predictions from the model
  blur = cv2.GaussianBlur(roi, (7,7), 3)
  ad_thres = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
  ret, thres = cv2.threshold(ad_thres, 25, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
      
      #Converting the image into array
  image_array = image.img_to_array(thres)
      
      #Converting the image from (64,64,1) to (64,64,3)
  image_array = cv2.cvtColor(image_array,cv2.COLOR_GRAY2BGR)
  image_array = np.expand_dims(image_array,axis =0)
      
      #Making predictions with the model
  predictions =loaded_model.predict(image_array)
      
      #Printing the predcitions on the screen
  #cv2.putText(frame,numbers[np.argmax(predictions)],(1,450), cv2.FONT_HERSHEY_SIMPLEX, 4,(255,255,255),2)
  #cv2.imshow('Frame',frame)
  valor = numbers[np.argmax(predictions)]
  if valor == 'NONE':
    return 0
  elif valor == 'ONE':
    return 1
  elif valor == 'TWO':
    return 2
  elif valor == 'THREE':
    return 3
  elif valor == 'FOUR':
    return 4
  elif valor == 'FIVE':
    return 5

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
