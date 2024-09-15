import streamlit as st
import sqlite3
import os
import base64
from streamlit_tags import st_tags, st_tags_sidebar

# Connect to SQLite database
conn = sqlite3.connect('pdf_data.db')
c = conn.cursor()


# Streamlit app
def main():
    # Set background image
    st.markdown("""  
        <style>
            .stApp {
                background-image: url('https://static.vecteezy.com/system/resources/previews/027/105/968/non_2x/legal-law-and-justice-concept-open-law-book-with-a-wooden-judges-gavel-in-a-courtroom-or-law-enforcement-office-free-photo.jpg');
                background-size: cover; 
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }
        </style>
    """, unsafe_allow_html=True)

    # CSS styling
    st.markdown("""
        <style>
            .title {
            color: #FFFF;
            font-size: 66px;
            font-weight: 400;
            margin-bottom: 20px;
            text-align: left;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
            margin-top: 20px;
            margin-left: 20px;
            font-weight: bold;
            }
            .pdf-link {
                color: #293638;
                text-decoration: none;
                font-weight: bold;
                margin-right: 10px;
                transition: color 0.3s ease;
                text-align: center;
            }
            .pdf-link:hover {
                color: #0056b3;
                
            }
            .pdf-iframe {
            border: 1px solid #ccc;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
            width: 110%; /* Adjust the width */
            height: 800px; /* Adjust the height */
    }
            .doc-card {
                background-color: #293638;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                animation: fadein 1s;
            }
            .doc-title {
                color: white;
                font-size: 25px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            @keyframes fadein {
                from { opacity: 0; }
                to   { opacity: 1; }
            }
            .logout-box {
                background-color: #141414;
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            .logout-link {
                color: white;
                text-decoration: none;
                font-weight: bold;
            }
            .logout-link:hover {
                color: #FFFF;
            }
            .back-button-box {
                background-color: #f0f0f0; /* Background color */
                padding: 15px 30px; 
                border-radius: 8px;
                margin-top: 20px;
                text-align: center;
            }
            .back-button {
                color: #333;
                text-decoration: none;
                font-weight: bold;
                transition: color 0.3s ease;
            }
            .back-button:hover {
                color: #555;
            }
            .stWarning {
                color: #FF5733; /* Adjust the color to make it more visible */
                font-size: 20px; /* Adjust the font size */
                font-weight: bold; /* Make the font bold for emphasis */
                margin-top: 10px; /* Add some top margin for spacing */
            }
            
        </style>
    """, unsafe_allow_html=True)
    
    

    st.markdown("<h1 class='title'>LegiSearch⚖️ </h1>", unsafe_allow_html=True)

    # Determine page
    page = st.query_params.get("page", "home")

    if page == "home":
        home_page()
    elif page == "pdf_viewer":
        pdf_viewer_page()
    elif page == "search_results":
        search_results_page()

    # Close connection
    conn.close()

# Function for home page
def home_page():
    # Define category keywords
    category_keywords = {
        'Civil': ['civil', 'law', 'land', 'appeal','section'],
        'Criminal': ['criminal','rape','sexual', 'abduct', 'crime', 'accused', 'mob', 'harassment', 'offence', 'narcotics', 'appeal','murder','fia','cia','opium','section'],
        'Family': ['family', 'marriage', 'divorce', 'custody', 'child', 'dowry','dower'],
        'Constitutional': ['constitutional', 'rights','election', 'affairs', 'amendment', 'religion', 'minorities', 'freedom', 'appeal','nab','section','304','428','429','430','298'],
        'Labor': ['labor', 'employment', 'workers','appeal','project','job','birth','union'],
        'Section':['section','304','428','429','430','298','amendment']
    }
    # Get search query from URL parameters
    search_query = st.query_params.get("search_query")

    # Input for searching keywords with autocomplete
    all_keywords = [keyword for keywords in category_keywords.values() for keyword in keywords]

    # Custom label for search input
    st.markdown("""
        <style>
        .custom-label {
            font-size: 20px;
            font-weight: bold;
            color: #fffff;
            padding: 10px 0;
            margin-bottom: 5px;
        }
        </style>
        <div class="custom-label">Enter keywords to search documents:</div>
    """, unsafe_allow_html=True)

    # Input field for searching keywords
    search_keywords = st_tags(
        label='',
        text='Enter keywords to search documents',
        value=search_query.split() if search_query else [],
        suggestions=all_keywords
    )

    search_query_input = ' '.join(search_keywords)

    # Suggestion box for categories based on entered keywords
    filtered_categories = [category for category, keywords in category_keywords.items() if any(keyword.lower() in search_query_input.lower() for keyword in keywords)]
    selected_category = st.selectbox("Category:", filtered_categories)

    # Button to trigger search when category is selected
    search_triggered = st.button("Search")

    if selected_category and search_triggered:
        search_query_input = selected_category

    # Proceed with search if there's a search query
    if search_query_input:
        conn = sqlite3.connect('pdf_data.db')
        c = conn.cursor()
        c.execute("SELECT DISTINCT filename, MIN(title) AS title FROM pdf_data WHERE keywords LIKE ? GROUP BY filename", ('%' + search_query_input + '%',))
        results = c.fetchall()
        conn.close()

        if results:
            st.write(f"Found {search_query_input} {len(results)} document(s) matching your query.")
            for result in results:
                pdf_link = f"/?page=pdf_viewer&filename={result[0]}&search_query={search_query_input}"
                st.markdown(
                    f'<div class="doc-card"><p class="doc-title">Title: {result[1]}</p><a href="{pdf_link}" class="pdf-link" target="_self">View PDF ({result[0]})</a></div>',
                    unsafe_allow_html=True)
        else:
            st.markdown("No documents found matching your query.")

    else:
        st.warning("Please enter keywords to search documents.")

    
    # Sidebar for logout
    st.sidebar.title("Menu")
    st.sidebar.markdown('Click below to Logout')
    st.sidebar.markdown("<div class='logout-box'><a href='http://localhost:8501' class='logout-link' target='_self'>Logout</a></div>", unsafe_allow_html=True)

