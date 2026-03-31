#Load necessary dependencies
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
import os 
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
import json

#loading the environment variables
load_dotenv()

#functionality to initialize gemini model and get response
def get_gemini_response(input:str,input_prompt:str):
    llm=ChatGoogleGenerativeAI(
        model=os.environ['GEMINI_MODEL'],
        temperature=0.5
    )
    response=llm.invoke([input,input_prompt])
    return response.content

# function to extract text from pdf in order to feed it to gemini model
def input_pdf_text(upload_file):
    with open("temp_uploaded_file.pdf","wb") as temp_file:
        temp_file.write(upload_file.read())

        #load the temporary stored pdf using PyPDFLoader
        loader=PyPDFLoader("temp_uploaded_file.pdf")
        docs=loader.load()
        text=""
        for page in range(len(docs)):
            page=docs[page]
            text+=str(page.page_content)
        return text

#prompt template for the ATS
input_prompt="""
Hey, act like a skilled or experienced ATS(Application Tracking System)
with deep understanding of tech field like software engineering, data science, data analyst, ai engineer and big data engineer.
your task is to evaluate the resume based on the given job description.
you must consider the job market is very competitve and you should provide best assistance for improving the resume.
Assign the percentage matching based on JD and the missing keyword with high accuracy.
resume:{text}
description:{jd}

I want response in one single string having the structure as below:
JD Match=%\n
MissingKeywords=[]\n
Profile Summary= ''
"""

#Initialize the streamlit app
st.set_page_config("LLM Based ATS System")
st.title("Smart ATS")
st.subheader("Prioritize beneficial placement for both sides")

st.text("Improve your resume according to ATS.")
jd=st.text_area("Paste the Job Description")
upload_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please Upload the pdf")

#if cv is not uploaded,it will throw error
if upload_file is not None:
    st.success("PDF Uploaded Successfully")
else:
    st.error("PDF not uploaded")

submit=st.button("Resume Percentage match with Job Description")

if submit:
    if upload_file is not None:
        text=input_pdf_text(upload_file)
        formatted_prompt=input_prompt.format(text=text,jd=jd)
        response=get_gemini_response(text,formatted_prompt)
        st.write(response)