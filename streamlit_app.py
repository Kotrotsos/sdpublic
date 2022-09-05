
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import warnings
import io
import os
from PIL import Image
import streamlit as st


hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden; display:none;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)



"""
## Welcome to Dream. Proof of Concept!
Use the input fields in the sidebar on the left to control what is generated.
On mobile click the arrow in the top left to open the sidebar. Close it again to see the
image. 
"""
 
stability_api = client.StabilityInference(
    key=st.secrets["key"], 
    verbose=True
)

# st.code(st.secrets["key"])
option = st.sidebar.selectbox(
     'Select a template?',
     ('', 'Synthwave car', 'HR Gigeresque landscape', 'Van Gogh painting'))

st.sidebar.write('You selected:', option)
options = st.sidebar.multiselect('Assemble a description by choosing features', ["Car", "Beautiful girl", "Landscape", "River", "A man", "Skyline", "Highly detailed","surrealism","trending on art station","triadic color scheme","smooth","sharp focus","matte","elegant","the most beautiful image ever seen","illustration","digital paint","dark","gloomy","octane render","8k","4k","washed colors","sharp","dramatic lighting","beautiful","post processing","picture of the day","ambient lighting","epic composition"])
 


if option == 'Synthwave car':
    template = "Car Synthwave Highly detailed, surrealism, trending on art station, triadic color scheme, smooth, sharp focus, matte, elegant, the most beautiful image ever seen, illustration, digital paint, dark, gloomy, octane render, 8k, 4k, washed colors, sharp, dramatic lighting, beautiful, post processing, picture of the day, ambient lighting, epic composition"
elif option == 'HR Gigeresque landscape':
    template = "Alien landscape by HR Giger,sharp focus, matte, elegant, the most beautiful image ever seen. High Quality. Ultra Realistic."
elif option == 'Van Gogh painting':
    template = "Painting by Vincent Van Gogh"
else:
    template = ""




if template == "":
    txt = st.sidebar.text_area('Or write out the description yourself.',', '.join(options),placeholder='A River flows into a lake. High Quality Art.')
else:
     txt = st.sidebar.text_area('Or write out the description yourself.',template,placeholder='A River flows into a lake. High Quality Art.')



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
                    st.text('Generate a new image when the image is blury or has a low quality.')