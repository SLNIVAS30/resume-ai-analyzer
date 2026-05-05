# Resume AI Analyzer - Professional Resume Analysis Tool


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
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download NLTK data if not already downloaded
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


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
def course_recommender(course_list, slider_key):
    st.subheader("**Courses & Certificates Recommendations 👨‍🎓**")
    c = 0
    rec_course = []
    ## slider to choose from range 1-10
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 5, key=f"slider_{slider_key}")
    random.shuffle(course_list)
    for c_name, c_link in course_list:
        c += 1
        st.markdown(f"({c}) [{c_name}]({c_link})")
        rec_course.append(c_name)
        if c == no_of_reco:
            break
    return rec_course


# Simple resume parser that doesn't use pyresparser
def simple_resume_parser(file_path):
    try:
        # Extract text from PDF
        text = pdf_reader(file_path)
        
        # Debug: Show extracted text
        st.write("**Debug: Extracted Text (first 500 chars):**")
        st.text(text[:500])
        
        # Initialize result dictionary
        result = {
            'name': 'Unknown',
            'email': 'Not found',
            'mobile_number': 'Not found',
            'skills': [],
            'college_name': 'Not found',
            'degree': 'Not found',
            'experience': 'Not found',
            'total_experience': 0,
            'no_of_pages': 1
        }
        
        # Extract name (simple pattern matching)
        name_patterns = [
            r'([A-Z][a-z]+\s+[A-Z][a-z]+)',
            r'Name[:\s]*([A-Z][a-z]+\s+[A-Z][a-z]+)',
            r'CURRICULUM VITAE\s*([A-Z][a-z]+\s+[A-Z][a-z]+)'
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, text[:500])  # Search in first 500 chars
            if match:
                result['name'] = match.group(1).strip()
                break
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        if email_match:
            result['email'] = email_match.group(0)
        
        # Extract phone number
        phone_patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\b\d{10}\b',
            r'\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b'
        ]
        
        for pattern in phone_patterns:
            phone_match = re.search(pattern, text)
            if phone_match:
                result['mobile_number'] = phone_match.group(0)
                break
        
        # Enhanced skills extraction
        tech_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'nodejs', 'django', 'flask',
            'tensorflow', 'pytorch', 'machine learning', 'data science', 'sql', 'mongodb',
            'html', 'css', 'bootstrap', 'git', 'docker', 'aws', 'azure', 'gcp',
            'c++', 'c#', '.net', 'php', 'ruby', 'swift', 'kotlin', 'android', 'ios',
            'figma', 'adobe xd', 'photoshop', 'illustrator', 'ui', 'ux', 'design',
            'linux', 'ubuntu', 'windows', 'macos', 'office', 'excel', 'powerpoint',
            'numpy', 'pandas', 'scikit-learn', 'matplotlib', 'seaborn', 'jupyter',
            'tensorflow', 'keras', 'pytorch', 'nlp', 'deep learning', 'ai', 'ml',
            'mongodb', 'mysql', 'postgresql', 'database', 'nosql', 'redis',
            'git', 'github', 'gitlab', 'version control', 'ci/cd', 'jenkins',
            'docker', 'kubernetes', 'devops', 'microservices', 'api', 'rest',
            'html5', 'css3', 'sass', 'less', 'javascript', 'typescript', 'es6',
            'react', 'angular', 'vue', 'nodejs', 'express', 'npm', 'yarn',
            'java', 'spring', 'hibernate', 'maven', 'junit', 'jvm',
            'c++', 'c', 'gcc', 'makefile', 'cmake', 'algorithms',
            'c#', '.net', 'asp.net', 'entity framework', 'linq',
            'php', 'laravel', 'symfony', 'composer', 'wordpress',
            'ruby', 'rails', 'sinatra', 'bundler', 'gem',
            'swift', 'kotlin', 'android studio', 'xcode', 'ios',
            'flutter', 'react native', 'xamarin', 'cordova',
            'figma', 'sketch', 'adobe xd', 'invision', 'zeplin',
            'photoshop', 'illustrator', 'indesign', 'after effects',
            'aws', 'azure', 'gcp', 'heroku', 'digitalocean',
            'linux', 'ubuntu', 'centos', 'debian', 'bash', 'shell',
            'windows', 'powershell', 'cmd', 'batch',
            'macos', 'terminal', 'zsh', 'homebrew',
            'office', 'excel', 'word', 'powerpoint', 'outlook',
            'agile', 'scrum', 'kanban', 'jira', 'confluence',
            'testing', 'unit testing', 'integration testing', 'selenium',
            'security', 'authentication', 'authorization', 'oauth',
            'performance', 'optimization', 'caching', 'cdn'
        ]
        
        text_lower = text.lower()
        found_skills = []
        for skill in tech_skills:
            if skill in text_lower:
                found_skills.append(skill.title())
        
        result['skills'] = found_skills[:20]  # Limit to 20 skills
        
        # Debug: Show found skills
        st.write(f"**Debug: Found {len(found_skills)} skills:**")
        st.write(found_skills)
        
        # Extract education information
        education_patterns = [
            r'(B\.?[A-Z]*\.?[A-Z]*\s*[A-Za-z\s]+)',
            r'(M\.?[A-Z]*\.?[A-Z]*\s*[A-Za-z\s]+)',
            r'(PhD\s*[A-Za-z\s]+)',
            r'(Bachelor\s*[A-Za-z\s]+)',
            r'(Master\s*[A-Za-z\s]+)'
        ]
        
        for pattern in education_patterns:
            edu_match = re.search(pattern, text)
            if edu_match:
                result['degree'] = edu_match.group(1).strip()
                break
        
        # Extract college/university
        college_patterns = [
            r'(University\s*of\s*[A-Za-z\s]+)',
            r'([A-Za-z\s]+University)',
            r'([A-Za-z\s]+College)',
            r'([A-Za-z\s]+Institute)'
        ]
        
        for pattern in college_patterns:
            college_match = re.search(pattern, text)
            if college_match:
                result['college_name'] = college_match.group(1).strip()
                break
        
        # Extract experience section
        experience_section = re.search(r'(?:EXPERIENCE|WORK EXPERIENCE|PROFESSIONAL EXPERIENCE)(.*?)(?:EDUCATION|SKILLS|PROJECTS|$)', text, re.DOTALL | re.IGNORECASE)
        if experience_section:
            result['experience'] = experience_section.group(1).strip()[:500]  # Limit to 500 chars
        
        # Calculate total experience (simple estimation)
        year_patterns = [
            r'(\d+)\s*years?',
            r'(\d{4})\s*-\s*(\d{4})',
            r'(\d{4})\s*-\s*present'
        ]
        
        total_exp = 0
        for pattern in year_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple) and len(match) == 2:
                    try:
                        start_year = int(match[0])
                        if match[1].lower() == 'present':
                            end_year = 2026
                        else:
                            end_year = int(match[1])
                        total_exp += (end_year - start_year)
                    except:
                        pass
                elif isinstance(match, str):
                    try:
                        total_exp += int(match)
                    except:
                        pass
        
        result['total_experience'] = min(total_exp, 50)  # Cap at 50 years
        
        # Count pages (simple estimation)
        page_count = text.count('\x0c') + 1  # Form feed character indicates page break
        result['no_of_pages'] = page_count
        
        return result
        
    except Exception as e:
        st.error(f"Error parsing resume: {str(e)}")
        return None


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

