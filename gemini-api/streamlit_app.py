import os, vertexai, streamlit as st
from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel

# Streamlit app
st.subheader("Gemini Playground")
with st.sidebar:
  creds_file = st.file_uploader("Google Cloud credentials file", type="json")
  google_cloud_project = st.text_input("Googe Cloud project")
  google_cloud_location = st.text_input("Google Cloud location")

prompt = st.text_input("Prompt", label_visibility="collapsed")

# If Generate button is clicked
if st.button("Generate"):
  if creds_file is None:
    st.error("Please provide the JSON credentials file.")
  elif not google_cloud_project.strip() or not google_cloud_location.strip() or not prompt.strip():
    st.error("Please provide the missing fields.")
  else:
    try:
      # Read the uploaded credentials file, and set the GOOGLE_APPLICATION_CREDENTIALS environment variable
      creds_contents = creds_file.read().decode("utf-8")
      with open("temp_credentials.json", "w") as f:
        f.write(creds_contents)
      os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "temp_credentials.json" 
    
      vertexai.init(project=google_cloud_project, location=google_cloud_location)    

      with st.spinner("Please wait..."):
        # Run Gemini 1.0 Pro model on Google Cloud
        model = GenerativeModel("gemini-1.0-pro")
        responses = model.generate_content(prompt, stream=False)
        st.success(responses.text)      
    except Exception as e:
      st.exception(f"Exception: {e}")
