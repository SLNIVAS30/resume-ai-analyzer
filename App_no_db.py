# Developed by dnoobnerd [https://dnoobnerd.netlify.app]    Made with Streamlit


###### Packages Used ######
import streamlit as st # core package used in this project
import pandas as pd
import base64, random
import time,datetime
import os
import socket
import platform
import geocoder
import secrets
import io,random
import plotly.express as px # to create visualisations at the admin session
import plotly.graph_objects as go
from geopy.geocoders import Nominatim
# libraries used to parse the pdf files
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
from streamlit_tags import st_tags
from PIL import Image
# pre stored data for prediction purposes
from Courses import ds_course,web_course,android_course,ios_course,uiux_course,resume_videos,interview_videos
import nltk
nltk.download('stopwords')


###### Preprocessing functions ######


# Generates a link allowing the data in a given panda dataframe to be downloaded in csv format 
def get_csv_download_link(df,filename,text):
    csv = df.to_csv(index=False)
    ## bytes conversions
    b64 = base64.b64encode(csv.encode()).decode()      
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href


# Reads Pdf file and check_extractable
def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
            print(page)
        text = fake_file_handle.getvalue()

    ## close open handles
    converter.close()
    fake_file_handle.close()
    return text


# show uploaded file path to view pdf_display
def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


# course recommendations which has data already loaded from Courses.py
def course_recommender(course_list):
    st.subheader("**Courses & Certificates Recommendations 👨‍🎓**")
    c = 0
    rec_course = []
    ## slider to choose from range 1-10
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 5)
    random.shuffle(course_list)
    for c_name, c_link in course_list:
        c += 1
        st.markdown(f"({c}) [{c_name}]({c_link})")
        rec_course.append(c_name)
        if c == no_of_reco:
            break
    return rec_course


###### Database Stuffs (Disabled) ######

# Database functions disabled for standalone operation
def insert_data(sec_token,ip_add,host_name,dev_user,os_name_ver,latlong,city,state,country,act_name,act_mail,act_mob,name,email,res_score,timestamp,no_of_pages,reco_field,cand_level,skills,recommended_skills,courses,pdf_name):
    # Database insertion disabled
    pass

def insert_feedback(sec_token,ip_add,host_name,dev_user,os_name_ver,latlong,city,state,country,act_name,act_mail,act_mob,timestamp,feedback):
    # Database insertion disabled
    pass

def fetch_data():
    # Database fetch disabled - return empty DataFrame
    return pd.DataFrame()

def fetch_feedback():
    # Database fetch disabled - return empty DataFrame
    return pd.DataFrame()