# Skill Gap Detection System
def detect_skill_gaps(user_skills):
    """
    Detect skill gaps for different career paths based on user's current skills
    """
    
    # Define required skills for different career paths
    career_paths = {
        "Data Scientist": {
            "required_skills": [
                "Python", "Machine Learning", "Data Science", "Statistics", 
                "SQL", "TensorFlow", "PyTorch", "Numpy", "Pandas", 
                "Scikit-learn", "Data Visualization", "Deep Learning", "AI", "ML",
                "Jupyter", "Matplotlib", "Seaborn", "NLP", "Big Data", "Hadoop"
            ],
            "priority_skills": ["Python", "Machine Learning", "Statistics", "SQL", "TensorFlow"],
            "description": "Data Science and Machine Learning roles"
        },
        "Full Stack Developer": {
            "required_skills": [
                "HTML", "CSS", "JavaScript", "React", "Node.js", "Python", 
                "SQL", "MongoDB", "Git", "Docker", "REST", "API", 
                "TypeScript", "Angular", "Vue", "Express", "MySQL", "PostgreSQL",
                "Bootstrap", "Sass", "Webpack", "Testing", "CI/CD"
            ],
            "priority_skills": ["JavaScript", "React", "Node.js", "Python", "SQL"],
            "description": "Full Stack Web Development"
        },
        "Mobile App Developer": {
            "required_skills": [
                "Android", "iOS", "Swift", "Kotlin", "Java", "React Native", 
                "Flutter", "Mobile", "Xcode", "Android Studio", "API", "REST",
                "Firebase", "SQLite", "Git", "Docker", "TypeScript", "JavaScript"
            ],
            "priority_skills": ["Android", "iOS", "Swift", "Kotlin", "React Native"],
            "description": "Mobile Application Development"
        },
        "UI/UX Designer": {
            "required_skills": [
                "Figma", "Adobe XD", "UI", "UX", "Design", "Prototyping", 
                "Wireframes", "Photoshop", "Illustrator", "Sketch", "InVision",
                "User Research", "Interaction Design", "Visual Design", "Typography",
                "Color Theory", "Responsive Design", "Adobe Creative Suite"
            ],
            "priority_skills": ["Figma", "Adobe XD", "UI", "UX", "Prototyping"],
            "description": "User Interface and User Experience Design"
        },
        "DevOps Engineer": {
            "required_skills": [
                "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Linux", 
                "CI/CD", "Jenkins", "Git", "Terraform", "Ansible", "Python",
                "Bash", "Shell", "Monitoring", "Security", "Networking", "API",
                "Microservices", "Cloud Computing", "DevOps"
            ],
            "priority_skills": ["Docker", "Kubernetes", "AWS", "Linux", "CI/CD"],
            "description": "DevOps and Cloud Infrastructure"
        },
        "Backend Developer": {
            "required_skills": [
                "Python", "Java", "Node.js", "SQL", "API", "REST", 
                "MongoDB", "MySQL", "PostgreSQL", "Docker", "Git", "Microservices",
                "Authentication", "Security", "Caching", "Performance", "Testing",
                "Redis", "GraphQL", "Express", "Spring", "Django"
            ],
            "priority_skills": ["Python", "Java", "SQL", "API", "Docker"],
            "description": "Backend Development and APIs"
        }
    }
    
    # Normalize user skills to lowercase for comparison
    user_skills_lower = [skill.lower() for skill in user_skills]
    
    gap_analysis = {}
    
    for career_path, details in career_paths.items():
        required_skills = details["required_skills"]
        priority_skills = details["priority_skills"]
        
        # Find missing skills
        missing_skills = []
        missing_priority_skills = []
        
        for skill in required_skills:
            if skill.lower() not in user_skills_lower:
                missing_skills.append(skill)
                
        for skill in priority_skills:
            if skill.lower() not in user_skills_lower:
                missing_priority_skills.append(skill)
        
        # Calculate match percentage
        total_required = len(required_skills)
        matched_skills = total_required - len(missing_skills)
        match_percentage = (matched_skills / total_required) * 100 if total_required > 0 else 0
        
        # Calculate priority match percentage
        total_priority = len(priority_skills)
        matched_priority = total_priority - len(missing_priority_skills)
        priority_match_percentage = (matched_priority / total_priority) * 100 if total_priority > 0 else 0
        
        gap_analysis[career_path] = {
            "match_percentage": round(match_percentage, 1),
            "priority_match_percentage": round(priority_match_percentage, 1),
            "missing_skills": missing_skills,
            "missing_priority_skills": missing_priority_skills,
            "matched_skills": [skill for skill in required_skills if skill.lower() in user_skills_lower],
            "total_required": total_required,
            "description": details["description"]
        }
    
    return gap_analysis

