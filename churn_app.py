# import streamlit as st
# import pandas as pd
# from joblib import load
# from sklearn.preprocessing import LabelEncoder

# # Load the trained Random Forest model
# model = load('random_forest_model.joblib')

# # Create a Streamlit app
# st.title("Customer Churn Prediction App")

# # Input fields for feature values on the main screen
# st.header("Enter Customer Information")
# tenure = st.number_input("Tenure (in months)", min_value=0, max_value=100, value=1)
# internet_service = st.selectbox("Internet Service", ('DSL', 'Fiber optic', 'No'))
# contract = st.selectbox("Contract", ('Month-to-month', 'One year', 'Two year'))
# monthly_charges = st.number_input("Monthly Charges", min_value=0, max_value=200, value=50)
# total_charges = st.number_input("Total Charges", min_value=0, max_value=10000, value=0)

# # Map input values to numeric using the label mapping
# label_mapping = {
#     'DSL': 0,
#     'Fiber optic': 1,
#     'No': 2,
#     'Month-to-month': 0,
#     'One year': 1,
#     'Two year': 2,
# }
# internet_service = label_mapping[internet_service]
# contract = label_mapping[contract]

# # Make a prediction using the model
# prediction = model.predict([[tenure, internet_service, contract, monthly_charges, total_charges]])

# # Display the prediction result on the main screen
# st.header("Prediction Result")
# if prediction[0] == 0:
#     st.success("This customer is likely to stay.")
# else:
#     st.error("This customer is likely to churn.")

# # Add any additional Streamlit components or UI elements as needed.

import streamlit as st
from joblib import load

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📉",
    layout="centered",
)

# ---------- SIMPLE CUSTOM CSS ----------
st.markdown(
    """
    <style>
        .main {
            padding-top: 2rem;
        }
        .churn-card {
            padding: 2rem 2.5rem;
            border-radius: 1rem;
            background-color: #111827;
            border: 1px solid #1f2933;
        }
        .stButton>button {
            border-radius: 999px;
            padding: 0.6rem 2rem;
            font-weight: 600;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- LOAD MODEL ----------
model = load("random_forest_model.joblib")

# ---------- SIDEBAR ----------
st.sidebar.title("About")
st.sidebar.write(
    """
    This app uses a trained Random Forest model  
    to predict whether a telecom customer is likely  
    to churn based on basic account information.
    """
)
st.sidebar.markdown("---")
st.sidebar.write("Made with Streamlit & scikit-learn.")

# ---------- HEADER ----------
st.markdown("### 📉 Customer Churn Prediction App")
st.markdown(
    "Use the form below to enter customer details and estimate whether the customer is likely to churn."
)

st.markdown("<div class='churn-card'>", unsafe_allow_html=True)

st.subheader("Enter Customer Information")

# ---------- INPUT FORM ----------
with st.form("churn_form"):
    col1, col2 = st.columns(2)

    with col1:
        tenure = st.number_input("Tenure (months)", min_value=0, max_value=100, value=12)
        monthly_charges = st.number_input(
            "Monthly Charges", min_value=0, max_value=200, value=50
        )
        total_charges = st.number_input(
            "Total Charges", min_value=0, max_value=10000, value=600
        )

    with col2:
        internet_service = st.selectbox(
            "Internet Service", ("DSL", "Fiber optic", "No")
        )
        contract = st.selectbox(
            "Contract Type", ("Month-to-month", "One year", "Two year")
        )

    submitted = st.form_submit_button("Predict churn")

st.markdown("</div>", unsafe_allow_html=True)

# ---------- PREDICTION ----------
if submitted:
    # manual mapping – must match training encodings
    label_mapping = {
        "DSL": 0,
        "Fiber optic": 1,
        "No": 2,
        "Month-to-month": 0,
        "One year": 1,
        "Two year": 2,
    }

    internet_service_num = label_mapping[internet_service]
    contract_num = label_mapping[contract]

    features = [[tenure, internet_service_num, contract_num,
                 monthly_charges, total_charges]]

    # class (0/1) and probability
    pred_class = model.predict(features)[0]
    proba = model.predict_proba(features)[0][pred_class] * 100

    st.markdown("### Prediction Result")

    if pred_class == 0:
        st.success(f"This customer is **likely to stay**. (Confidence ~{proba:.1f}%)")
    else:
        st.error(f"This customer is **likely to churn**. (Confidence ~{proba:.1f}%)")

    # small metrics row
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Tenure (months)", tenure)
    with m2:
        st.metric("Monthly Charges", monthly_charges)
    with m3:
        st.metric("Total Charges", total_charges)
