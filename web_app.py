import numpy as np
import pandas as pd
import pickle
import streamlit as st


import json

# Open the file for reading
with open('./columns.json', 'r') as f:
    # Load the JSON data from the file
    data = json.load(f)

# get the columns from the json file 
columns = data['data_columns'] 

# get only the locations from the columns
locations = columns[3:]



model = pickle.load(open('trained_model.sav','rb'))

def predict_the_price(location,sqft,bath,bhk):

    location_index = columns.index(location)
    
    x = np.zeros(len(columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if location_index >= 0:
        x[location_index] = 1
    return model.predict([x])[0]

print(predict_the_price('1st phase jp nagar',1000,3,3))


def main():
    # styles 
    st.markdown("""
    <style>
    div.stButton > button:first-child {
    margin-left: auto;
    margin-right: auto;
    display: block;
    }
    </style>
    """, unsafe_allow_html=True)

    # title 
    inputed_values = []
    st.title('Bengaluru Price House Estimator')
    selected_location = st.selectbox('Select a location', locations)
    inputed_values.append(selected_location)

    selected_sqft = int(st.number_input('Enter the square footage'))
    inputed_values.append(selected_sqft)

    selected_bath = int(st.number_input('Enter number of baths'))
    inputed_values.append(selected_bath)

    selected_bhk = int(st.number_input('Enter number of Bedroom Hall Kitchen(e.g 2 BHK)'))
    inputed_values.append(selected_bhk)

    # Check if any of the values are empty
    if st.button('Estimate the Price'):
        if not all(inputed_values):
            st.warning("Please enter a value for all fields")
        else:
            prediction = predict_the_price(selected_location,selected_sqft,selected_bath,selected_bhk)
            st.write(f'<div style="text-align:center; font-weight:bold; background-color:green; padding:10px;">Estimated Price: {prediction}</div>',
                     unsafe_allow_html=True)



if __name__ =='__main__':
    main()