def generate_gap_recommendations(gap_analysis, user_skills):
    """
    Generate personalized recommendations based on skill gaps
    """
    recommendations = []
    
    # Sort career paths by match percentage
    sorted_careers = sorted(gap_analysis.items(), key=lambda x: x[1]["match_percentage"], reverse=True)
    
    for career_path, analysis in sorted_careers:
        match_pct = analysis["match_percentage"]
        priority_match_pct = analysis["priority_match_percentage"]
        missing_priority_skills = analysis["missing_priority_skills"]
        
        if match_pct >= 70:
            level = "Excellent Match"
            color = "🟢"
            advice = f"You have strong skills for {career_path}! Focus on advanced topics."
        elif match_pct >= 50:
            level = "Good Match"
            color = "🟡"
            advice = f"You have a good foundation for {career_path}. Focus on missing priority skills."
        elif match_pct >= 30:
            level = "Moderate Match"
            color = "🟠"
            advice = f"You have some relevant skills for {career_path}. Consider learning the priority skills first."
        else:
            level = "Needs Development"
            color = "🔴"
            advice = f"You'll need significant skill development for {career_path}. Start with the fundamentals."
        
        recommendations.append({
            "career_path": career_path,
            "level": level,
            "color": color,
            "match_percentage": match_pct,
            "priority_match_percentage": priority_match_pct,
            "missing_priority_skills": missing_priority_skills[:5],  # Show top 5 missing priority skills
            "total_missing": len(analysis["missing_skills"]),
            "advice": advice,
            "description": analysis["description"]
        })
    
    return recommendations

