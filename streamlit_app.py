import vertexai, streamlit as st
from vertexai.preview.language_models import TextGenerationModel

# Initialize Vertex AI with the required variables
PROJECT_ID = '' # @param {type:"string"}
LOCATION = ''  # @param {type:"string"}
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Streamlit app
st.title('Palmfish')
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
    prompt = 'Provide a summary within 250 words for the following article: \n' + source_text + '\nSummary: '

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
     
