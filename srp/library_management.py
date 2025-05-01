import streamlit as st
import pandas as pd
import datetime
import json
import os
import hashlib
import random
import string

# Initialize session state variables
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'users' not in st.session_state:
    st.session_state.users = {}
if 'books' not in st.session_state:
    st.session_state.books = []
if 'borrowings' not in st.session_state:
    st.session_state.borrowings = []

# File paths
USERS_FILE = "srp/users.json"
BOOKS_FILE = "srp/books.json"
BORROWINGS_FILE = "srp/borrowings.json"

# Set page configuration
st.set_page_config(
    page_title="GRIET Library Management System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Main background and container styling */
    .stApp {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        color: #ffffff;
    }
    
    /* Book card styling */
    .book-card {
        background: rgba(51, 51, 51, 0.8);
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    
    .book-card:hover {
        transform: translateY(-5px);
    }
    
    .book-card img {
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    /* Override Streamlit's default white background */
    .st-bx {
        background-color: transparent;
    }
    
    .st-emotion-cache-1y4p8pa {
        background-color: #1a1a1a !important;
    }

    /* Fix for white background in main content */
    .st-emotion-cache-18ni7ap {
        background-color: #1a1a1a !important;
    }

    .st-emotion-cache-r421ms {
        background-color: #1a1a1a !important;
    }

    /* Input field styling */
    input[type="text"], 
    input[type="password"],
    input[type="number"],
    input[type="email"],
    textarea,
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        background-color: #333333 !important;
        color: #ffffff !important;
        border: 1px solid #4a4a4a !important;
        border-radius: 4px !important;
        padding: 8px 12px !important;
    }

    /* Selectbox styling */
    .stSelectbox > div > div > div {
        background-color: #333333 !important;
        color: #ffffff !important;
        border: 1px solid #4a4a4a !important;
    }

    /* Selectbox dropdown styling */
    .stSelectbox > div > div > div:hover {
        border-color: #0D47A1 !important;
    }

    /* Multiselect styling */
    .stMultiSelect > div > div > div {
        background-color: #333333 !important;
        color: #ffffff !important;
        border: 1px solid #4a4a4a !important;
    }

    /* DataFrame styling */
    .dataframe {
        background-color: #333333 !important;
        color: #ffffff !important;
    }

    .dataframe th {
        background-color: #0D47A1 !important;
        color: #ffffff !important;
    }

    .dataframe td {
        background-color: #333333 !important;
        color: #ffffff !important;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #0D47A1 0%, #1565C0 100%) !important;
        color: #ffffff !important;
        border: none !important;
        padding: 8px 16px !important;
        border-radius: 4px !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #1565C0 0%, #1976D2 100%) !important;
        border: none !important;
    }

    /* Header styling */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }

    /* Text styling */
    p, span, div, label {
        color: #ffffff !important;
    }

    /* Link styling */
    a {
        color: #64B5F6 !important;
    }

    a:hover {
        color: #90CAF9 !important;
    }

    /* Sidebar styling */
    .css-1d391kg, .css-12oz5g7 {
        background-color: #1a1a1a !important;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #333333 !important;
        padding: 10px !important;
        border-radius: 4px !important;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #4a4a4a !important;
        border-radius: 4px !important;
        margin-right: 4px !important;
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #0D47A1 0%, #1565C0 100%) !important;
        border: none !important;
    }

    /* Success/Info/Error/Warning message styling */
    .stSuccess, .stInfo, .stError, .stWarning {
        background-color: #333333 !important;
        color: #ffffff !important;
        padding: 16px !important;
        border-radius: 4px !important;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #333333 !important;
        color: #ffffff !important;
        border: 1px solid #4a4a4a !important;
        border-radius: 4px !important;
    }

    /* Radio button styling */
    .stRadio > div {
        color: #ffffff !important;
    }

    /* Checkbox styling */
    .stCheckbox > div {
        color: #ffffff !important;
    }

    /* Metric styling */
    .stMetric {
        background-color: #333333 !important;
        color: #ffffff !important;
    }

    /* Progress bar styling */
    .stProgress > div > div > div {
        background-color: #0D47A1 !important;
    }

    /* File uploader styling */
    .stFileUploader > div {
        background-color: #333333 !important;
        color: #ffffff !important;
        border: 1px solid #4a4a4a !important;
        border-radius: 4px !important;
    }

    /* Override any remaining white backgrounds */
    div[data-testid="stAppViewContainer"], 
    div[data-testid="stHeader"],
    section[data-testid="stSidebar"] {
        background-color: #1a1a1a !important;
    }
</style>
""", unsafe_allow_html=True)

# Predefined datasets
BOOK_CATEGORIES = [
    "Fiction",
    "Non-Fiction",
    "Science",
    "Technology",
    "History",
    "Biography",
    "Business",
    "Arts",
    "Literature",
    "Philosophy",
    "Psychology",
    "Education",
    "Reference",
    "Children",
    "Comics",
    "Poetry",
    "Drama",
    "Religion",
    "Social Science",
    "Travel"
]

BOOK_LANGUAGES = [
    "English",
    "Hindi",
    "Telugu",
    "Tamil",
    "Malayalam",
    "Kannada",
    "Bengali",
    "Marathi",
    "Gujarati",
    "Urdu",
    "Sanskrit"
]

POPULAR_BOOKS = [
    {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "category": "Fiction",
        "language": "English",
        "price": 1078.00,  # 12.99 USD * 83
        "cover_url": "https://m.media-amazon.com/images/I/71FxgtFKcQL._AC_UF1000,1000_QL80_.jpg"
    },
    {
        "title": "1984",
        "author": "George Orwell",
        "category": "Fiction",
        "language": "English",
        "price": 912.00,  # 10.99 USD * 83
        "cover_url": "https://m.media-amazon.com/images/I/71kxa1-0mfL._AC_UF1000,1000_QL80_.jpg"
    },
    {
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "category": "Fiction",
        "language": "English",
        "price": 995.00,  # 11.99 USD * 83
        "cover_url": "https://m.media-amazon.com/images/I/71aFt4+OTOL._AC_UF1000,1000_QL80_.jpg"
    },
    {
        "title": "Brief History of Time",
        "author": "Stephen Hawking",
        "category": "Science",
        "language": "English",
        "price": 1244.00,  # 14.99 USD * 83
        "cover_url": "https://m.media-amazon.com/images/I/A1xkFZX5k-L._AC_UF1000,1000_QL80_.jpg"
    },
    {
        "title": "The Power of Habit",
        "author": "Charles Duhigg",
        "category": "Psychology",
        "language": "English",
        "price": 1161.00,  # 13.99 USD * 83
        "cover_url": "https://m.media-amazon.com/images/I/71QKQ9mwV7L._AC_UF1000,1000_QL80_.jpg"
    },
    {
        "title": "Wings of Fire",
        "author": "APJ Abdul Kalam",
        "category": "Biography",
        "language": "English",
        "price": 829.00,  # 9.99 USD * 83
        "cover_url": "https://m.media-amazon.com/images/I/71KKZlVjbwL._AC_UF1000,1000_QL80_.jpg"
    },
    {
        "title": "Zero to One",
        "author": "Peter Thiel",
        "category": "Business",
        "language": "English",
        "price": 1327.00,  # 15.99 USD * 83
        "cover_url": "https://m.media-amazon.com/images/I/71m-MxdJ2WL._AC_UF1000,1000_QL80_.jpg"
    },
    {
        "title": "Sapiens",
        "author": "Yuval Noah Harari",
        "category": "History",
        "language": "English",
        "price": 1410.00,  # 16.99 USD * 83
        "cover_url": "https://m.media-amazon.com/images/I/71N3-FFSDxL._AC_UF1000,1000_QL80_.jpg"
    },
    {
        "title": "The Art of War",
        "author": "Sun Tzu",
        "category": "Philosophy",
        "language": "English",
        "price": 746.00,  # 8.99 USD * 83
        "cover_url": "https://m.media-amazon.com/images/I/71KM8RhcgbL._AC_UF1000,1000_QL80_.jpg"
    },
    {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "category": "Technology",
        "language": "English",
        "price": 1659.00,  # 19.99 USD * 83
        "cover_url": "https://m.media-amazon.com/images/I/41xShlnTZTL._AC_UF1000,1000_QL80_.jpg"
    }
]

# Initialize custom datasets in session state
if 'custom_categories' not in st.session_state:
    st.session_state.custom_categories = list(set([book["category"] for book in POPULAR_BOOKS]))
if 'custom_languages' not in st.session_state:
    st.session_state.custom_languages = list(set([book["language"] for book in POPULAR_BOOKS]))
if 'custom_authors' not in st.session_state:
    st.session_state.custom_authors = list(set([book["author"] for book in POPULAR_BOOKS]))
if 'custom_books' not in st.session_state:
    st.session_state.custom_books = POPULAR_BOOKS.copy()

PRICE_RANGES = [
    (0, 10, "Under $10"),
    (10, 20, "$10 - $20"),
    (20, 30, "$20 - $30"),
    (30, 50, "$30 - $50"),
    (50, 100, "$50 - $100"),
    (100, float('inf'), "Over $100")
]

# Helper functions
def load_data():
    """Load data from JSON files"""
    # Create srp directory if it doesn't exist
    os.makedirs("srp", exist_ok=True)
    
    # Load users
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            st.session_state.users = json.load(f)
    else:
        # Create default admin user
        st.session_state.users = {
            "admin": {
                "password": hashlib.sha256("admin123".encode()).hexdigest(),
                "is_admin": True,
                "name": "Administrator"
            }
        }
        save_users()
    
    # Load books
    if os.path.exists(BOOKS_FILE) and os.path.getsize(BOOKS_FILE) > 0:
        with open(BOOKS_FILE, 'r') as f:
            st.session_state.books = json.load(f)
    else:
        st.session_state.books = []
        # Initialize with sample books if empty
        for book in POPULAR_BOOKS:
            new_book = {
                "id": generate_book_id(),
                "title": book["title"],
                "author": book["author"],
                "category": book["category"],
                "language": book["language"],
                "price": book["price"],
                "quantity": random.randint(1, 10),
                "available": random.randint(1, 10),
                "description": f"A {book['category']} book by {book['author']}",
                "cover_url": book["cover_url"]
            }
            new_book["available"] = min(new_book["available"], new_book["quantity"])
            st.session_state.books.append(new_book)
        save_books()
    
    # Load borrowings
    if os.path.exists(BORROWINGS_FILE):
        with open(BORROWINGS_FILE, 'r') as f:
            st.session_state.borrowings = json.load(f)
    else:
        st.session_state.borrowings = []
        save_borrowings()
    
    # Update session state with custom datasets
    st.session_state.custom_categories = list(set([book["category"] for book in st.session_state.books] + [book["category"] for book in POPULAR_BOOKS]))
    st.session_state.custom_languages = list(set([book["language"] for book in st.session_state.books] + [book["language"] for book in POPULAR_BOOKS]))
    st.session_state.custom_authors = list(set([book["author"] for book in st.session_state.books] + [book["author"] for book in POPULAR_BOOKS]))
    st.session_state.custom_books = POPULAR_BOOKS.copy()
    
    st.session_state.initialized = True

def save_users():
    """Save users to JSON file"""
    with open(USERS_FILE, 'w') as f:
        json.dump(st.session_state.users, f)

def save_books():
    """Save books to JSON file"""
    with open(BOOKS_FILE, 'w') as f:
        json.dump(st.session_state.books, f)

def save_borrowings():
    """Save borrowings to JSON file"""
    with open(BORROWINGS_FILE, 'w') as f:
        json.dump(st.session_state.borrowings, f)

def generate_book_id():
    """Generate a unique book ID"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def hash_password(password):
    """Hash a password for storage"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed_password):
    """Verify a password against its hash"""
    return hash_password(password) == hashed_password

# Load data on startup if not initialized
if not st.session_state.initialized:
    load_data()

# Main UI
st.markdown('<h1 class="main-header">📚 GRIET Library Management System</h1>', unsafe_allow_html=True)

# Login/Register section
if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.markdown('<h2 class="sub-header">Login</h2>', unsafe_allow_html=True)
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            if login_username in st.session_state.users:
                if verify_password(login_password, st.session_state.users[login_username]["password"]):
                    st.session_state.logged_in = True
                    st.session_state.username = login_username
                    st.session_state.is_admin = st.session_state.users[login_username].get("is_admin", False)
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Incorrect password!")
            else:
                st.error("User not found!")
    
    with tab2:
        st.markdown('<h2 class="sub-header">Register</h2>', unsafe_allow_html=True)
        reg_username = st.text_input("Username", key="reg_username")
        reg_password = st.text_input("Password", type="password", key="reg_password")
        reg_confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm_password")
        reg_name = st.text_input("Full Name", key="reg_name")
        
        if st.button("Register"):
            if reg_username and reg_password and reg_confirm_password and reg_name:
                if reg_password != reg_confirm_password:
                    st.error("Passwords do not match!")
                elif reg_username in st.session_state.users:
                    st.error("Username already exists!")
                else:
                    st.session_state.users[reg_username] = {
                        "password": hash_password(reg_password),
                        "is_admin": False,
                        "name": reg_name
                    }
                    save_users()
                    st.success("Registration successful! Please login.")
            else:
                st.error("Please fill all fields!")

# Main application after login
else:
    # Sidebar with user info and logout
    with st.sidebar:
        st.markdown(f"### Welcome, {st.session_state.username}")
        st.markdown(f"**Role:** {'Administrator' if st.session_state.is_admin else 'User'}")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.is_admin = False
            st.rerun()
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs(["Browse Books", "Borrow/Return", "Admin Panel"])
    
    # Browse Books tab
    with tab1:
        st.markdown('<h2 class="sub-header">Browse Books</h2>', unsafe_allow_html=True)
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            categories = ["All"] + sorted(list(set([book["category"] for book in st.session_state.books] + BOOK_CATEGORIES)))
            selected_category = st.selectbox("Category", categories)
        
        with col2:
            languages = ["All"] + sorted(list(set([book["language"] for book in st.session_state.books] + BOOK_LANGUAGES)))
            selected_language = st.selectbox("Language", languages)
        
        with col3:
            search_query = st.text_input("Search by title or author")
        
        # Filter books
        filtered_books = st.session_state.books
        if selected_category != "All":
            filtered_books = [book for book in filtered_books if book["category"] == selected_category]
        if selected_language != "All":
            filtered_books = [book for book in filtered_books if book["language"] == selected_language]
        if search_query:
            search_query = search_query.lower()
            filtered_books = [book for book in filtered_books 
                             if search_query in book["title"].lower() or 
                                search_query in book["author"].lower()]
        
        # Display books
        if filtered_books:
            for book in filtered_books:
                with st.container():
                    st.markdown('<div class="book-card">', unsafe_allow_html=True)
                    col1, col2, col3 = st.columns([1, 2, 1])
                    
                    with col1:
                        if book.get('cover_url'):
                            st.image(book['cover_url'], width=150)
                        else:
                            st.image("https://via.placeholder.com/150x200?text=No+Cover", width=150)
                    
                    with col2:
                        st.markdown(f"### {book['title']}")
                        st.markdown(f"**Author:** {book['author']}")
                        st.markdown(f"**Category:** {book['category']}")
                        st.markdown(f"**Language:** {book['language']}")
                        if book.get('description'):
                            st.markdown(f"**Description:** {book['description']}")
                    
                    with col3:
                        st.markdown(f"**Price:** ₹{book['price']:.2f}")
                        st.markdown(f"**Available:** {book['available']} of {book['quantity']}")
                        if book['available'] > 0:
                            if st.button("Borrow", key=f"borrow_{book['id']}"):
                                # Add borrowing record
                                borrowing = {
                                    "id": ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)),
                                    "book_id": book["id"],
                                    "book_title": book["title"],
                                    "username": st.session_state.username,
                                    "borrow_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                                    "return_date": None
                                }
                                st.session_state.borrowings.append(borrowing)
                                save_borrowings()
                                
                                # Update book availability
                                book["available"] -= 1
                                save_books()
                                
                                st.success(f"Book '{book['title']}' borrowed successfully!")
                                st.rerun()
                        else:
                            st.markdown("**Out of Stock**")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No books found matching your criteria.")
    
    # Borrow/Return tab
    with tab2:
        st.markdown('<h2 class="sub-header">My Borrowings</h2>', unsafe_allow_html=True)
        
        # Filter borrowings for current user
        user_borrowings = [b for b in st.session_state.borrowings if b["username"] == st.session_state.username]
        
        if user_borrowings:
            for borrowing in user_borrowings:
                with st.container():
                    st.markdown('<div class="book-card">', unsafe_allow_html=True)
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.markdown(f"**{borrowing['book_title']}**")
                        st.markdown(f"**Borrowed on:** {borrowing['borrow_date']}")
                    
                    with col2:
                        if borrowing['return_date']:
                            st.markdown(f"**Returned on:** {borrowing['return_date']}")
                        else:
                            st.markdown("**Status:** Borrowed")
                    
                    with col3:
                        if not borrowing['return_date']:
                            if st.button("Return", key=f"return_{borrowing['id']}"):
                                # Update borrowing record
                                borrowing["return_date"] = datetime.datetime.now().strftime("%Y-%m-%d")
                                
                                # Update book availability
                                for book in st.session_state.books:
                                    if book["id"] == borrowing["book_id"]:
                                        book["available"] += 1
                                        break
                                
                                save_books()
                                save_borrowings()
                                
                                st.success(f"Book '{borrowing['book_title']}' returned successfully!")
                                st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("You haven't borrowed any books yet.")
    
    # Admin Panel tab
    with tab3:
        if st.session_state.is_admin:
            st.markdown('<h2 class="sub-header">Admin Panel</h2>', unsafe_allow_html=True)
            
            admin_tab1, admin_tab2, admin_tab3 = st.tabs(["Add Book", "Manage Books", "View All Borrowings"])
            
            # Add Book tab
            with admin_tab1:
                st.markdown('<h3>Add New Book</h3>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    new_title = st.text_input("Title")
                    new_author = st.text_input("Author")
                    new_category = st.selectbox("Category", BOOK_CATEGORIES)
                    new_language = st.selectbox("Language", BOOK_LANGUAGES)
                
                with col2:
                    new_price = st.number_input("Price (₹)", min_value=0.0, step=100.0, format="%.2f")
                    new_quantity = st.number_input("Quantity", min_value=1, step=1)
                    new_description = st.text_area("Description")
                
                if st.button("Add Book"):
                    if new_title and new_author and new_price > 0 and new_quantity > 0:
                        new_book = {
                            "id": generate_book_id(),
                            "title": new_title,
                            "author": new_author,
                            "category": new_category,
                            "language": new_language,
                            "price": new_price,
                            "quantity": new_quantity,
                            "available": new_quantity,
                            "description": new_description,
                            "cover_url": ""
                        }
                        
                        st.session_state.books.append(new_book)
                        save_books()
                        
                        st.success(f"Book '{new_title}' added successfully!")
                    else:
                        st.error("Please fill all required fields!")
            
            # Manage Books tab
            with admin_tab2:
                st.markdown('<h3>Manage Books</h3>', unsafe_allow_html=True)
                
                if st.session_state.books:
                    for book in st.session_state.books:
                        with st.expander(f"{book['title']} by {book['author']}"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                edited_title = st.text_input("Title", book["title"], key=f"edit_title_{book['id']}")
                                edited_author = st.text_input("Author", book["author"], key=f"edit_author_{book['id']}")
                                edited_category = st.selectbox("Category", BOOK_CATEGORIES, 
                                                             index=BOOK_CATEGORIES.index(book["category"]),
                                                             key=f"edit_category_{book['id']}")
                                edited_language = st.selectbox("Language", BOOK_LANGUAGES,
                                                             index=BOOK_LANGUAGES.index(book["language"]),
                                                             key=f"edit_language_{book['id']}")
                            
                            with col2:
                                edited_price = st.number_input("Price (₹)", min_value=0.0, step=100.0, value=book["price"], key=f"edit_price_{book['id']}")
                                edited_quantity = st.number_input("Quantity", min_value=0, step=1, value=book["quantity"], key=f"edit_quantity_{book['id']}")
                                edited_description = st.text_area("Description", book["description"], key=f"edit_description_{book['id']}")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("Update", key=f"update_{book['id']}"):
                                    book["title"] = edited_title
                                    book["author"] = edited_author
                                    book["category"] = edited_category
                                    book["language"] = edited_language
                                    book["price"] = edited_price
                                    book["quantity"] = edited_quantity
                                    book["description"] = edited_description
                                    book["available"] = min(book["available"], edited_quantity)
                                    
                                    save_books()
                                    st.success(f"Book '{edited_title}' updated successfully!")
                            
                            with col2:
                                if st.button("Delete", key=f"delete_{book['id']}"):
                                    st.session_state.books.remove(book)
                                    save_books()
                                    st.success(f"Book '{book['title']}' deleted successfully!")
                                    st.rerun()
                else:
                    st.info("No books in the library.")
            
            # View All Borrowings tab
            with admin_tab3:
                st.markdown('<h3>All Borrowings</h3>', unsafe_allow_html=True)
                
                if st.session_state.borrowings:
                    # Create a DataFrame for better display
                    borrowings_data = []
                    for borrowing in st.session_state.borrowings:
                        user_name = st.session_state.users[borrowing["username"]]["name"]
                        borrowings_data.append({
                            "ID": borrowing["id"],
                            "Book": borrowing["book_title"],
                            "User": f"{borrowing['username']} ({user_name})",
                            "Borrow Date": borrowing["borrow_date"],
                            "Return Date": borrowing["return_date"] or "Not returned"
                        })
                    
                    df = pd.DataFrame(borrowings_data)
                    st.dataframe(df, use_container_width=True)
                    
                    # Download option
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download as CSV",
                        data=csv,
                        file_name="library_borrowings.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("No borrowing records found.")
        else:
            st.warning("You don't have permission to access the admin panel.")

    # Dataset Management tab (only visible to admin)
    if st.session_state.is_admin:
        st.markdown("---")
        st.markdown('<h2 class="sub-header">Dataset Management</h2>', unsafe_allow_html=True)
        
        dataset_tab1, dataset_tab2, dataset_tab3, dataset_tab4 = st.tabs([
            "Categories", "Languages", "Authors", "Popular Books"
        ])
        
        # Categories Management
        with dataset_tab1:
            st.markdown('<h3>Manage Categories</h3>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                new_category = st.text_input("Add New Category")
                if st.button("Add Category"):
                    if new_category and new_category not in st.session_state.custom_categories:
                        st.session_state.custom_categories.append(new_category)
                        st.success(f"Category '{new_category}' added successfully!")
            
            with col2:
                category_to_remove = st.selectbox("Remove Category", 
                    [c for c in st.session_state.custom_categories if c not in ["Fiction", "Non-Fiction"]])
                if st.button("Remove Category"):
                    if category_to_remove:
                        st.session_state.custom_categories.remove(category_to_remove)
                        st.success(f"Category '{category_to_remove}' removed successfully!")
            
            st.markdown("### Current Categories")
            st.write(st.session_state.custom_categories)
        
        # Languages Management
        with dataset_tab2:
            st.markdown('<h3>Manage Languages</h3>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                new_language = st.text_input("Add New Language")
                if st.button("Add Language"):
                    if new_language and new_language not in st.session_state.custom_languages:
                        st.session_state.custom_languages.append(new_language)
                        st.success(f"Language '{new_language}' added successfully!")
            
            with col2:
                language_to_remove = st.selectbox("Remove Language", 
                    [l for l in st.session_state.custom_languages if l not in ["English"]])
                if st.button("Remove Language"):
                    if language_to_remove:
                        st.session_state.custom_languages.remove(language_to_remove)
                        st.success(f"Language '{language_to_remove}' removed successfully!")
            
            st.markdown("### Current Languages")
            st.write(st.session_state.custom_languages)
        
        # Authors Management
        with dataset_tab3:
            st.markdown('<h3>Manage Authors</h3>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                new_author = st.text_input("Add New Author")
                if st.button("Add Author"):
                    if new_author and new_author not in st.session_state.custom_authors:
                        st.session_state.custom_authors.append(new_author)
                        st.success(f"Author '{new_author}' added successfully!")
            
            with col2:
                author_to_remove = st.selectbox("Remove Author", st.session_state.custom_authors)
                if st.button("Remove Author"):
                    if author_to_remove:
                        st.session_state.custom_authors.remove(author_to_remove)
                        st.success(f"Author '{author_to_remove}' removed successfully!")
            
            st.markdown("### Current Authors")
            st.write(st.session_state.custom_authors)
        
        # Popular Books Management
        with dataset_tab4:
            st.markdown('<h3>Manage Popular Books</h3>', unsafe_allow_html=True)
            
            # Add new book
            st.markdown("#### Add New Book")
            col1, col2 = st.columns(2)
            with col1:
                new_book_title = st.text_input("Book Title")
                new_book_author = st.selectbox("Author", st.session_state.custom_authors)
            with col2:
                new_book_category = st.selectbox("Category", st.session_state.custom_categories)
                new_book_language = st.selectbox("Language", st.session_state.custom_languages)
            
            if st.button("Add Book"):
                if new_book_title and new_book_author and new_book_category and new_book_language:
                    new_book = {
                        "title": new_book_title,
                        "author": new_book_author,
                        "category": new_book_category,
                        "language": new_book_language,
                        "cover_url": ""
                    }
                    if new_book not in st.session_state.custom_books:
                        st.session_state.custom_books.append(new_book)
                        st.success(f"Book '{new_book_title}' added successfully!")
            
            # Remove book
            st.markdown("#### Remove Book")
            book_to_remove = st.selectbox("Select Book to Remove", 
                [f"{book['title']} by {book['author']}" for book in st.session_state.custom_books])
            if st.button("Remove Book"):
                if book_to_remove:
                    title = book_to_remove.split(" by ")[0]
                    st.session_state.custom_books = [b for b in st.session_state.custom_books if b['title'] != title]
                    st.success(f"Book '{title}' removed successfully!")
            
            st.markdown("### Current Popular Books")
            books_df = pd.DataFrame(st.session_state.custom_books)
            st.dataframe(books_df, use_container_width=True)

# Footer
st.markdown("---")
st.caption("Library Management System © 2023") 