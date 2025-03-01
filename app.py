import streamlit as st
import pickle
import numpy as np

# Load the trained model
with open("Loan_Approval_Prediction.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# Streamlit UI
st.set_page_config(page_title="Loan Approval Prediction", layout="wide", page_icon="🏦")

# Add a header with a fancy title
st.title("🏦 Loan Approval Prediction")
st.markdown("""
    <style>
    .header {
        font-size: 32px;
        color: #1e1e1e;
        font-weight: bold;
    }
    .subheader {
        font-size: 20px;
        color: #555;
    }
    .prediction-text {
        font-size: 18px;
        font-weight: bold;
        color: #4CAF50;
    }
    </style>
""", unsafe_allow_html=True)

# Welcome message
st.markdown('<div class="subheader">Enter the details below to check loan approval status.</div>', unsafe_allow_html=True)

# Organize Inputs in Columns
col1, col2 = st.columns(2)

with col1:
    Married = st.selectbox("Married", ["No", "Yes"])
    Education = st.selectbox("Education", ["Graduate", "Not Graduate"])
    Dependents = st.selectbox('Dependents', ['Yes', 'No'])
    ApplicantIncome = st.number_input("Applicant Income (in thousands)", min_value=0)
    LoanAmount = st.number_input("Loan Amount (in thousands)", min_value=0)

with col2:
    if Dependents == 'No':
        CoapplicantIncome = 0
    else:
        CoapplicantIncome = st.number_input("Coapplicant Income (in thousands)", min_value=0)
    Loan_Amount_Term = st.selectbox("Loan Amount Term (Months)", [360, 180, 120, 60])
    Credit_History = st.selectbox("Credit History", [0.0, 1.0])
    property_area = st.selectbox('Property Area', ['Urban', 'Rural', 'Semi-Urban'])

# Convert categorical values
Married = 1 if Married == "Yes" else 0
Education = 1 if Education == "Graduate" else 0
Dependents = 1 if Dependents == "Yes" else 0
if property_area == 'Urban':
    property_area = 1
elif property_area == 'Semi-Urban':
    property_area = 2
else:
    property_area = 0

# Prepare input array
input_data = np.array([[Married, Education, Dependents, ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History, property_area]])

# Add a stylish button with hover effect
button = st.button("Predict", help="Click to check the loan approval status")

if button:
    prediction = model.predict(input_data)
    result = "Approved ✅" if prediction[0] == 1 else "Rejected ❌"

    # Display Result in a styled box
    st.markdown(f'<div class="prediction-text">{result}</div>', unsafe_allow_html=True)

    if result == "Approved ✅":
        st.markdown("Congratulations! Your loan is approved. 🎉")
    else:
        st.markdown("Unfortunately, your loan is not approved. 😞")

