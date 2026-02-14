import streamlit as st
import requests

st.set_page_config(layout="wide")
st.title("🧠 Enterprise ITSM AI Assistant")

user_input = st.text_area("Enter your request")

if st.button("Submit"):

    if not user_input.strip():
        st.warning("Please enter a request.")
    else:
        with st.spinner("Processing..."):
            try:
                response = requests.post(
                    "http://localhost:5000/chat",
                    json={"message": user_input}
                )

                if response.status_code != 200:
                    st.error("Server error.")
                    st.write(response.text)
                else:
                    result = response.json()

                    mode = result.get("mode")

                    if mode == "error":
                        st.error(result.get("error"))

                    elif mode == "analyze":
                        data = result.get("data", {})
                        st.success(f"Incident: {data.get('incident_number')}")
                        st.info(f"Category: {data.get('category')}")
                        st.markdown("## 📊 Analysis")
                        st.write(data.get("analysis"))

                    elif mode == "create":
                        st.success("Incident Created Successfully")
                        st.json(result.get("data"))

                    else:
                        st.warning("Unexpected response.")
                        st.json(result)

            except Exception as e:
                st.error(f"Connection failed: {e}")
