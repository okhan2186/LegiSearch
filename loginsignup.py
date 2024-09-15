import streamlit as st
import sqlite3
import hashlib
import re
from streamlit_option_menu import option_menu
st.set_page_config(layout="wide")
# Database connection
conn = sqlite3.connect('LS.db')
c = conn.cursor()

# Create user table if not exists
c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, email TEXT, password TEXT)')
conn.commit()

def password_strength(password):
    # Define criteria for password strength
    length_error = len(password) < 8
    number_error = re.search(r'\d', password) is None
    uppercase_error = re.search(r'[A-Z]', password) is None
    lowercase_error = re.search(r'[a-z]', password) is None
    special_error = re.search(r'[!@#$%^&*()_+{}|:"<>?]', password) is None

    # Calculate overall strength score
    strength_score = 5 - sum([length_error, number_error, uppercase_error, lowercase_error, special_error])

    return strength_score

def main():
    


    # st.set_page_config(layout="wide")
    # Add CSS for background image and custom text
    st.markdown(
        f"""
        <style>
            @keyframes fadeIn {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
            }}
            @keyframes slideInLeft {{
                from {{ transform: translateX(-100%); }}
                to {{ transform: translateX(0); }}
            }}
            @keyframes fadeInUp {{
                from {{ transform: translateY(20px); opacity: 0; }}
                to {{ transform: translateY(0); opacity: 1; }}
            }}
            .title {{
                color: #FFFF;
                font-size: 80px;
                font-weight: bold;
                margin-bottom: 20px;
                text-align: center;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
                margin-top: 20px;
                margin-left: 20px;
            }}

            .stApp {{
                background-image: url('https://static.vecteezy.com/system/resources/previews/027/105/968/non_2x/legal-law-and-justice-concept-open-law-book-with-a-wooden-judges-gavel-in-a-courtroom-or-law-enforcement-office-free-photo.jpg'); 
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
                padding: 20px;
            }}
            .custom-text {{
                color: #FFFF;
                font-size: 20px;
                font-family: 'Arial', sans-serif;
                line-height: 1.6;
                text-align: justify;
                padding: 20px;
                background-color: #293638;
                border-radius: 10px;
                box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
                animation: fadeIn 1s ease-in-out;
                font-weight: bold;
            }}
            .custom-text h1, .custom-text h2, .custom-text h3, .custom-text h4, .custom-text h5, .custom-text h6 {{
                color: #FFFFFF;
                font-family: 'Arial', sans-serif;
                font-size: 15px;
                font-weight: bold;
                text-align: center;
                margin-bottom: 10px;
                animation: slideInLeft 1s ease-in-out;
            }}
            .custom-text ul {{
                list-style-type: circle;
                padding-left: 20px;
                animation: fadeInUp 1s ease-in-out;
            }}
            .custom-text p {{
                font-size: 20px;
                margin-bottom: 10px;
                animation: fadeIn 1s ease-in-out;
            }}
            .key-feature {{
                margin-bottom: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
                transition: transform 0.3s ease, background-color 0.3s ease;
                font-family: 'Arial', sans-serif;
                animation: fadeInUp 1s ease-in-out; /* Add animation */
                background-color: #1e282c; /* Ensure good contrast */
                color: #FFFFFF; /* Ensure text color is readable */
                padding: 20px; /* Add padding for better readability */
            }}

            .key-feature:hover {{
                transform: translateY(-5px);
                background-color: #2b3a42; /* Change background color on hover */
            }}

            .card-body {{
                padding: 20px;
                background-color: #1e282c;
            }}

            .card-title {{
                font-size: 25px; /* Increase font size */
                font-weight: bold;
                color: #FFFFFF;
                margin-bottom: 5px;
                font-family: 'Arial', sans-serif;
            }}

            .card-text {{
                font-size: 30px; /* Increase font size */
                color: #FFFFFF;
                font-family: 'Arial', sans-serif;
            }}

            .contact-form {{
                display: flex;
                flex-direction: column;
                gap: 10px;
                margin-top: 20px;
                animation: fadeInUp 1s ease-in-out; /* Add animation */
            }}
            .contact-form input, .contact-form textarea {{
                padding: 10px;
                border-radius: 5px;
                border: 2px solid #293638;
                outline: none;
                font-size: 16px;
                font-family: 'Arial', sans-serif;
                transition: border-color 0.3s ease;
            }}
            .contact-form input:focus, .contact-form textarea:focus {{
                border-color: #1e282c;
            }}
            .contact-form button {{
                padding: 10px;
                border-radius: 5px;
                border: none;
                background-color: #293638;
                color: #FFFFFF;
                font-size: 24px;
                font-family: 'Arial', sans-serif;
                cursor: pointer;
                transition: background-color 0.3s ease, transform 0.3s ease;
            }}
            .contact-form button:hover {{
                background-color: #1e282c;
                transform: translateY(-3px);
            }}
            .login-box {{
                background-color: #141414;
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }}
            .login-link {{
                color: white;
                text-decoration: none;
                font-weight: bold;
            }}
            .login-link:hover {{
                color: #FFFF;
            }}

             <style>
            .card-title {{
                color: #ffff;
                font-style: "Helvetica";
                font-size: 30px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            .card-text {{
                color: #FFFF;
                font-size: 30px; /* Increase font size */
                font-family: 'Arial', sans-serif;
                line-height: 1.6;
                margin-bottom: 15px;
            }}
            .key-feature {{
                
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
        </style>

            
            
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<h1 class='title'>LegiSearch⚖️ </h1>", unsafe_allow_html=True)
    with st.sidebar:
        choice=option_menu(
            menu_title="Menu",
            options=["Home", "About","Rules & Regulations", "Contact", "Login", "SignUp"],
            icons=["house","calendar2-heart-fill","question-circle", "envelope-heart-fill","bi-box-arrow-in-right","bi-box-arrow-in-left"],
            menu_icon="bi-menu-app-fill",
            default_index=0,
            styles={
            
            "container": {"padding": "0!important","font-style":"Helvetica","font-size": "30px", "background-color": "#262631"},
            "icon": {"color": "white", "font-size": "30px"},
            "nav-link": {
                "font-style":"Helvetica",
                "font-size": "30px",
                "font-weight": "bold",
                "text-align": "justify",
                "margin": "10px 0px",
                "--hover-color": "#bf9000",
            },
            "nav-link-selected": {"background-color": "#bf9000"},
        }
         
        )
    
    # menu=["Home", "About", "Contact", "Login", "SignUp"]
   
    # choice=st.sidebar.selectbox("Menu",menu)
    
    if choice=="Home":
        st.title("Welcome to LegiSearch⚖️")
        
        st.write(
            
            """

        
            <div class="col-md-4">
                <div class="card key-feature">
                    <div class="card-body">
                        <h5 class="card-title">   </h5>
                        <p class="card-text">LegiSearch⚖️ aims to provide users with a streamlined and intuitive platform for searching and viewing legal documents. By leveraging advanced search capabilities, users can easily find relevant documents based on keywords, enhancing efficiency in legal research. The application offers a seamless PDF viewing experience, allowing users to explore documents with ease. With its user-friendly interface and robust functionality, LegiSearch seeks to simplify the process of accessing and analyzing legal content, catering to the needs of legal professionals, researchers, and enthusiasts alike.</p>
                    </div>
                </div>
            </div>
            """
            , unsafe_allow_html=True
        )


        # Key Features Cards
        st.write('<div class="row">', unsafe_allow_html=True)

        st.title("Key Features")

        # Feature 1: Search for legal documents
        st.write(
            """
            <div class="col-md-4">
                <div class="card key-feature">
                    <div class="card-body">
                        <h5 class="card-title">🔎 Search for Legal Documents</h5>
                        <p class="card-text">Effortlessly search through a vast database of legal documents.</p>
                    </div>
                </div>
            </div>
            """
            , unsafe_allow_html=True
        )

        # Feature 2: Access a wide range of legal resources
        st.write(
            """
            <div class="col-md-4">
                <div class="card key-feature">
                    <div class="card-body">
                        <h5 class="card-title">🔰 Access Legal Resources</h5>
                        <p class="card-text">Explore a diverse collection of legal resources at your fingertips.</p>
                    </div>
                </div>
            </div>
            """
            , unsafe_allow_html=True
        )

        # Feature 3: Stay updated with the latest legal news
        st.write(
            """
            <div class="col-md-4">
                <div class="card key-feature">
                    <div class="card-body">
                        <h5 class="card-title">📲 Stay Updated</h5>
                        <p class="card-text">Keep yourself informed with the latest legal news and updates.</p>
                    </div>
                </div>
            </div>
            """
            , unsafe_allow_html=True
        )
        

        st.write("</div>", unsafe_allow_html=True)

    elif choice=="About":
        st.title("About ")
       
        st.write(
            """
            
            
            <div class="col-md-4">
                <div class="card key-feature">
                    <div class="card-body">
                        <h5 class="card-title">About</h5>
                        <p class="card-text">LegiSearch⚖️ isn't your average legal search engine; it's your digital legal concierge, poised to revolutionize the way you navigate the legal landscape. Picture an expansive repository housing a treasure trove of legal documents, from landmark cases to intricate statutes, all at your fingertips. With LegiSearch, your journey through legal research becomes a breeze, thanks to its intuitive interface and advanced search features that deliver precise results with ease. Stay ahead of the curve with our commitment to keeping our database current, ensuring you're always armed with the latest legal insights. But LegiSearch isn't just about functionality—it's about empowerment. Customize your experience, dive deep into analysis, and uncover the legal gems you seek, all in one seamless platform. Say goodbye to the ordinary and hello to extraordinary legal research with LegiSearch.</p>
                    </div>
                </div>
            </div>
            """
            , unsafe_allow_html=True
        )
        
        
        st.title("Our Mission")
         # Feature 1: Accessibility
        st.write(
            """
            <div class="col-md-4">
        <div class="card key-feature">
            <div class="card-body">
                <h5 class="card-title">🔰 Accessibility</h5>
                <p class="card-text">LegiSearch is committed to democratizing access to legal knowledge by providing a user-friendly platform for searching and viewing legal documents. We believe that everyone should have access to legal information, regardless of their background or expertise.</p>
            </div>
        </div>
    </div>
            """
            , unsafe_allow_html=True
        )





        # Feature 2: Efficiency
        st.write(
            """
            <div class="col-md-4">
                <div class="card key-feature">
                    <div class="card-body">
                        <h5 class="card-title">🏋 Efficiency</h5>
                        <p class="card-text">Our mission is to enhance the efficiency of legal research by offering advanced search capabilities and seamless PDF viewing. We strive to empower users, whether legal professionals, researchers, or enthusiasts, with the tools they need to quickly find and analyze relevant documents.</p>
                    </div>
                </div>
            </div>
            """
            , unsafe_allow_html=True
        )
                 # Feature 3: Understanding
                # Feature 3: Stay updated with the latest legal news
        st.write(
            """
            <div class="col-md-4">
                <div class="card key-feature">
                    <div class="card-body">
                        <h5 class="card-title">💡 Understanding</h5>
                        <p class="card-text">At LegiSearch, we aim to foster a deeper understanding of the law by facilitating access to comprehensive legal content. By breaking down barriers to legal information, we enable users to make informed decisions and navigate complex legal issues with confidence.</p>
                    </div>
                </div>
            </div>
            """
            , unsafe_allow_html=True
        )
        
    elif choice == "Rules & Regulations":
        st.title("Rules and Regulations for LegiSearch Website")
        st.write(
        """
        <style>
            .card-title {
                color: #ffff;
                font-style: "Helvetica";
                font-size: 30px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .card-text {
                color: #FFFF;
                font-size: 30px; /* Increase font size */
                font-family: 'Arial', sans-serif;
                line-height: 1.6;
                margin-bottom: 15px;
            }
            .key-feature {
                
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
        </style>
        <div class="col-md-4">
            <div class="card key-feature">
                <div class="card-body">
                    <h5 class="card-title">Sign-Up Process</h5>
                    <p class="card-text">If you are new to the website, you need to sign up first. Click on the "Sign Up" button and provide the required information to create your account. If you already have an account, click on the "Sign In" button and enter your credentials to log in.</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card key-feature">
                <div class="card-body">
                    <h5 class="card-title">Searching Documents</h5>
                    <p class="card-text">Once you are logged in, you can use the search bar to find documents by entering relevant keywords. Enter specific keywords related to the topic you are looking for. For example, if you are interested in documents related to "murder" or any "crime", type those keywords in the search bar.</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card key-feature">
                <div class="card-body">
                    <h5 class="card-title">Categories</h5>
                    <p class="card-text">Based on your search keywords, the website will suggest relevant categories such as Civil, Criminal, Family, Constitutional, and Labor. You can select a category from the suggestions to narrow down your search results. This helps in finding documents more efficiently.</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card key-feature">
                <div class="card-body">
                    <h5 class="card-title">Viewing Documents</h5>
                    <p class="card-text">After you search for a document, a list of matching documents will be displayed. Click on the "View PDF" link to open the document. The document will open in an embedded PDF viewer on the website. If you want to go back to the search results page, use the "Go Back to Search Page" button provided in the PDF viewer page.</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card key-feature">
                <div class="card-body">
                    <h5 class="card-title">Logout</h5>
                    <p class="card-text">There is an option to log out of your account from the sidebar menu. Click on the "Logout" button to sign out from the website securely.</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card key-feature">
                <div class="card-body">
                    <h5 class="card-title">General Usage</h5>
                    <p class="card-text">Use the website respectfully and do not engage in any unlawful activities using the documents found on the site. Your personal information is protected and will not be shared with third parties. Ensure you use your account responsibly. If you encounter any issues or need assistance, you can contact the website's support team for help.</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card key-feature">
                <div class="card-body">
                    <h5 class="card-title">Legal Notice</h5>
                    <p class="card-text">The documents provided on this website are for informational purposes only. The website does not guarantee the accuracy or completeness of the information. Users are responsible for their use of the information and documents obtained from the website.</p>
                </div>
            </div>
        </div>
        """
        , unsafe_allow_html=True
    )


    elif choice == "Contact":
        st.title("Contact Us")
        
        name = st.text_input("Your Name", key="name")
        email = st.text_input("Your Email", key="email")
        message = st.text_area("Your Message", key="message")
        if st.button("Submit"):
            if name and email and message:
                # Here you can handle the form submission (e.g., save to database, send an email, etc.)
                # st.success("Thank you for your message! We will get back to you soon.")
                st.markdown(f"<div class='login-box'> Thank you for your message! We will get back to you soon </a></div>", unsafe_allow_html=True)

            else:
                # st.error("Please fill in all fields.")
                st.markdown(f"<div class='login-box'> Please fill in all fields. </a></div>", unsafe_allow_html=True)


    elif choice == "Login":
        st.title("Login To Your Account")

        username = st.text_input("User Name")
        password = st.text_input("Password", type='password')

        if st.button("Login"):
            c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, hashlib.sha256(password.encode()).hexdigest()))
            data = c.fetchall()
            if data:
                # st.success("Logged In as {}".format(username))
                st.markdown(f"<div class='login-box'><a href='http://localhost:8502' class='login-link' target='_self'>Welcome to LegiSearch, {username}</a></div>", unsafe_allow_html=True)

            else:
                # st.warning("Incorrect Username/Password")
                st.markdown(f"<div class='login-box'> Incorrect Username/Password</a></div>", unsafe_allow_html=True)

    elif choice == "SignUp":
        st.title("Create New Account")
        new_user = st.text_input("Username")
        new_email = st.text_input("Email")
        new_password = st.text_input("Password", type='password')
        confirm_password = st.text_input("Confirm Password", type='password')

        if st.button("SignUp"):
            if new_password != confirm_password:
                # st.error("Passwords do not match")
                st.markdown(f"<div class='login-box'> Passwords do not match</a></div>", unsafe_allow_html=True)
            
            elif password_strength(new_password) < 3:
                st.markdown(f"<div class='login-box'> Please fill in all fields.</a></div>", unsafe_allow_html=True)

            else:
                hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
                c.execute('INSERT INTO userstable(username, email, password) VALUES (?,?,?)', (new_user, new_email, hashed_password))
                conn.commit()
                # st.success("Account created successfully")
                st.markdown(f"<div class='login-box'> Account created successfully</a></div>", unsafe_allow_html=True)

                # st.info("Go to the Login menu to log in")
                st.markdown(f"<div class='login-box'> Go to the Login menu to log in </a></div>", unsafe_allow_html=True)


if __name__ == '__main__':
    main()