# Function for PDF viewer page
def pdf_viewer_page():
    filename = st.query_params.get("filename")
    search_query = st.query_params.get("search_query")
    pdf_directory = r'C:\Users\Hp\Desktop\Legi\path'
    full_path = os.path.join(pdf_directory, filename)
    try:
        with open(full_path, "rb") as file:
            pdf_bytes = file.read()
            pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
            st.markdown(f'<iframe src="data:application/pdf;base64,{pdf_base64}" width="150%" height="1000" class="pdf-iframe"></iframe>', unsafe_allow_html=True)
            st.write("")  # Empty space for better layout
            st.markdown(f"<div class='back-button-box'><a href='/?page=search_results&search_query={search_query}' class='back-button' target='_self'>Go Back to Search Page</a></div>", unsafe_allow_html=True)

    except FileNotFoundError:
        st.error("File not found.")

# Function for displaying search results page
def search_results_page():
    # Define category keywords
    category_keywords = {
        'Civil': ['civil', 'law', 'land', 'appeal','section'],
        'Criminal': ['criminal', 'abduct','rape','sexual', 'crime', 'accused', 'mob', 'harassment', 'offence', 'narcotics', 'appeal','murder','fia','cia','opium','section'],
        'Family': ['family', 'marriage', 'divorce', 'custody', 'child', 'dowry'],
        'Constitutional': ['constitutional','election', 'rights','affairs' ,'amendment', 'religion', 'minorities', 'freedom', 'appeal','nab','section','304','428','429','430','298'],
        'Labor': ['labor', 'employment', 'workers','appeal','project','job','birth','union'],
        'Section':['section','304','428','429','430','298','amendment']
    }

    search_query = st.query_params.get("search_query")

    # Input for searching keywords with autocomplete
    all_keywords = [keyword for keywords in category_keywords.values() for keyword in keywords]
    # Custom label for search input
    st.markdown("""
        <style>
        .custom-label {
            font-size: 20px;
            font-weight: bold;
            color: #fffff;
            padding: 10px 0;
            margin-bottom: 5px;
        }
        </style>
        <div class="custom-label">Enter keywords to search documents:</div>
    """, unsafe_allow_html=True)
    search_query_input = st_tags(
        label='',
        text='Enter keywords to search documents:',
        value=search_query.split() if search_query else [],
        suggestions=all_keywords
    )

    search_query_input = ' '.join(search_query_input)

    # Suggestion box for categories based on entered keywords
    filtered_categories = [category for category, keywords in category_keywords.items() if any(keyword.lower() in search_query_input.lower() for keyword in keywords)]
    selected_category = st.selectbox("Category:", filtered_categories)

    # Button to trigger search when category is selected
    search_triggered = st.button("Search")

    if selected_category and search_triggered:
        search_query_input = selected_category

    if search_query_input:
        conn = sqlite3.connect('pdf_data.db')
        c = conn.cursor()
        c.execute("SELECT DISTINCT filename, MIN(title) AS title FROM pdf_data WHERE keywords LIKE ? GROUP BY filename", ('%' + search_query_input + '%',))
        results = c.fetchall()
        conn.close()

        if results:
            st.markdown(f"Found {search_query_input} {len(results)} document(s) matching your query.")
            for result in results:
                pdf_link = f"/?page=pdf_viewer&filename={result[0]}&search_query={search_query_input}"
                st.markdown(
                    f'<div class="doc-card"><p class="doc-title">Title: {result[1]}</p><a href="{pdf_link}" class="pdf-link" target="_self">View PDF ({result[0]})</a></div>',
                    unsafe_allow_html=True)
        else:
            st.markdown("No documents found matching your query.", unsafe_allow_html=True)  # Adding unsafe_allow_html=True for warning message
           
    else:
        st.warning("Please enter keywords to search documents.")
# Sidebar for logout
    st.sidebar.title("Menu")
    st.sidebar.markdown('Click below to Logout')
    st.sidebar.markdown("<div class='logout-box'><a href='http://localhost:8501' class='logout-link' target='_self'>Logout</a></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
