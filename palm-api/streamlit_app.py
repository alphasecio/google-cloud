import os, validators, vertexai, streamlit as st
from langchain.document_loaders import UnstructuredURLLoader
from vertexai.preview.language_models import TextGenerationModel

# Streamlit app
st.subheader('Palmfish')

# Create a file upload widget for the credentials JSON file
with st.sidebar:
    creds_file = st.file_uploader("Upload Google Cloud credentials file", type="json")

# If the user has uploaded a file, read its contents and set the GOOGLE_APPLICATION_CREDENTIALS environment variable
if creds_file is not None:
    creds_contents = creds_file.read().decode("utf-8")
    with open("temp_credentials.json", "w") as f:
        f.write(creds_contents)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "temp_credentials.json"

    with st.sidebar:
        option = st.selectbox("Select your option", ["Answer Question", "Summarize Text", "Summarize URL"])

    if option == "Answer Question":
        prompt = st.text_input("Your Question")

        if st.button("Submit"):
            if not prompt.strip():
                st.error("Please submit your question.")
            else:
                try:
                    with st.spinner('Please wait...'):
                        model = TextGenerationModel.from_pretrained("text-bison@001")
                        response = model.predict(
                            prompt,
                            temperature=0.1,
                            max_output_tokens=256
                        )

                        st.success(response)
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    elif option == "Summarize Text":
        source_text = st.text_area("Source Text", height=200)
        prompt = 'Provide a summary within 200 words for the following article: \n' + source_text + '\nSummary: '

        if st.button("Summarize"):
            if not source_text.strip():
                st.error("Please provide the text to summarize.")
            else:
                try:
                    with st.spinner('Please wait...'):
                        model = TextGenerationModel.from_pretrained("text-bison@001")
                        response = model.predict(
                            prompt,
                            temperature=0.2,
                            max_output_tokens=256,
                            top_k=40,
                            top_p=0.8,
                        )

                        st.success(response)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
    
    elif option == "Summarize URL":
        url = st.text_input("Source URL")

        if st.button("Summarize"):
            if not url.strip():
                st.error("Please provide the URL to summarize.")
            elif not validators.url(url):
                st.error("Please provide a valid URL.")
            else:
                try:
                    with st.spinner('Please wait...'):
                        text = ""
                        loader = UnstructuredURLLoader(urls=[url])
                        data = loader.load()
                        for i in range(len(data)):
                            text += data[i].page_content
                        
                        prompt = 'Provide a summary within 250-300 words for the following article: \n' + text + '\nSummary: '
                        model = TextGenerationModel.from_pretrained("text-bison@001")
                        response = model.predict(
                            prompt,
                            temperature=0.2,
                            max_output_tokens=256,
                            top_k=40,
                            top_p=0.8,
                        )

                        st.success(response)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
