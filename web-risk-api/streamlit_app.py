import os, streamlit as st
from google.cloud import webrisk_v1

# Streamlit app
st.title('Google Cloud Web Risk API')

# Create a file upload widget for the credentials JSON file
creds_file = st.file_uploader("Upload Google Cloud credentials file", type="json")

# If the user has uploaded a file, read its contents and set the GOOGLE_APPLICATION_CREDENTIALS environment variable
if creds_file is not None:
    creds_contents = creds_file.read().decode("utf-8")
    with open("temp_credentials.json", "w") as f:
        f.write(creds_contents)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "temp_credentials.json"

    # Get the URL or hash prefix inputs for lookup
    col1, col2 = st.columns(2)
    url_input = col1.text_input('Enter URL', value='')
    url_lookup = col1.button(key='LookupURL', label='Lookup')
    hash_input = col2.text_input('Enter hash prefix', value='')
    hash_lookup = col2.button(key='LookupHash', label='Lookup')
    
    # Initialize the WebRiskServiceClient and define the threat types
    client = webrisk_v1.WebRiskServiceClient()
    threat_types = [webrisk_v1.ThreatType.MALWARE,
                        webrisk_v1.ThreatType.SOCIAL_ENGINEERING,
                        webrisk_v1.ThreatType.SOCIAL_ENGINEERING_EXTENDED_COVERAGE,
                        webrisk_v1.ThreatType.UNWANTED_SOFTWARE]

    if url_lookup:
        if not url_input.strip():
            col1.write(f'Provide the URL for lookup.')    
        else:
            try:
                # Call the Lookup API for submitted URL
                response = client.search_uris(uri=url_input, threat_types=threat_types)
        
                if response.threat:
                    st.error(f'The URL `{url_input}` is associated with:\n - {response.threat.threat_types[0].name}')
                else:
                    st.success(f'The URL `{url_input}` appears safe.')
            except Exception as e:
                st.error(f"An error occurred: {e}")

    if hash_lookup:
        if not hash_input.strip():
            col2.write(f'Provide the hash prefix for lookup.')    
        else:
            try:
                # Call the Lookup API for submitted hash prefix
                response = client.search_hashes(hash_prefix=hash_input, threat_types=threat_types)

                if len(response.threats) > 0:
                    st.error(f'The hash prefix {hash_input} matched the following hashes:\n')
                    for threat_hash in response.threats:
                        st.write(threat_hash.hash)
                else:
                    st.success(f'The hash prefix {hash_input} appears safe.')
            except Exception as e:
                st.error(f"An error occurred: {e}")
