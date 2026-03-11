from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import traceback
import os

app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": os.environ.get("EXPRESS_BACKEND_URL", "http://localhost:4000")}})

# Load dataset
df = pd.read_csv("APEAPCET2023LASTRANKDETAILS.csv")

# Columns used in training
category_columns = [
    'OC_BOYS', 'OC_GIRLS', 'SC_BOYS', 'SC_GIRLS', 'BCA_BOYS', 'BCA_GIRLS',
    'BCB_BOYS', 'BCB_GIRLS', 'BCC_BOYS', 'BCC_GIRLS', 'BCD_BOYS', 'BCD_GIRLS',
    'BCE_BOYS', 'BCE_GIRLS', 'OC_EWS_BOYS', 'OC_EWS_GIRLS', 'ST_BOYS', 'ST_GIRLS'
]
numeric_columns = ['COLLEGE FEE'] + category_columns
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce').fillna(0)

# Encode categorical columns
label_encoders = {}
categorical_columns = ['INSTCODE', 'NAME OF THE INSTITUTION', 'INST_REG', 'BRANCH_CODE', 'TYPE']
for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    label_encoders[col] = le

# Prepare features and model
features = df[['BRANCH_CODE', 'INST_REG'] + category_columns]
targets = df[['INSTCODE', 'NAME OF THE INSTITUTION', 'COLLEGE FEE', 'TYPE']]
model = RandomForestRegressor(random_state=42, n_estimators=100)
model.fit(features, targets)

@app.route('/')
def home():
    return "✅ ML Model API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print("📥 Received request:", data)

        # Validate and extract input
        required_fields = ['rank', 'category_gender', 'branch_code', 'inst_reg']
        for field in required_fields:
            if field not in data or data[field] is None or str(data[field]).strip() == "":
                return jsonify({'error': f"Missing or empty field: {field}"}), 400

        person_rank = int(data['rank'])
        category_gender = data['category_gender'].strip().upper()
        branch_code = data['branch_code'].strip().upper()
        inst_reg = data['inst_reg'].strip().upper()

        if category_gender not in [col.upper() for col in category_columns]:
            return jsonify({'error': 'Invalid category_gender value'}), 400

        # Encode inputs
        try:
            branch_code_encoded = label_encoders['BRANCH_CODE'].transform([branch_code])[0]
            inst_reg_encoded = label_encoders['INST_REG'].transform([inst_reg])[0]
        except Exception as e:
            return jsonify({'error': f'Invalid branch_code or inst_reg: {str(e)}'}), 400

        input_data = [branch_code_encoded, inst_reg_encoded] + [0] * len(category_columns)
        category_index = [col.upper() for col in category_columns].index(category_gender)
        input_data[category_index + 2] = person_rank

        # Predict
        prediction = model.predict([input_data])
        df['PREDICTED_DISTANCE'] = np.linalg.norm(targets - prediction, axis=1)
        top = df.nsmallest(2, 'PREDICTED_DISTANCE')

        result = []
        for _, row in top.iterrows():
            result.append({
                "INSTCODE": label_encoders['INSTCODE'].inverse_transform([int(round(row['INSTCODE']))])[0],
                "NAME": label_encoders['NAME OF THE INSTITUTION'].inverse_transform([int(round(row['NAME OF THE INSTITUTION']))])[0],
                "FEE": int(round(row['COLLEGE FEE'])),
                "TYPE": label_encoders['TYPE'].inverse_transform([int(round(row['TYPE']))])[0]
            })

        return jsonify({"result": result})
    
    except Exception as e:
        print("❌ Flask error:\n", traceback.format_exc())
        return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
