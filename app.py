import streamlit as st
import pandas as pd
import requests

# Set page configuration
st.set_page_config(page_title="Library Management System", layout="wide")

# Apply Background Image Using Streamlit Components
def set_bg_image(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url({image_url}) no-repeat center center fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set background image
set_bg_image("https://www.edigitallibrary.com/img/Library-school.jpg")

# Custom CSS for Styling
st.markdown(
    """
    <style>
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            width: 230px !important;
            background: #690B22;
            box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.7);
        }
        
        /* Main Title */
        .main-title {
            text-align: center;
            color: #ffffff;
            font-size: 40px;
            font-weight: bold;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);
        }
        
        /* Buttons */
        .stButton > button {
            background-color: #7D0A0A;
            color: white;
            font-size: 18px;
            border-radius: 8px;
            padding: 10px 20px;
            transition: all 0.3s ease-in-out;
        }
        .stButton > button:hover {
            background-color: #690B22;
            transform: scale(1.1);
             color: #ffffff;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar menu
st.sidebar.title("📖 Menu")
option = st.sidebar.radio("Choose an Option", ["Add Book", "Delete Book", "Issue Book", "Return Book", "View Local Books", "View API Books"])

# Dummy Book Database (Replace with actual DB or API calls)
if "books" not in st.session_state:
    st.session_state.books = pd.DataFrame(columns=["ID", "Title", "Author"])

# Add Book
if option == "Add Book":
    st.markdown('<h1 class="main-title">📚 Add a New Book</h1>', unsafe_allow_html=True)
    book_id = st.text_input("Book ID")
    title = st.text_input("Title")
    author = st.text_input("Author")
    uploaded_file = st.file_uploader("Upload Book Image", type=["jpg", "jpeg", "png"])
    
    if st.button("Add Book"):
        if book_id and title and author:
            st.session_state.books = pd.concat([st.session_state.books, pd.DataFrame([[book_id, title, author]], columns=["ID", "Title", "Author"])], ignore_index=True)
            st.success("Book added successfully!")
        else:
            st.error("Please fill in all fields.")

# Delete Book
elif option == "Delete Book":
    st.markdown('<h1 class="main-title">🗑️ Delete a Book</h1>', unsafe_allow_html=True)
    book_id = st.text_input("Enter Book ID to Delete")
    if st.button("Delete Book"):
        st.session_state.books = st.session_state.books[st.session_state.books["ID"] != book_id]
        st.success("Book deleted successfully!")

# Issue Book
elif option == "Issue Book":
    st.markdown('<h1 class="main-title">📖 Issue a Book</h1>', unsafe_allow_html=True)
    book_id = st.text_input("Enter Book ID to Issue")
    if st.button("Issue Book"):
        st.success(f"Book ID {book_id} issued successfully!")

# Return Book
elif option == "Return Book":
    st.markdown('<h1 class="main-title">🔄 Return a Book</h1>', unsafe_allow_html=True)
    book_id = st.text_input("Enter Book ID to Return")
    if st.button("Return Book"):
        st.success(f"Book ID {book_id} returned successfully!")

# View Local Books
elif option == "View Local Books":
    st.markdown('<h1 class="main-title">📚 View Local Books</h1>', unsafe_allow_html=True)
    st.write(st.session_state.books)

# View API Books (Fetching from Open Library API)
elif option == "View API Books":
    st.markdown('<h1 class="main-title">🌐 Search and View Books from Open Library</h1>', unsafe_allow_html=True)
    query = st.text_input("Search for a book (e.g., Python, Data Science):")
    if st.button("Search"):
        if query:
            url = f"https://openlibrary.org/search.json?q={query}&limit=5"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                books = data.get("docs", [])
                if books:
                    for book in books:
                        st.subheader(book.get("title", "Unknown Title"))
                        st.write(f"Author: {', '.join(book.get('author_name', ['Unknown Author']))}")
                        st.write(f"First Published Year: {book.get('first_publish_year', 'N/A')}")
                else:
                    st.warning("No books found. Try a different search query.")
            else:
                st.error("Failed to fetch data from Open Library API.")
        else:
            st.warning("Enter a search query to find books.")