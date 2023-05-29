import os, streamlit as st
import vertexai, google.cloud.dlp_v2
from vertexai.preview.language_models import TextGenerationModel

# Streamlit app
st.subheader('Summarize Lah!')

# Create a file upload widget for the credentials JSON file
with st.sidebar:
    st.subheader('Settings')
    creds_file = st.file_uploader("Google Cloud credentials file", type="json")
    project_id = st.text_input("Google Cloud project id")
    dlp_enabled = st.checkbox("Scan for sensitive data")
    st.caption("Uses DLP API to scan for the following identifiers:\n* Credit Card Number\n* Email Address")

source_text = st.text_area("Source text", height=200, label_visibility="collapsed")

def inspect():
    dlp = google.cloud.dlp_v2.DlpServiceClient()
    info_types = [
        {"name":"CREDIT_CARD_NUMBER"},
        {"name":"EMAIL_ADDRESS"}
    ]
    inspect_config = {"info_types": info_types}
    item = {"value": source_text}
    parent = f"projects/{project_id}"
    response = dlp.inspect_content(
        request={"parent": parent, "inspect_config": inspect_config, "item": item}
    )

    findings_list = []
    if response.result.findings:
        for finding in response.result.findings:
            finding_dict = {'Info type': finding.info_type.name, 'Likelihood': finding.likelihood.name}
            findings_list.append(finding_dict)
    
    return findings_list

def summarize():
    with st.spinner("Please wait..."):
        prompt = 'Provide a summary within 200 words for the following article: \n' + source_text + '\nSummary: '
        model = TextGenerationModel.from_pretrained("text-bison@001")
        response = model.predict(
            prompt,
            temperature=0.2,
            max_output_tokens=256,
            top_k=40,
            top_p=0.8,
        )
        st.success(response)

if st.button("Summarize"):
    if creds_file is None:
        st.error("Please provide the JSON credentials file.")
    elif not project_id.strip():
        st.error("Please provide the project id.")
    elif not source_text.strip():
        st.error("Please provide the text to summarize.")
    else:
        try:
            # If the user has uploaded a file, read its contents and set the GOOGLE_APPLICATION_CREDENTIALS environment variable
            creds_contents = creds_file.read().decode("utf-8")
            with open("temp_credentials.json", "w") as f:
                f.write(creds_contents)
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "temp_credentials.json"
        except Exception as e:
            st.exception(f"An error occurred: {e}")

        if dlp_enabled:
            try:
                findings = inspect()
                if len(findings) > 0:
                    findings_str = "\n\n".join([f"Info type: {finding['Info type']}, Likelihood: {finding['Likelihood']}" for finding in findings])
                    st.error(f"Sensitive info found:\n\n{findings_str}")
                else:
                    summarize()
            except Exception as e:
                st.exception(f"An error occurred: {e}")
        else:
            try:
                summarize()
            except Exception as e:
                st.exception(f"An error occurred: {e}")