# AI Chat Assistant System
class ResumeChatAssistant:
    def __init__(self):
        self.conversation_history = []
        self.resume_data = None
        
    def get_response(self, user_message, resume_data=None):
        """
        Generate AI response based on user message and resume context
        """
        if resume_data:
            self.resume_data = resume_data
            
        user_message_lower = user_message.lower()
        
        # Resume building tips
        if any(keyword in user_message_lower for keyword in ['resume', 'cv', 'build', 'create', 'write']):
            return self.get_resume_tips(user_message_lower)
        
        # Skills and career advice
        elif any(keyword in user_message_lower for keyword in ['skill', 'career', 'job', 'learn', 'improve']):
            return self.get_career_advice(user_message_lower)
        
        # Interview preparation
        elif any(keyword in user_message_lower for keyword in ['interview', 'question', 'prepare', 'tips']):
            return self.get_interview_tips(user_message_lower)
        
        # Course recommendations
        elif any(keyword in user_message_lower for keyword in ['course', 'learn', 'study', 'training']):
            return self.get_course_recommendations(user_message_lower)
        
        # General help
        elif any(keyword in user_message_lower for keyword in ['help', 'hello', 'hi', 'guide']):
            return self.get_help_response()
        
        # Specific technical questions
        elif any(keyword in user_message_lower for keyword in ['python', 'java', 'javascript', 'react', 'data science']):
            return self.get_technical_advice(user_message_lower)
        
        else:
            return self.get_general_response(user_message_lower)
    
    def get_resume_tips(self, message):
        tips = [
            "📝 **Resume Writing Tips:**\n• Keep it concise (1-2 pages max)\n• Use action verbs and quantifiable achievements\n• Tailor it to each job application\n• Include relevant keywords from job descriptions",
            "🎯 **Key Resume Sections:**\n• Contact Information (name, email, phone)\n• Professional Summary/Objective\n• Work Experience with achievements\n• Education & Certifications\n• Skills section (technical & soft skills)\n• Projects (if applicable)",
            "✨ **Resume Best Practices:**\n• Use professional formatting\n• Proofread for errors\n• Save as PDF for applications\n• Include LinkedIn profile URL\n• Use consistent date formatting"
        ]
        
        if 'format' in message:
            return "📋 **Resume Format:**\n• Use clean, professional layout\n• Choose readable fonts (Arial, Calibri, Times New Roman)\n• Use bullet points for achievements\n• Maintain consistent spacing\n• Keep margins between 0.5-1 inch"
        
        if 'skill' in message:
            return "🎯 **Skills Section Tips:**\n• List technical skills first\n• Include proficiency levels\n• Group similar skills together\n• Mention relevant certifications\n• Keep it updated with new skills"
        
        return random.choice(tips)
    
    def get_career_advice(self, message):
        if self.resume_data and self.resume_data.get('skills'):
            skills = self.resume_data['skills']
            skill_count = len(skills) if isinstance(skills, list) else 1
            
            advice = f"🚀 **Career Advice Based on Your Resume:**\n\n"
            advice += f"You have {skill_count} skills detected. "
            
            if skill_count < 5:
                advice += "Consider developing more technical skills to increase your opportunities. "
            elif skill_count < 10:
                advice += "You have a good foundation. Focus on deepening your expertise in key areas. "
            else:
                advice += "You have diverse skills! Consider specializing in 2-3 key areas. "
            
            advice += "\n\n**Next Steps:**\n• Identify your target career path\n• Focus on missing priority skills\n• Build projects to showcase your abilities\n• Network with professionals in your field"
            
            return advice
        else:
            return "💡 **Career Development Tips:**\n• Identify your strengths and interests\n• Research growing industries and roles\n• Develop both technical and soft skills\n• Build a portfolio of projects\n• Seek mentorship and networking opportunities\n• Stay updated with industry trends"
    
    def get_interview_tips(self, message):
        tips = [
            "🎤 **Interview Preparation:**\n• Research the company and role\n• Prepare answers to common questions\n• Practice with mock interviews\n• Prepare questions to ask the interviewer\n• Dress professionally and arrive early",
            "💬 **Common Interview Questions:**\n• 'Tell me about yourself'\n• 'Why do you want this job?'\n• 'What are your strengths/weaknesses?'\n• 'Describe a challenging situation you handled'\n• 'Where do you see yourself in 5 years?'",
            "🎯 **Interview Success Tips:**\n• Use the STAR method for behavioral questions\n• Provide specific examples with results\n• Show enthusiasm and confidence\n• Follow up with a thank-you email\n• Be honest and authentic"
        ]
        
        if 'technical' in message:
            return "🔧 **Technical Interview Tips:**\n• Review fundamental concepts\n• Practice coding challenges\n• Explain your thought process\n• Ask clarifying questions\n• Be prepared for system design questions"
        
        return random.choice(tips)
    
    def get_course_recommendations(self, message):
        recommendations = [
            "📚 **Learning Platforms:**\n• Coursera - University-level courses\n• Udemy - Practical skills and tutorials\n• edX - Free courses from top universities\n• Pluralsight - Technology skills\n• LinkedIn Learning - Professional development",
            "🎓 **Course Selection Tips:**\n• Check reviews and ratings\n• Look for hands-on projects\n• Verify instructor credentials\n• Consider time commitment\n• Check prerequisites",
            "📖 **Free Learning Resources:**\n• YouTube tutorials\n• GitHub repositories\n• Stack Overflow\n• FreeCodeCamp\n• MIT OpenCourseWare"
        ]
        
        if 'data science' in message:
            return "📊 **Data Science Learning Path:**\n• Python programming\n• Statistics and probability\n• Machine learning fundamentals\n• Data visualization tools\n• SQL and database management\n• Deep learning frameworks"
        
        if 'web development' in message:
            return "🌐 **Web Development Learning Path:**\n• HTML, CSS, JavaScript fundamentals\n• Frontend framework (React, Angular, or Vue)\n• Backend development (Node.js, Python, or Java)\n• Database management\n• Version control with Git"
        
        return random.choice(recommendations)
    
    def get_help_response(self):
        return """🤖 **AI Resume Assistant - How I Can Help:**

**Resume Building:**
• Resume writing tips and best practices
• Format and structure guidance
• Skills section optimization

**Career Guidance:**
• Career path recommendations
• Skill development advice
• Job search strategies

**Interview Preparation:**
• Common interview questions
• Technical interview tips
• Mock interview guidance

**Learning Resources:**
• Course recommendations
• Learning platform suggestions
• Free resources and tutorials

**Technical Support:**
• Programming language advice
• Technology stack guidance
• Project ideas

Just ask me anything about resumes, careers, or skill development!"""
    
    def get_technical_advice(self, message):
        if 'python' in message:
            return "🐍 **Python Learning Path:**\n• Start with basics (variables, data types, control flow)\n• Learn object-oriented programming\n• Master popular libraries (NumPy, Pandas, Matplotlib)\n• Practice with real projects\n• Explore frameworks (Django, Flask, FastAPI)"
        
        if 'javascript' in message:
            return "🌐 **JavaScript Learning Path:**\n• Master fundamentals (variables, functions, objects)\n• Learn DOM manipulation\n• Study modern ES6+ features\n• Pick a framework (React, Angular, or Vue)\n• Build interactive projects"
        
        if 'data science' in message:
            return "📊 **Data Science Career Path:**\n• Strong foundation in statistics and mathematics\n• Python programming with data science libraries\n• Machine learning algorithms and concepts\n• Data visualization and communication skills\n• Domain knowledge in your industry"
        
        return "💻 **Technical Career Advice:**\n• Focus on fundamentals first\n• Build practical projects\n• Contribute to open source\n• Stay updated with industry trends\n• Network with other developers"
    
    def get_general_response(self, message):
        responses = [
            "I'm here to help with your resume and career development! Ask me about resume writing, interview tips, career guidance, or skill development.",
            "I can provide personalized advice based on your resume. Upload your resume and ask specific questions about your career path.",
            "Need help with your job search? I can assist with resume optimization, interview preparation, and career planning.",
            "Looking to improve your skills? I can recommend learning paths and resources based on your career goals."
        ]
        
        return random.choice(responses)

