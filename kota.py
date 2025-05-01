import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
import string
import datetime

# Set page configuration
st.set_page_config(
    page_title="GRIET Library Management System",
    page_icon="📚",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("📚 GRIET Library Management System")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Data Analysis", "Visualization", "Reports"])

# Main content
if page == "Home":
    st.header("Welcome to GRIET Library")
    st.write("This dashboard provides access to the GRIET Library Management System.")
    
elif page == "Data Analysis":
    st.header("Library Data Analysis")
    st.write("Perform data analysis here.")
    
elif page == "Visualization":
    st.header("Library Data Visualization")
    st.write("Create visualizations here.")
    
elif page == "Reports":
    st.header("Library Reports")
    st.write("Generate and view reports here.")

# Footer
st.markdown("---")
st.caption("© 2024 GRIET Library Management System")

# Update POPULAR_BOOKS with Indian Rupee prices
POPULAR_BOOKS = [
    {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "category": "Fiction",
        "language": "English",
        "price": 499.00,
        "cover_url": "https://m.media-amazon.com/images/I/71FxgtFKcQL.AC_UF1000,1000_QL80.jpg"
    },
    {
        "title": "1984",
        "author": "George Orwell",
        "category": "Fiction",
        "language": "English",
        "price": 399.00,
        "cover_url": "https://m.media-amazon.com/images/I/71kxa1-0mfL.AC_UF1000,1000_QL80.jpg"
    },
    {
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "category": "Fiction",
        "language": "English",
        "price": 299.00,
        "cover_url": "https://m.media-amazon.com/images/I/71aFt4+OTOL.AC_UF1000,1000_QL80.jpg"
    },
    {
        "title": "Brief History of Time",
        "author": "Stephen Hawking",
        "category": "Science",
        "language": "English",
        "price": 599.00,
        "cover_url": "https://m.media-amazon.com/images/I/A1xkFZX5k-L.AC_UF1000,1000_QL80.jpg"
    },
    {
        "title": "The Power of Habit",
        "author": "Charles Duhigg",
        "category": "Psychology",
        "language": "English",
        "price": 449.00,
        "cover_url": "https://m.media-amazon.com/images/I/71QKQ9mwV7L.AC_UF1000,1000_QL80.jpg"
    },
    {
        "title": "Wings of Fire",
        "author": "APJ Abdul Kalam",
        "category": "Biography",
        "language": "English",
        "price": 249.00,
        "cover_url": "https://m.media-amazon.com/images/I/71KKZlVjbwL.AC_UF1000,1000_QL80.jpg"
    },
    {
        "title": "Zero to One",
        "author": "Peter Thiel",
        "category": "Business",
        "language": "English",
        "price": 549.00,
        "cover_url": "https://m.media-amazon.com/images/I/71m-MxdJ2WL.AC_UF1000,1000_QL80.jpg"
    },
    {
        "title": "Sapiens",
        "author": "Yuval Noah Harari",
        "category": "History",
        "language": "English",
        "price": 699.00,
        "cover_url": "https://m.media-amazon.com/images/I/71N3-FFSDxL.AC_UF1000,1000_QL80.jpg"
    },
    {
        "title": "The Art of War",
        "author": "Sun Tzu",
        "category": "Philosophy",
        "language": "English",
        "price": 199.00,
        "cover_url": "https://m.media-amazon.com/images/I/71KM8RhcgbL.AC_UF1000,1000_QL80.jpg"
    },
    {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "category": "Technology",
        "language": "English",
        "price": 799.00,
        "cover_url": "https://m.media-amazon.com/images/I/41xShlnTZTL.AC_UF1000,1000_QL80.jpg"
    }
]

# Update PRICE_RANGES to use Indian Rupees
PRICE_RANGES = [
    (0, 200, "Under ₹200"),
    (200, 400, "₹200 - ₹400"),
    (400, 600, "₹400 - ₹600"),
    (600, 800, "₹600 - ₹800"),
    (800, 1000, "₹800 - ₹1000"),
    (1000, float('inf'), "Over ₹1000")
]

# Update the price display in the book cards
with col3:
    st.markdown(f"Price: ₹{book['price']:.2f}")
    st.markdown(f"Available: {book['available']}/{book['quantity']}")
    if book['available'] > 0:
        if st.button("Borrow", key=f"borrow_{book['id']}"):
            # Add borrowing record
            borrowing = {
                "id": ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)),
                "book_id": book["id"],
                "book_title": book["title"],
                "username": st.session_state.username,
                "borrow_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "return_date": None,
                "price": book["price"]
            }
            st.session_state.borrowings.append(borrowing)
            save_borrowings()

            # Add transaction record
            transaction = {
                "id": ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)),
                "type": "borrow",
                "book_id": book["id"],
                "book_title": book["title"],
                "username": st.session_state.username,
                "amount": book["price"],
                "date": datetime.datetime.now().strftime("%Y-%m-%d")
            }
            st.session_state.transactions.append(transaction)
            save_transactions()

            # Update book availability
            book["available"] -= 1
            save_books()

            st.success(f"Book '{book['title']}' borrowed successfully! Amount: ₹{book['price']:.2f}")
            st.rerun()
    else:
        st.markdown("Out of Stock") 