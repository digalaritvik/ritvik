import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Calculator",
    page_icon="🧮",
    layout="centered"
)

# Initialize session state for calculator
if 'display_value' not in st.session_state:
    st.session_state.display_value = "0"
if 'first_number' not in st.session_state:
    st.session_state.first_number = None
if 'operation' not in st.session_state:
    st.session_state.operation = None
if 'new_number' not in st.session_state:
    st.session_state.new_number = True

# Custom CSS for calculator styling
st.markdown("""
<style>
    .calculator-container {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        max-width: 400px;
        margin: 0 auto;
    }
    .calc-display {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 15px;
        text-align: right;
        font-size: 24px;
        min-height: 50px;
        color: black;
    }
    .stButton > button {
        width: 100%;
        margin-bottom: 5px;
        border-radius: 5px;
        font-size: 18px;
    }
    .number-button > button {
        background-color: #4CAF50;
        color: white;
    }
    .operator-button > button {
        background-color: #2196F3;
        color: white;
    }
    .clear-button > button {
        background-color: #f44336;
        color: white;
    }
    .equals-button > button {
        background-color: #FF9800;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Calculator functions
def update_display(value):
    st.session_state.display_value = value

def append_digit(digit):
    if st.session_state.new_number:
        update_display(str(digit))
        st.session_state.new_number = False
    else:
        if st.session_state.display_value == "0":
            update_display(str(digit))
        else:
            update_display(st.session_state.display_value + str(digit))

def clear_display():
    update_display("0")
    st.session_state.first_number = None
    st.session_state.operation = None
    st.session_state.new_number = True

def set_operation(op):
    if st.session_state.first_number is None:
        st.session_state.first_number = float(st.session_state.display_value)
    else:
        calculate_result()
    
    st.session_state.operation = op
    st.session_state.new_number = True

def calculate_result():
    if st.session_state.first_number is not None and st.session_state.operation is not None:
        second_number = float(st.session_state.display_value)
        
        if st.session_state.operation == "+":
            result = st.session_state.first_number + second_number
        elif st.session_state.operation == "-":
            result = st.session_state.first_number - second_number
        elif st.session_state.operation == "×":
            result = st.session_state.first_number * second_number
        elif st.session_state.operation == "÷":
            if second_number == 0:
                result = "Error"
            else:
                result = st.session_state.first_number / second_number
        
        if result == "Error":
            update_display("Error")
        else:
            # Format the result to avoid long decimal numbers
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            update_display(str(result))
        
        st.session_state.first_number = None
        st.session_state.operation = None
        st.session_state.new_number = True

# Main calculator UI
st.title("Calculator")

# Calculator container
with st.container():
    st.markdown('<div class="calculator-container">', unsafe_allow_html=True)
    
    # Display
    st.markdown(f'<div class="calc-display">{st.session_state.display_value}</div>', unsafe_allow_html=True)
    
    # Calculator buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="number-button">', unsafe_allow_html=True)
        if st.button("7", key="7"):
            append_digit(7)
        if st.button("4", key="4"):
            append_digit(4)
        if st.button("1", key="1"):
            append_digit(1)
        if st.button("0", key="0"):
            append_digit(0)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="number-button">', unsafe_allow_html=True)
        if st.button("8", key="8"):
            append_digit(8)
        if st.button("5", key="5"):
            append_digit(5)
        if st.button("2", key="2"):
            append_digit(2)
        if st.button(".", key="."):
            append_digit(".")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="number-button">', unsafe_allow_html=True)
        if st.button("9", key="9"):
            append_digit(9)
        if st.button("6", key="6"):
            append_digit(6)
        if st.button("3", key="3"):
            append_digit(3)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="clear-button">', unsafe_allow_html=True)
        if st.button("C", key="C"):
            clear_display()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="operator-button">', unsafe_allow_html=True)
        if st.button("÷", key="÷"):
            set_operation("÷")
        if st.button("×", key="×"):
            set_operation("×")
        if st.button("-", key="-"):
            set_operation("-")
        if st.button("+", key="+"):
            set_operation("+")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Equals button (full width)
    st.markdown('<div class="equals-button">', unsafe_allow_html=True)
    if st.button("=", key="="):
        calculate_result()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Add a small footer
st.markdown("---")
st.caption("A customizable calculator built with Streamlit") 