def run():
    
    # Professional header
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 30px;'>
        <h1 style='color: white; margin: 0;'>Resume Gap Analyzer</h1>
        <p style='color: white; margin: 10px 0 0 0; opacity: 0.9;'>Professional Resume Analysis & Recommendations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Professional sidebar
    st.sidebar.markdown("### Navigation")
    activities = ["User", "Feedback", "About", "Admin"]
    choice = st.sidebar.selectbox("Select an option:", activities)
    st.sidebar.markdown('''
        <div style='margin-top: 50px; padding: 15px; background: #f8f9fa; border-radius: 8px;'>
            <p style='font-size: 12px; color: #6c757d; margin: 0;'>© 2026 Resume Gap Analyzer</p>
            <p style='font-size: 11px; color: #adb5bd; margin: 5px 0 0 0;'>Professional Resume Analysis Tool</p>
        </div>
    ''', unsafe_allow_html=True)

    if choice == "User":
        st.markdown("### Upload Your Resume")
        st.markdown("Upload your resume in PDF format to get personalized analysis and recommendations.")
        
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        
        if uploaded_file is not None:
            # Save the uploaded file temporarily
            with open("temp_resume.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.success("File uploaded successfully!")
            
            # Parse the resume
            try:
                data = ResumeParser("temp_resume.pdf").get_extracted_data()
                
                if data:
                    st.markdown("### Resume Analysis Results")
                    
                    # Display extracted information
                    if data.get('name'):
                        st.markdown(f"**Name:** {data['name']}")
                    
                    if data.get('email'):
                        st.markdown(f"**Email:** {data['email']}")
                    
                    if data.get('mobile_number'):
                        st.markdown(f"**Phone:** {data['mobile_number']}")
                    
                    if data.get('skills'):
                        st.markdown("**Skills Detected:**")
                        skills = data['skills']
                        if isinstance(skills, list):
                            st.write(", ".join(skills))
                        else:
                            st.write(skills)
                    
                    if data.get('college_name'):
                        st.markdown(f"**Education:** {data['college_name']}")
                    
                    if data.get('degree'):
                        st.markdown(f"**Degree:** {data['degree']}")
                    
                    if data.get('experience'):
                        st.markdown("**Experience:**")
                        st.write(data['experience'])
                    
                    if data.get('total_experience'):
                        st.markdown(f"**Total Experience:** {data['total_experience']} years")
                    
                    if data.get('no_of_pages'):
                        st.markdown(f"**Resume Pages:** {data['no_of_pages']}")
                    
                    # Course recommendations based on skills
                    if data.get('skills'):
                        skills_list = data['skills'] if isinstance(data['skills'], list) else [data['skills']]
                        
                        # Simple skill-based course recommendations
                        st.markdown("### Recommended Courses")
                        
                        # Check for different skill categories
                        ds_skills = ['python', 'machine learning', 'data science', 'tensorflow', 'numpy', 'pandas']
                        web_skills = ['html', 'css', 'javascript', 'react', 'nodejs', 'angular']
                        android_skills = ['android', 'java', 'kotlin', 'mobile']
                        ios_skills = ['ios', 'swift', 'objective-c', 'iphone']
                        
                        if any(skill.lower() in [s.lower() for s in skills_list] for skill in ds_skills):
                            st.markdown("**Data Science Courses:**")
                            course_recommender(ds_course)
                        
                        if any(skill.lower() in [s.lower() for s in skills_list] for skill in web_skills):
                            st.markdown("**Web Development Courses:**")
                            course_recommender(web_course)
                        
                        if any(skill.lower() in [s.lower() for s in skills_list] for skill in android_skills):
                            st.markdown("**Android Development Courses:**")
                            course_recommender(android_course)
                        
                        if any(skill.lower() in [s.lower() for s in skills_list] for skill in ios_skills):
                            st.markdown("**iOS Development Courses:**")
                            course_recommender(ios_course)
                    
                    # Show PDF preview
                    st.markdown("### Resume Preview")
                    show_pdf("temp_resume.pdf")
                    
                else:
                    st.error("Could not extract data from the resume. Please ensure it's a valid PDF resume.")
                    
            except Exception as e:
                st.error(f"Error processing resume: {str(e)}")
            
            # Clean up temporary file
            if os.path.exists("temp_resume.pdf"):
                os.remove("temp_resume.pdf")
    
    elif choice == "Feedback":
        st.markdown("### Feedback")
        st.markdown("We value your feedback! Please share your experience with our Resume Analyzer.")
        
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        feedback = st.text_area("Your Feedback", height=150)
        
        if st.button("Submit Feedback"):
            if name and email and feedback:
                st.success("Thank you for your feedback! We appreciate your input.")
                # In a real application, this would be saved to database
            else:
                st.error("Please fill in all fields.")
    
    elif choice == "About":
        st.markdown("### About Resume Gap Analyzer")
        st.markdown("""
        **Resume Gap Analyzer** is a professional tool designed to help job seekers analyze their resumes 
        and get personalized recommendations for career improvement.
        
        **Features:**
        - 📄 Resume parsing and analysis
        - 🎯 Skill extraction and identification
        - 📚 Personalized course recommendations
        - 📊 Resume scoring and optimization tips
        - 🔍 Experience analysis
        - 📱 Mobile-friendly interface
        
        **How it works:**
        1. Upload your resume in PDF format
        2. Our AI analyzes your skills, experience, and education
        3. Get personalized recommendations for courses and improvements
        4. Download your analysis results
        
        **Technologies Used:**
        - Streamlit for the web interface
        - NLTK for natural language processing
        - Resume Parser for PDF extraction
        - Plotly for data visualization
        
        **Contact:**
        - Developer: dnoobnerd
        - Website: https://dnoobnerd.netlify.app
        """)
    
    elif choice == "Admin":
        st.markdown("### Admin Panel")
        st.markdown("Admin functionality requires database connection. This is a standalone version.")
        st.info("Database features are disabled in this standalone version. For full admin functionality, please set up MySQL database.")
        
        # Show some demo analytics
        st.markdown("### Demo Analytics")
        st.info("These are demo statistics. Real analytics require database connection.")
        
        # Create some demo data for visualization
        demo_data = pd.DataFrame({
            'Category': ['Data Science', 'Web Development', 'Mobile Dev', 'UI/UX', 'Other'],
            'Count': [35, 28, 15, 12, 10]
        })
        
        fig = px.pie(demo_data, values='Count', names='Category', title='Demo: Resume Categories Distribution')
        st.plotly_chart(fig)


# Calling the main (run()) function to make the whole process run
if __name__ == "__main__":
    run()
