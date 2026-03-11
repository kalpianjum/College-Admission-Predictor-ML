import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# Load the CSV file
csv_file = r"C:\Users\kalpi\OneDrive\Desktop\project\APEAPCET2023LASTRANKDETAILS.csv"

if not os.path.exists(csv_file):
    print(f"File not found: {csv_file}")
else:
    # Load the dataset
    df = pd.read_csv(csv_file)

    # Replace non-numeric values in numeric columns with NaN
    numeric_columns = ['COLLEGE FEE'] + [
        'OC_BOYS', 'OC_GIRLS', 'SC_BOYS', 'SC_GIRLS', 'BCA_BOYS', 'BCA_GIRLS',
        'BCB_BOYS', 'BCB_GIRLS', 'BCC_BOYS', 'BCC_GIRLS', 'BCD_BOYS', 'BCD_GIRLS',
        'BCE_BOYS', 'BCE_GIRLS', 'OC_EWS_BOYS', 'OC_EWS_GIRLS'
    ]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert non-numeric to NaN

    # Fill missing values for numeric columns with 0
    df.fillna(0, inplace=True)

    # Encode categorical columns
    label_encoders = {}
    categorical_columns = ['INSTCODE', 'NAME OF THE INSTITUTION', 'INST_REG', 'BRANCH_CODE']
    for col in categorical_columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        label_encoders[col] = le

    # Features and target preparation
    category_columns = [
        'OC_BOYS', 'OC_GIRLS', 'SC_BOYS', 'SC_GIRLS', 'BCA_BOYS', 'BCA_GIRLS',
        'BCB_BOYS', 'BCB_GIRLS', 'BCC_BOYS', 'BCC_GIRLS', 'BCD_BOYS', 'BCD_GIRLS',
        'BCE_BOYS', 'BCE_GIRLS', 'OC_EWS_BOYS', 'OC_EWS_GIRLS'
    ]
    target_columns = ['INSTCODE', 'NAME OF THE INSTITUTION', 'INST_REG', 'COLLEGE FEE']

    # Features: category columns + branch_code + person_rank
    features = df[['BRANCH_CODE'] + category_columns]
    targets = df[target_columns]

    # Train the model
    model = RandomForestRegressor(random_state=42, n_estimators=100)
    model.fit(features, targets)

    # Prediction function
    def predict_institution(person_rank, category_gender, branch_code):
        if category_gender not in category_columns:
            raise ValueError(f"Invalid category_gender: {category_gender}. Must be one of {category_columns}")

        # Encode branch_code
        branch_code_encoded = label_encoders['BRANCH_CODE'].transform([branch_code])[0]

        # Prepare input data
        input_data = [branch_code_encoded] + [0] * len(category_columns)
        category_index = category_columns.index(category_gender)
        input_data[category_index + 1] = person_rank  # Add person_rank to the correct category

        # Predict using the model
        prediction = model.predict([input_data])[0]

        # Decode results
        decoded_results = {
            'INSTCODE': label_encoders['INSTCODE'].inverse_transform([int(round(prediction[0]))])[0],
            'NAME OF THE INSTITUTION': label_encoders['NAME OF THE INSTITUTION'].inverse_transform([int(round(prediction[1]))])[0],
            'INST_REG': label_encoders['INST_REG'].inverse_transform([int(round(prediction[2]))])[0],
            'COLLEGE FEE': int(round(prediction[3]))
        }
        return decoded_results

    # Take inputs from user
    person_rank = int(input("Enter person rank: "))
    category_gender = input(f"Enter category_gender (options: {', '.join(category_columns)}): ")
    branch_code = input("Enter branch code: ")

    # Predict and display results
    try:
        result = predict_institution(person_rank, category_gender, branch_code)
        print("Predicted Results:")
        for key, value in result.items():
            print(f"{key}: {value}")
    except Exception as e:
        print(f"Error occurred: {e}")
