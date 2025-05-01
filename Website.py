import streamlit as st

number1 = st.slider("Pick a number 1", 0, 1000)
number2 = st.slider("Pick a number 2", 0, 1000)

sum_result = number1 + number2
st.write(f"The sum of your selected numbers is: {sum_result}")

# Add a file uploader
uploaded_file = st.file_uploader("Pick a file") 