from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import time


app = Flask(__name__)
app.secret_key = 'realysecurekeydontyouthinkimeanwhocreatessuchakey'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
@app.route('/survey')
def survey():
   return render_template('survey.html')


@app.route('/')
def index():
   return render_template('index.html')


@app.route('/about')
def about():
   about_text = (
       "<br>"
       "ColoDetect v1.0<br>"
       "<br>"
       "Creator: N/A<br>"
       "<br>"
       "Description:<br>"
       "<br>"
       "ColoDetect is an application designed to make the process of colorectal health assessment more "
       "accessible. It helps individuals assess their risk of colorectal cancer by providing a user-friendly "
       "survey that takes various risk factors into account.<br>"
       "The application aims to raise awareness and promote early detection of colorectal cancer, ultimately "
       "contributing to better colorectal health outcomes.<br>"
   )
   return render_template('about.html', about_text=about_text)


def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
@app.route('/imaging', methods=['GET', 'POST'])
def imaging():
   if request.method == 'POST':
       if 'image' not in request.files:
           flash('No file part')
           return redirect(request.url)


       file = request.files['image']


       if file.filename == '':
           flash('No selected file')
           return redirect(request.url)


       if file and allowed_file(file.filename):
           filename = secure_filename(file.filename)
           filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
           file.save(filepath)


          
           time.sleep(5)
           flash('Analysis complete. No model was found.')


           return redirect(url_for('imaging'))


   return render_template('imaging.html')


@app.route('/calculate_risk', methods=['POST'])
def calculate_risk():
   age = request.form.get('age',0, type=int)
   family_history = request.form.get('family_history', 'no')
   personal_history = request.form.get('personal_history', 'no')
   dietary_habits = request.form.get('dietary_habits', 'healthy')
   physical_activity = request.form.get('physical_activity', 'regularly')
   obesity = request.form.get('obesity', 'no')
   smoking = request.form.get('smoking', 'no')
   alcohol_consumption = request.form.get('alcohol_consumption', 'low')
   ibd = request.form.get('ibd', 'no')
   type_2_diabetes = request.form.get('type_2_diabetes', 'no')
   genetic_factors = request.form.get('genetic_factors', 'no')
   screening_history = request.form.get('screening_history', 'yes')


   risk_score = 0


   if age > 50:
       risk_score += 20


   if family_history == 'yes':
       risk_score += 10


   if personal_history == 'yes':
       risk_score += 10


   if dietary_habits == 'unhealthy':
       risk_score += 10


   if physical_activity == 'rarely':
       risk_score += 10


   if obesity == 'yes':
       risk_score += 10


   if smoking == 'yes':
       risk_score += 10


   if alcohol_consumption == 'high':
       risk_score += 10


   if ibd == 'yes':
       risk_score += 10


   if type_2_diabetes == 'yes':
       risk_score += 10


   if genetic_factors == 'yes':
       risk_score += 10


   if screening_history == 'no':
       risk_score += 10


   risk_percentage = min(100, risk_score)  # Cap the risk at 100%


   message = f"Based on your responses, your estimated risk of colorectal cancer is approximately {risk_percentage}%."
 
   # return jsonify({
   #     'risk_percentage': risk_percentage,
   #     'message': f"Based on your responses, your estimated risk of colorectal cancer is approximately {risk_percentage}%."
   # })
   return render_template('result.html', message=message, risk_percentage=risk_percentage)


if __name__ == '__main__':
   app.run(debug=True)