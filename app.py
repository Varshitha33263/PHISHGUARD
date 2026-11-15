
import streamlit as st
import pandas as pd
import joblib

model = joblib.load("phishing_model.pkl")

st.set_page_config(page_title="PHISHGUARD", page_icon="🛡️")

st.title("🛡️ PHISHGUARD")
st.subheader("Phishing URL Risk Classification")

st.write("Enter a website URL to check its phishing risk.")

url = st.text_input("Enter Website URL")

if st.button("Check URL"):
    if url.strip():

        features = pd.DataFrame([{
            'url_length': len(url),
            'dot_count': url.count('.'),
            'hyphen_count': url.count('-'),
            'at_count': url.count('@'),
            'digit_count': sum(c.isdigit() for c in url),
            'https': int(url.startswith('https://')),
            'slash_count': url.count('/')
        }])

        prediction = model.predict(features)[0]
        risk = model.predict_proba(features)[0][1] * 100

        if prediction == 1:
            st.error("Potentially Phishing Website!")
        else:
            st.success("Likely Legitimate Website")

        st.metric("Estimated Phishing Risk", f"{risk:.2f}%")
        st.caption("This is an ML-based estimate, not a guarantee of website safety.")

    else:
        st.warning("Please enter a URL.")
