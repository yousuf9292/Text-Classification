from flask import Flask,jsonify,request,session,redirect,url_for,render_template
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired,Length
import numpy as np
from keras.models import load_model
import joblib

def return_predictions(model,sample_text,tokenize_model):
    Text=sample_text["Text"]
    Text=[Text]
    classes=np.array(['Bussiness','Entartaiment','Sport','Tech'])
    test=tokenize.texts_to_matrix(Text)
    class_ind=model.predict_classes(test)[0]
    return classes[class_ind]



class Form(FlaskForm):
    text=StringField('Enter Text To Classify',validators=[DataRequired(message='Text is Required'),Length(min=10,message='Must me 10 character long')])


app=Flask(__name__)
app.config["SECRET_KEY"]="This is Secret"


@app.route('/',methods=['POST','GET'])
def form():
	form=Form()
	if form.validate_on_submit():
		session['Text']=form.text.data
		return redirect(url_for('predictions'))
	return render_template('form.html',form=form)

model=load_model('C:\\Users\\yousuf\\Text.h5')
tokenize=joblib.load('C:\\Users\\yousuf\\tokenize.pkl')


@app.route('/predictions')
def predictions():
	content={}

	content['Text']=session['Text']
	results=return_predictions(model,content,tokenize)
	return render_template('prediction.html',results=results,content=content)



@app.route('/api',methods=['POST'])
def prediction():
	context=request.json
	results=return_predictions(model,context,tokenize)
	return jsonify(results)

if __name__ == '__main__':
	app.run(debug=True)