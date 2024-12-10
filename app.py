import streamlit as st
import google.generativeai as genai
import PyPDF2 as pdf
from dotenv import load_dotenv
import os

load_dotenv() 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text



### Input Prompt for model
input_prompt = """
Hey , act like an advanced and experienced Application Tracking System (ATS) with a deep understanding on fields like AI Enginner, Data Science
Data Analytics, Business Analyst, Data Engineer and Machine Learning Engineer. Your task is to evaluate the candidate's resume based on the attached 
Job Description and uploaded resume. You must consider the challenges in the current job market especially for freshers and early career and also
consider the location and overseas visa requirements. Assign the percentage match and missing keywords along with necessary changes to be done before applying.
resume : {text}
description : {jd}

I want the response in one single string in the below format
{{"JD Match": "%", 
  "Missing Keywords:[]", 
  "Profile Summary" : ""}}

"""

#### App Code
st.title("Profile Evaluator")
st.text("Improve resume based on suggestions")
jd = st.text_area("Paste the job description")
uploaded_file = st.file_uploader("Upload your resume", type="pdf", help="Please upload the pdf file")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt)
        st.subheader(response)

