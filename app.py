from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#function to load gemini

model=genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input,image,prompt):
    response=model.generate_content([input,image[0],prompt])
    return response.text
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()
        
        image_part=[
            {
                "mime_type":uploaded_file.type,
                "data":bytes_data
            }
        ]
        return image_part
    else:
        raise FileNotFoundError("no file uploaded")
    
    
    

st.set_page_config(page_title="multilanguage invoive extractor")

st.header("Multilanguage Invoice Extractor")

input=st.text_input("input prompt:",key=input)
uploaded_file=st.file_uploader("choose an image", type=["jpg","jpeg","png"])
image=""

if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="uploadedfile",use_column_width=True)
    
submit=st.button("tell me about the invoice")

input_prompt="""
you are an expert in understanding invoices.we will upload a image as an invoice and you will have
to answer any question based on the uploaded invoice image

"""

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The response is")
    st.write(response)
    
    
