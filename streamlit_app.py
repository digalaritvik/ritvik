import streamlit as st
import pandas as pd

# Set page title
st.title("Interactive Dashboard")

# Add RGB sliders for custom color creation
st.sidebar.header("Background Color Settings")
st.sidebar.subheader("RGB Color Sliders")
red = st.sidebar.slider("Red", 0, 255, 255)
green = st.sidebar.slider("Green", 0, 255, 255)
blue = st.sidebar.slider("Blue", 0, 255, 255)

# Convert RGB to hex color
rgb_color = f"#{red:02x}{green:02x}{blue:02x}"

# Display the RGB color
st.sidebar.color_picker("RGB Color Result", rgb_color, disabled=True)

# Apply the RGB color as background using custom CSS
st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {rgb_color};
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Create sliders for number inputs
number1 = st.slider("Pick a number 1", 0, 1000)
st.write(number1)

number2 = st.slider("Pick a number 2", 0, 1000)
st.write(number2)

# Color picker
color = st.color_picker("Pick a color")

# Date input
date = st.date_input("Pick a date")

# Create sample dataframe
df = pd.DataFrame({
    "category": ["A", "B", "C"],
    "sales": [100, 150, 200]
})

# Display the dataframe
st.subheader("Sample Data")
st.dataframe(df)

# Plot the bar chart
st.subheader("Bar Chart")
st.bar_chart(df, x="category", y="sales")

# Calculator UI
st.subheader("Calculator")
col1, col2, col3, col4 = st.columns(4)

with col1:
    add_button = st.button("Add (+)")
with col2:
    subtract_button = st.button("Subtract (-)")
with col3:
    multiply_button = st.button("Multiply (×)")
with col4:
    divide_button = st.button("Divide (÷)")

# Perform calculations based on button clicks
result = None
operation = ""

if add_button:
    result = number1 + number2
    operation = "addition"
elif subtract_button:
    result = number1 - number2
    operation = "subtraction"
elif multiply_button:
    result = number1 * number2
    operation = "multiplication"
elif divide_button:
    if number2 != 0:
        result = number1 / number2
        operation = "division"
    else:
        st.error("Cannot divide by zero!")

# Display calculation result
if result is not None:
    st.success(f"Result of {operation}: {number1} {'+' if operation == 'addition' else '-' if operation == 'subtraction' else '×' if operation == 'multiplication' else '÷'} {number2} = {result}")

# Add some interactivity based on the selected values
st.subheader("Interactive Results")
st.write(f"You selected numbers: {number1} and {number2}")
st.write(f"You selected color: {color}")
st.write(f"You selected date: {date}")
st.write(f"Background RGB Color: {rgb_color}")

# Calculate and display the sum of the selected numbers
sum_result = number1 + number2
st.write(f"The sum of your selected numbers is: {sum_result}") 