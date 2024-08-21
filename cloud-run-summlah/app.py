import os, validators, magic, vertexai, streamlit as st
import vertexai.generative_models as generative_models
from vertexai.generative_models import GenerativeModel
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader

st.set_page_config(page_title="Summarize Lah!")
st.subheader("Summarize Lah!")

col1, col2 = st.columns([4,1])
url = col1.text_input("URL", label_visibility="collapsed")
summarize = col2.button("Summarize")

gcp_project_id = os.getenv("PROJECT_ID")
gcp_location = os.getenv("LOCATION", "us-central1")  # Default to 'us-central1' if not set

vertexai.init(project=gcp_project_id, location=gcp_location)
model = GenerativeModel("gemini-1.5-flash-001")

if summarize:
    if not url.strip() or not validators.url(url):
        st.error("Please provide a valid URL.")
    else:
        try:
            with st.spinner("Please wait..."):
                text = ""
                if "youtube.com" in url:
                    loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
                else:
                    loader = UnstructuredURLLoader(urls=[url], ssl_verify=False, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
                data = loader.load()
                for i in range(len(data)):
                    text += data[i].page_content
                    
                prompt = "Write a summary of the following in 200-250 words: \n" + text + "\nSummary: "
                
                response = model.generate_content(prompt, stream=False)
                st.success(response.text) 
        except Exception as e:
            st.exception(f"Error: {e}")
