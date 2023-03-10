import os
import replicate
import streamlit as st
from deta import Deta  

st.set_page_config(
    page_title="Edit Image",
    # page_icon=im,
    layout="wide",
)

hide_menu = """
<style>
#MainMenu{
    visibility:hidden;
}
.css-14xtw13 e8zbici0{
    visibility:hidden;
}
.css-j7qwjs e1fqkh3o7{
    visibility:hidden;
}
footer{
    visibility:hidden;
}
</style>
"""
 
st.markdown(hide_menu , unsafe_allow_html=True)


# Initializing the Database
deta = Deta('a0ercjes3ku_wTUSCQJfNm8BuGaHSNMdXWRgDYzHNpEj')
db = deta.Base('image-processing')

def getItem():
    return db.fetch().items
######################### Frontend UI of the Application #########################

# App Title Name
st.title("Edit Image")

key = st.sidebar.text_input("Enter the Security Key")
auth = getItem()
if key == auth[1]["secretKey"]:
    st.sidebar.success("Welcome")
    # Initializing the database
    

    language = getItem()
    lang = st.sidebar.selectbox("Specify the Page Language",("Dutch","English","French","Spanish","German"))

    if lang == "Dutch":
        st.markdown(language[2]["dutch"])
    elif lang == "English":
        st.markdown(language[2]["english"])
    elif lang == "French":
        st.markdown(language[2]["french"])
    elif lang == "Spanish":
        st.markdown(language[2]["spanish"])
    else:
        st.markdown(language[2]["german"])

    st.sidebar.write("__________________________")
    st.write("______________________________________________________________________________________________________________________")

    # Image resizing tools
    imageResize = '[Image Resize](https://imageresizer.com/)'
    cssFix = """
        <style>
        a{
            border-radius:2px;
            border:1px solid;
            text-decoration:none;
            padding:6px;
            color: black;
        }
        a:hover{
            text-decoration:none;
            color:red;
            border:1px solid red;
        }
    """
    st.markdown(imageResize, unsafe_allow_html=True)
    st.markdown(cssFix, unsafe_allow_html=True)

    # Uploading image file
    image_file = st.file_uploader("Choose File")
    if image_file is not None:
        st.subheader("Before")
        st.image(image_file,width=600)

    st.write("___________________________________________________________________________________________________________________________")

    global valueTake
    valueTake = st.checkbox("Want to take Picture")
    if valueTake == True:
        valueTake = False
    else:
        valueTake = True
    picture = st.camera_input("Take a picture of yourself", disabled=valueTake)
    if picture is not None:
        st.subheader("Before")
        st.image(picture,width=600)

    ################## Backend Logic of the Application #####################


    # Setting the Environment of the application using the API token of Replicate from the database
    apiKey = getItem()
    # os.environ['REPLICATE_API_TOKEN'] = "12229e73fd19da262b8a02e3cc386b842cad82ba"
    os.environ['REPLICATE_API_TOKEN'] = apiKey[0]["api_Key"]


    # # Grabbing the models models
    model = replicate.models.get("timothybrooks/instruct-pix2pix")
    version = model.versions.get("30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f")

    # Taking the prompt
    prompt = st.text_input("Enter the Prompt")

    # Negative Prompts
    negPrompt = st.text_input("Enter negative prompt (leave blank if you don't want any)")

    #number of outputs
    numOut = st.selectbox("Enter the Number of Output Images",["1","4"])

    if st.button("Submit"):
        if image_file is not None:
        
            st.warning("Working....")

            dataBase = getItem()

            inputs = {
                # An image which will be repainted according to prompt
                'image': image_file,

                # Prompt to guide the image generation
                'prompt': prompt,

                # The prompt or prompts not to guide the image generation (what you do
                # not want to see in the generation). Ignored when not using guidance.
                # 'negative_prompt': ...,

                # Number of images to output
                'num_outputs': numOut,

                # The number of denoising steps. More denoising steps usually lead to
                # a higher quality image at the expense of slower inference.
                # Range: 1 to 500
                'num_inference_steps': dataBase[3]["numInf"],

                # Scale for classifier-free guidance. Higher guidance scale encourages
                # to generate images that are closely linked to the text prompt,
                # usually at the expense of lower image quality.
                # Range: 1 to 20
                'guidance_scale': dataBase[3]['guidance_scale'],

                # Image guidance scale is to push the generated image towards the
                # inital image. Higher image guidance scale encourages to generate
                # images that are closely linked to the source image, usually at the
                # expense of lower image quality.
                # Minimum: 1
                'image_guidance_scale': dataBase[3]['image_guidance_scale'],

                # Choose a scheduler.
                'scheduler': dataBase[3]["scheduler"],

                # Random seed. Leave blank to randomize the seed
                'seed': dataBase[3]['seed'] ,
            }

            # https://replicate.com/timothybrooks/instruct-pix2pix/versions/30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f#output-schema
            try:
                output = version.predict(**inputs)
                
                # Output and Downloading image
                st.subheader("After")
                for image in output:
                    st.image(image,width=500)
                    st.markdown("Click on the below link to Download")
                    st.write(image)

            except Exception:
                st.error("There could be some problems with API or use images with single person")

        if picture is not None:
            st.warning("Working....")

            dataBase = getItem()
            inputs = {
                # An image which will be repainted according to prompt
                'image': picture,

                # Prompt to guide the image generation
                'prompt': prompt,

                # The prompt or prompts not to guide the image generation (what you do
                # not want to see in the generation). Ignored when not using guidance.
                # 'negative_prompt': ...,

                # Number of images to output
                'num_outputs': numOut,

                # The number of denoising steps. More denoising steps usually lead to
                # a higher quality image at the expense of slower inference.
                # Range: 1 to 500
                'num_inference_steps': dataBase[3]["numInf"],

                # Scale for classifier-free guidance. Higher guidance scale encourages
                # to generate images that are closely linked to the text prompt,
                # usually at the expense of lower image quality.
                # Range: 1 to 20
                'guidance_scale': dataBase[3]['guidance_scale'],

                # Image guidance scale is to push the generated image towards the
                # inital image. Higher image guidance scale encourages to generate
                # images that are closely linked to the source image, usually at the
                # expense of lower image quality.
                # Minimum: 1
                'image_guidance_scale': dataBase[3]['image_guidance_scale'],

                # Choose a scheduler.
                'scheduler': dataBase[3]["scheduler"],

                # Random seed. Leave blank to randomize the seed
                'seed': dataBase[3]['seed'] ,
            }

            try:
                # https://replicate.com/timothybrooks/instruct-pix2pix/versions/30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f#output-schema
                output = version.predict(**inputs)
            
                # Output and Downloading image
                st.subheader("After")
                for image in output:
                    st.image(image,width=500)
                    st.markdown("Click on the below link to Download")
                    st.write(image)
            
            except Exception:
                st.error("There could be some problems with API or use images with single person")


elif key == "":
    st.sidebar.warning("Enter Secret Key")
else:
    st.sidebar.error("Incorrect Secret Key")

link = '[Magicaibox](https://www.magicaibox.site/controlpanel/udashboard)'
html = """
    <style>
    a{
        border-radius:2px;
        border:1px solid;
        text-decoration:none;
        padding:6px;
        color: black;
    }
    a:hover{
        text-decoration:none;
        color:red;
        border:1px solid red;
    }
"""
st.markdown(link, unsafe_allow_html=True)
st.markdown(html, unsafe_allow_html=True)
