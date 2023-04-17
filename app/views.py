from flask import render_template, request
import os
import cv2
from app.face_recognition import faceRecognitionPipeline
import matplotlib.image as mating
import time 

counter = 0

def unique_filename_f(filename):
    global counter
    current_time = int(time.time())
    counter += 1
    return f"{current_time}_{counter}_{filename}"


UPLOAD_FOLDER = "static/upload"
def index():
    return render_template('index.html')

def app():
    return render_template('app.html')

def genderapp():
    if request.method =="POST":
        f = request.files['image_name']
        # save our image in upload folder
        unique_filename = unique_filename_f(f.filename)
        path = os.path.join(UPLOAD_FOLDER, unique_filename)
        f.save(path) #save image into upload folder
        # get predictions
        pred_image, predictions = faceRecognitionPipeline(path)
        pred_filename = unique_filename_f(f'prediction_image.jpg')
        #pred_filename = 'prediction_image.jpg'
        cv2.imwrite(f'./static/predict/{pred_filename}', pred_image)
        # generate report
        report = []
        for i, obj in enumerate(predictions):
            gray_image =obj['roi'] # grayscale image
            eigen_image = obj['eig_img'].reshape(100,100) # eigen image
            gender_name = obj['prediction_name'] #name
            score = round(obj['score'] *100,2) # probaility score
            #save grayscale and eigen image in predict folder 
            gray_image_name = unique_filename_f(f'roi_{i}.jpg')
            eigen_image_name = unique_filename_f(f'eigen_{i}.jpg')
            mating.imsave(f'./static/predict/{gray_image_name}', gray_image, cmap='gray')
            mating.imsave(f'./static/predict/{eigen_image_name}', eigen_image, cmap='gray')

            # save report 
            report.append([
                gray_image_name,
                eigen_image_name,
                gender_name,
                score
            ])
        return render_template('gender.html',fileupload=True, pred_filename = pred_filename, report=report)    # Get Request



    return render_template('gender.html',fileupload=False) # Get Request