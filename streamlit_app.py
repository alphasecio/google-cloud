import os, vertexai, streamlit as st
from vertexai.preview.language_models import TextGenerationModel

# Streamlit app
st.title('Palmfish')

# Create a file upload widget for the credentials JSON file
creds_file = st.file_uploader("Upload Google Cloud credentials file", type="json")

# If the user has uploaded a file, read its contents and set the GOOGLE_APPLICATION_CREDENTIALS environment variable
if creds_file is not None:
    creds_contents = creds_file.read().decode("utf-8")
    with open("temp_credentials.json", "w") as f:
        f.write(creds_contents)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "temp_credentials.json"

    option = st.selectbox("Select Your Option", ["Answer Question", "Summarize Text"])

    if option == "Answer Question":
        prompt = st.text_input("Your Question")

        if st.button("Submit"):
            if not prompt.strip():
                st.write(f"Please submit your question.")
            else:
                try:
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
                st.write(f"Please provide the text to summarize.")
            else:
                try:
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
