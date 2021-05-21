from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import BookRec
import pandas as pd
#import pickle
#import numpy as np
#import sklearn
#from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
CORS(app)


@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


#standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def recommend_books():
    if request.method == 'POST':
        book_title = request.form['Title']
         
        result = BookRec.results(book_title)
                
        return render_template('index.html',column_names=result.columns.values, row_data=list(result.values.tolist()), zip=zip)
        

if __name__=="__main__":
    app.run(debug=True)


