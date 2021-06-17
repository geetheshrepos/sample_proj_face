import os
import pandas as pd 
import numpy as np 
import flask
import pickle
import joblib
from flask import Flask, render_template, request
app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1,12)
    loaded_model = joblib.load(open('best_estimator_gnb-Copy1.sav','rb'))
    result = loaded_model.predict(to_predict)
    return result[0]
@app.route('/predict',methods = ['POST'])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list=list(to_predict_list.values())
        to_predict_list = list(map(int, to_predict_list))
        Phase = ValuePredictor(to_predict_list)
        def Type_connect(Ph):
            if Ph == 'Phase_1' or 'Phase' == 'Phase_2':
                val = 'Type_1'
            elif Ph == 'Phase_3' or 'Phase' == 'Phase_4' or 'Phase' == 'Phase_5' or 'Phase' == 'Phase_6' or 'Phase' == 'Phase_7':
                val = 'Type_2'
            elif Ph == 'Phase_8' or 'Phase' == 'Phase_9' or 'Phase' == 'Phase_10':
                val = 'Type_3'
            elif Ph == 'Phase_11' or 'Phase' == 'Phase_12':
                val = 'Type_4'
            else:
                val = 'random_type'
            return val

        Type_conn = Type_connect(Phase)

        def connect_article(T):
            if T == 'Type_1':
                cal =  ['A183','A111','A116','A166','A167','A173','A151','A137','A138','A139','A134'
                    ,'A181','A152','A142','A151','A153','A154','A160','A164','A182']

            elif T == 'Type_2':
                cal = ['A184','A163','A156','A149','A137','A138','A139','A134','A111','A116','A166',
                                'A167','A173','A151','A169','A126','A129','A172','A131','A165','A101','A100','A177',
                                'A104','A105','A103','A102','A106','A108','A178','A110','A124','A125','A180','A181',
                                'A152','A142','A151','A153','A154','A160','A164','A182']


            elif T == 'Type_3':
                cal = ['A185','A137','A138','A139','A134','A111','A116','A166','A167','A173','A151','A123','A179',
                                'A121','A119','A118','A122','A169','A126','A129','A172','A131','A165','A101','A100','A177','A104',
                                'A105','A103','A102','A106','A108','A178','A110','A124','A125','A180','A181','A152','A142','A151','A153',
                                'A154','A160','A164','A182']

            elif T == 'Type_4': 
                cal = ['A186','A123','A179','A121','A119','A118','A122','A101','A100','A177','A106','A108','A178','A110','A124','A125',
                       'A181','A152','A142','A151','A153','A154','A160','A164','A182']
            elif T == 'random_type':
                cal = ['A152','A142','A151','A153','A154','A160','A164','A182']
            return cal

        All_set = connect_article(Type_conn)

        def artcile_Recom(all_set_art, no_to_recom = 10):
            if len(all_set_art) < 10 or len(all_set_art) == 10 :
                val = all_set_art
            else:
                val =  random.sample(all_set_art, 10)
            return val    

        result = artcile_Recom(All_set)
        Phase_type = "Based on your response you are  in {Ph} and categorized to {ty} menopause. List of Recommended articles    are".format(Ph= Phase , ty = Type_conn)

        prediction = Phase_type + str(result)
    return render_template('predict.html',prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)