# Initialize chat assistant
chat_assistant = ResumeChatAssistant()

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
    activities = ["User", "AI Assistant", "Feedback", "About", "Admin"]
    choice = st.sidebar.selectbox("Select an option:", activities)
    st.sidebar.markdown('''
        <div style='margin-top: 50px; padding: 15px; background: #f8f9fa; border-radius: 8px;'>
            <p style='font-size: 12px; color: #6c757d; margin: 0;'>© 2026 Resume Gap Analyzer</p>
            <p style='font-size: 11px; color: #adb5bd; margin: 5px 0 0 0;'>Professional Resume Analysis Tool</p>
        </div>
    ''', unsafe_allow_html=True)

    if choice == "AI Assistant":
        st.markdown("### 🤖 AI Resume Assistant")
        st.markdown("Get personalized career guidance, resume tips, and skill development advice from our AI assistant.")
        
        # Initialize session state for chat history
        if 'chat_messages' not in st.session_state:
            st.session_state.chat_messages = []
            # Add welcome message
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": "👋 Hello! I'm your AI Resume Assistant. I can help you with:\n\n• Resume writing and formatting\n• Career guidance and path recommendations\n• Interview preparation tips\n• Skill development advice\n• Course recommendations\n\nFeel free to ask me anything about your career development!"
            })
        
        # Display chat messages
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.chat_messages:
                if message["role"] == "user":
                    st.markdown(f"""
                    <div style='margin: 10px 0; padding: 10px; background: #e3f2fd; border-radius: 10px; border-left: 4px solid #2196f3;'>
                        <strong>You:</strong> {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='margin: 10px 0; padding: 15px; background: #f8f9fa; border-radius: 10px; border-left: 4px solid #667eea;'>
                        <strong>🤖 AI Assistant:</strong><br>
                        {message["content"].replace('\n', '<br>')}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Chat input
        st.markdown("### Ask me anything:")
        
        # Create columns for input and send button
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_input = st.text_input("Type your question here...", key="chat_input", placeholder="e.g., How should I format my resume?")
        
        with col2:
            send_button = st.button("Send", key="send_button")
        
        # Quick question buttons
        st.markdown("### Quick Questions:")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("Resume Tips", key="resume_tips"):
                user_input = "How can I improve my resume?"
                # Add user message to chat
                st.session_state.chat_messages.append({
                    "role": "user",
                    "content": user_input
                })
                # Get AI response
                ai_response = chat_assistant.get_response(user_input)
                # Add AI response to chat
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": ai_response
                })
                st.rerun()
        
        with col2:
            if st.button("Career Advice", key="career_advice"):
                user_input = "What career path should I choose?"
                # Add user message to chat
                st.session_state.chat_messages.append({
                    "role": "user",
                    "content": user_input
                })
                # Get AI response
                ai_response = chat_assistant.get_response(user_input)
                # Add AI response to chat
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": ai_response
                })
                st.rerun()
        
        with col3:
            if st.button("Interview Help", key="interview_help"):
                user_input = "How should I prepare for interviews?"
                # Add user message to chat
                st.session_state.chat_messages.append({
                    "role": "user",
                    "content": user_input
                })
                # Get AI response
                ai_response = chat_assistant.get_response(user_input)
                # Add AI response to chat
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": ai_response
                })
                st.rerun()
        
        with col4:
            if st.button("Skill Learning", key="skill_learning"):
                user_input = "What skills should I learn?"
                # Add user message to chat
                st.session_state.chat_messages.append({
                    "role": "user",
                    "content": user_input
                })
                # Get AI response
                ai_response = chat_assistant.get_response(user_input)
                # Add AI response to chat
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": ai_response
                })
                st.rerun()
        
        # Process user input
        if send_button and user_input:
            # Add user message to chat
            st.session_state.chat_messages.append({
                "role": "user",
                "content": user_input
            })
            
            # Get AI response
            ai_response = chat_assistant.get_response(user_input)
            
            # Add AI response to chat
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": ai_response
            })
            
            # Clear input
            st.session_state.chat_input = ""
            
            # Rerun to update chat
            st.rerun()
        
        # Clear chat button
        if st.button("Clear Chat", key="clear_chat"):
            st.session_state.chat_messages = []
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": "👋 Chat cleared! How can I help you with your resume and career development?"
            })
            st.rerun()

    elif choice == "User":
        st.markdown("### Upload Your Resume")
        st.markdown("Upload your resume in PDF format to get personalized analysis and recommendations.")
        
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        
        if uploaded_file is not None:
            # Save the uploaded file temporarily
            with open("temp_resume.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.success("File uploaded successfully!")
            
            # Parse the resume using our simple parser
            try:
                data = simple_resume_parser("temp_resume.pdf")
                
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
                        st.write(data['experience'][:300] + "..." if len(data['experience']) > 300 else data['experience'])
                    
                    if data.get('total_experience'):
                        st.markdown(f"**Total Experience:** {data['total_experience']} years")
                    
                    if data.get('no_of_pages'):
                        st.markdown(f"**Resume Pages:** {data['no_of_pages']}")
                    
                    # Course recommendations based on skills
                    if data.get('skills'):
                        skills_list = data['skills'] if isinstance(data['skills'], list) else [data['skills']]
                        
                        # Skill Gap Detection Analysis
                        st.markdown("### 🎯 Skill Gap Analysis")
                        st.markdown("Analyzing your skills against different career paths...")
                        
                        # Perform gap analysis
                        gap_analysis = detect_skill_gaps(skills_list)
                        recommendations = generate_gap_recommendations(gap_analysis, skills_list)
                        
                        # Display gap analysis results
                        for rec in recommendations:
                            st.markdown(f"""
                            <div style='padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #667eea; background: #f8f9fa;'>
                                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;'>
                                    <h4 style='margin: 0; color: #333;'>{rec['color']} {rec['career_path']}</h4>
                                    <span style='font-size: 18px; font-weight: bold; color: #667eea;'>{rec['match_percentage']}%</span>
                                </div>
                                <p style='margin: 5px 0; color: #666; font-size: 14px;'>{rec['description']}</p>
                                <p style='margin: 5px 0; color: #333; font-weight: bold;'>{rec['level']}</p>
                                <p style='margin: 5px 0; color: #666;'>{rec['advice']}</p>
                                {f"<p style='margin: 5px 0; color: #d73b5c;'>Missing Priority Skills: {', '.join(rec['missing_priority_skills'])}</p>" if rec['missing_priority_skills'] else ""}
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Create gap analysis visualization
                        st.markdown("### 📊 Career Match Overview")
                        
                        # Prepare data for visualization
                        career_data = []
                        for rec in recommendations:
                            career_data.append({
                                'Career Path': rec['career_path'],
                                'Match %': rec['match_percentage'],
                                'Priority Match %': rec['priority_match_percentage'],
                                'Level': rec['level']
                            })
                        
                        df_career = pd.DataFrame(career_data)
                        
                        # Create bar chart
                        fig = px.bar(df_career, x='Career Path', y='Match %', 
                                     color='Level', title='Career Path Match Analysis',
                                     color_discrete_map={
                                         'Excellent Match': '#2ecc71',
                                         'Good Match': '#f39c12', 
                                         'Moderate Match': '#e67e22',
                                         'Needs Development': '#e74c3c'
                                     })
                        fig.update_layout(xaxis_tickangle=-45)
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Simple skill-based course recommendations
                        st.markdown("### Recommended Courses")
                        
                        # Check for different skill categories
                        ds_skills = ['python', 'machine learning', 'data science', 'tensorflow', 'numpy', 'pandas']
                        web_skills = ['html', 'css', 'javascript', 'react', 'nodejs', 'angular']
                        android_skills = ['android', 'java', 'kotlin', 'mobile']
                        ios_skills = ['ios', 'swift', 'objective-c', 'iphone']
                        
                        if any(skill.lower() in [s.lower() for s in skills_list] for skill in ds_skills):
                            st.markdown("**Data Science Courses:**")
                            course_recommender(ds_course, "data_science")
                        
                        if any(skill.lower() in [s.lower() for s in skills_list] for skill in web_skills):
                            st.markdown("**Web Development Courses:**")
                            course_recommender(web_course, "web_dev")
                        
                        if any(skill.lower() in [s.lower() for s in skills_list] for skill in android_skills):
                            st.markdown("**Android Development Courses:**")
                            course_recommender(android_course, "android")
                        
                        if any(skill.lower() in [s.lower() for s in skills_list] for skill in ios_skills):
                            st.markdown("**iOS Development Courses:**")
                            course_recommender(ios_course, "ios")
                    
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
        - PDF text extraction for resume parsing
        - Plotly for data visualization
        
        **Features:**
        - Resume parsing and analysis
        - Skill extraction and identification
        - Course recommendations
        - Resume scoring and optimization tips
        - Experience analysis
        - Mobile-friendly interface
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
