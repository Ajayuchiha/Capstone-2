import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Set Streamlit page config
st.set_page_config(page_title = "BookScape Explorer", layout = "wide")

# Database connection
@st.cache_resource(ttl = 600)  # Refresh connection every 10 minutes
def get_connection():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Narut0@kurama", 
        database = "bookscape"
    )

# Set Times New Roman as the default font and add creative styling
st.markdown("""
    <style>
    * {
        font-family: 'Times New Roman', serif !important;
    }
    h1 {
        color: #4A90E2;
        text-align: center;
    }
    h2 {
        color: #50B432;
    }
    /* Title color */
    h1 {
        color: #ffee33 !important;  /* Yellow color */
        text-align: center;
    }

    /* Header color */
    h2 {
        color: #33ffbe !important;  /* HEX color */
    }

    /* Selectbox color */
    .stSelectbox > div > div {
        background-color: #f72323;  /* Red background */ 
        color: Black;  /* Black text */
    }
    
    /* Selectbox color */
    .stSelectbox > div > div {
        background-color: #ddf5da;  /* Green background */ 
        color: Black;  /* Black text */
    }

    /* Sidebar title color */
    .sidebar .sidebar-content .stMarkdown h1 {
        color: #8E44AD !important;  /* Purple color */
    }

    /* Option color in sidebar */
    .sidebar .sidebar-content > div > div {
        background-color: #34495E;  /* Dark blue background */
        color: White;  /* White text */
    }
    .stButton button {
        background-color: #1b07f0;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stButton button:hover {
        background-color: #357ABD;
    }
    .stDataFrame {
        border: 1px solid #4A90E2;
        border-radius: 5px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Function to generate WordCloud
def generate_wordcloud():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT book_title FROM dance_book_data")
    titles = [row[0] for row in cursor.fetchall()]
    text = " ".join(titles)
    
    wordcloud = WordCloud(width = 800, height = 400, background_color = "black").generate(text)
    plt.figure(figsize = (10, 5))
    plt.imshow(wordcloud, interpolation = "bilinear")
    plt.axis("off")
    st.pyplot(plt)

# Function to generate WordCloud
def generate_wordcloud():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT book_title FROM dance_book_data")
    titles = [row[0] for row in cursor.fetchall()]
    text = " ".join(titles)
    
    wordcloud = WordCloud(width = 800, height = 400, background_color = "black").generate(text)
    plt.figure(figsize = (10, 5))
    plt.imshow(wordcloud, interpolation = "bilinear")
    plt.axis("off")
    st.pyplot(plt)

# Queries dictionary
queries = {
    "Availability of eBooks vs Physical Books": """
        SELECT COUNT(CASE WHEN is_Ebook = 1 THEN 1 END) AS ebooks,
               COUNT(CASE WHEN is_Ebook = 0 THEN 1 END) AS physical_books
        FROM dance_book_data;
    """,
    
    "Publisher with Most Books Published": """
        SELECT publisher, COUNT(*) AS top_publisher
        FROM dance_book_data
        GROUP BY publisher
        ORDER BY top_publisher DESC
        LIMIT 1;
    """,
    
    "Publisher with Highest Average Rating": """
        SELECT publisher, AVG(average_Rating) AS avg_rating
        FROM dance_book_data
        GROUP BY publisher
        ORDER BY avg_rating DESC
        LIMIT 1;
    """,
    
    "Top 5 Most Expensive Books": """
        SELECT book_title, amount_retailPrice
        FROM dance_book_data
        ORDER BY amount_retailPrice DESC
        LIMIT 5;
    """,
    
    "Books Published After 2010 with at Least 500 Pages": """
        SELECT book_title, year, page_Count
        FROM dance_book_data
        WHERE year > 2010 AND page_Count >= 500
        ORDER BY year ASC;
    """,
    
    "Books with Discounts Greater than 20%": """
        SELECT book_title, 
               ((amount_listPrice - amount_retailPrice) / amount_listPrice) * 100 AS discount_above_20_percentage
        FROM dance_book_data
        WHERE amount_listPrice > 0 AND ((amount_listPrice - amount_retailPrice) / amount_listPrice) * 100 > 20
        ORDER BY discount_above_20_percentage ASC;
    """,

    "Average Page Count for eBooks vs Physical Books": """
        SELECT is_Ebook, AVG(page_Count) AS Average_Page_Count
        FROM dance_book_data
        GROUP BY is_Ebook;
    """,

    "Top 3 Authors with the Most Books": """
        SELECT book_authors, COUNT(*) AS total_books
        FROM dance_book_data
        GROUP BY book_authors
        ORDER BY total_books DESC
        LIMIT 3;
    """, 

    "Publishers with More than 10 Books": """
        SELECT publisher, COUNT(*) AS total_books
        FROM dance_book_data
        GROUP BY publisher
        HAVING total_books > 10
        ORDER BY total_books DESC;
    """, 

    "Average Page Count for Each Category": """
        SELECT categories, AVG(page_Count) AS avg_page_count
        FROM dance_book_data
        GROUP BY categories
        ORDER BY avg_page_count DESC;
    """, 

    "Books with More than 3 Authors": """
        SELECT book_title, book_authors
        FROM dance_book_data
        WHERE LENGTH(book_authors) - LENGTH(REPLACE(book_authors, ',', '')) >= 3;
    """, 

    "Books with Ratings Count Greater Than the Average": """
        SELECT book_title, ratings_Count
        FROM dance_book_data
        WHERE ratings_Count > (SELECT AVG(ratings_Count) FROM dance_book_data)
        ORDER BY ratings_Count DESC;
    """, 
        
    "Books with the Same Author Published in the Same Year": """
        SELECT book_authors, year, COUNT(*) AS books_published
        FROM dance_book_data
        GROUP BY book_authors, year
        HAVING books_published > 1
        ORDER BY year ASC;
    """,

    "Books with a Specific Keyword in the Title": """
        SELECT book_title
        FROM dance_book_data
        WHERE book_title LIKE '%dance%';
    """, 

    "Year with the Highest Average Book Price": """
        SELECT year, AVG(amount_retailPrice) AS avg_price
        FROM dance_book_data
        GROUP BY year
        ORDER BY avg_price DESC
        LIMIT 1;
    """, 

    "Authors Who Published 3 Consecutive Years": """
        SELECT 
            book_authors, 
            COUNT(DISTINCT year) AS consecutive_years
        FROM dance_book_data
        GROUP BY book_authors
        HAVING MAX(year) - MIN(year) >= 2
        ORDER BY consecutive_years DESC;
    """, 

    "Authors Who Published Books in the Same Year Under Different Publishers": """
        SELECT 
            book_authors, 
            year, 
            COUNT(DISTINCT publisher) AS publisher_count
        FROM dance_book_data
        GROUP BY book_authors, year
        HAVING COUNT(DISTINCT publisher) > 1
        ORDER BY year ASC;
    """, 

    "Average Retail Price of eBooks vs Physical Books": """
        SELECT 
            AVG(CASE WHEN is_Ebook = 1 THEN amount_retailPrice END) AS avg_ebook_price,
            AVG(CASE WHEN is_Ebook = 0 THEN amount_retailPrice END) AS avg_physical_price
        FROM dance_book_data;
    """, 

    "Books with Outlier Ratings": """
        WITH stats AS (
            SELECT 
                AVG(average_Rating) AS avg_rating, 
                STDDEV(average_Rating) AS std_dev
            FROM dance_book_data
        )
        SELECT 
            book_title, 
            average_Rating, 
            ratings_Count
        FROM dance_book_data, stats
        WHERE average_Rating > (stats.avg_rating + 2 * stats.std_dev)
           OR average_Rating < (stats.avg_rating - 2 * stats.std_dev);
    """,

    "Publisher with the Highest Average Rating (More than 10 Books)": """
        SELECT publisher, AVG(average_Rating) AS avg_rating, COUNT(*) AS total_books
        FROM dance_book_data
        GROUP BY publisher
        HAVING total_books > 10
        ORDER BY avg_rating DESC
        LIMIT 1;
    """
}

# Streamlit App
def main():
    st.title("📚 BookScape Explorer")
    st.markdown('<p style = "color:#4437fa; font-size:20px;"><b>Welcome to BookScape Explorer! 🎉</b></p>', unsafe_allow_html = True)
    generate_wordcloud()
    st.sidebar.title("Navigation")
    option = st.sidebar.selectbox(
        "Choose an option",
        ["Home", "Run SQL Queries"]
    )

    if option == "Home":

        st.markdown('<p style = "color:#eba91c; font-size:18px;">BookScape Explorer is a user-friendly web application designed to help book enthusiasts explore and analyze book data using SQL queries. It provides insights into book trends, ratings, and availability, pricing, authors, and publishers making it easier to discover new reads and make informed decisions.</p>', unsafe_allow_html = True)

    elif option == "Run SQL Queries":
        st.header("🔍 SQL Queries")
        query_choice = st.selectbox("Select a Query to Run", list(queries.keys()))

        if st.button("Run Query"):
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(queries[query_choice])
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]  # Get column names
            df = pd.DataFrame(result, columns=columns)
            st.dataframe(df)

if __name__ == "__main__":
    main()



