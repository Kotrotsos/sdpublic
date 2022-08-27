
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import warnings
import io
import os
from PIL import Image
import streamlit as st
"""
## Welcome to our Stable Diffusion Model!
Use the input fields in the sidebar on the left to control what is generated.
"""
 
stability_api = client.StabilityInference(
    key='sk-FIsaJ5SntlvgL4ViaClOzupfGqHY3Lsp8HjGuIYN1lnQoAiY', 
    verbose=True
)


options = st.sidebar.multiselect(
     'Assemble a description',
     ['A fierce', 'A young', 'Duck', 'Tomato', 'Running', 'Waddling', 'boy', 'girl', 'high-resolution'])

txt = st.sidebar.text_area('Or write out the description yourself.', ' '.join(options))

if st.sidebar.button('Generate image from this description'):
    answers = stability_api.generate(
        prompt=txt
    )
    with st.spinner('wait for it...'):
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    warnings.warn(
                        "Your request activated the API's safety filters and could not be processed."
                        "Please modify the prompt and try again.")
                if artifact.type == generation.ARTIFACT_IMAGE:
                    img = Image.open(io.BytesIO(artifact.binary))
                    st.image(img)