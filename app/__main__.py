import os
import time

import torch
import streamlit as st
from PIL import Image

from . import SAVE_DIR
from .model import discriminator, generator
from .utils import save_samples, get_files_in_dir, generate_video

# Create the saving directory
os.makedirs(SAVE_DIR, exist_ok=True)

# Load and evaluate models
generator.load_state_dict(torch.load("app/models/generator_model.bin", map_location=torch.device('cpu')))
discriminator.load_state_dict(torch.load("app/models/discriminator_model.bin", map_location=torch.device('cpu')))

# Finally, Evaluate them
generator.eval()
discriminator.eval()

# -- The views -- #
st.title("Anime Art generation")
st.header("Anime face image and video generation using Deep Convolutional GANs")

# Simple space
st.header("\n\n")

if __name__ == "__main__":
    # Option bar
    option = st.sidebar.selectbox("What do you want to generate?", ("Image", "Video")).lower()

    # Check the option chose
    if option == "video":
        video_range = st.sidebar.slider("How many video frames?", 3, 30, 5)
    else:
        st.sidebar.markdown("**Note:** that the image might be a bit broken due to the shape customization.")
        image_grids = st.sidebar.slider("How many image grids?", 1, 12, 8)

    # Generation logic
    if st.sidebar.button("Click here to generate!"):
        with st.spinner(f"Generating {option}..."):
            if option == "image":
                save_samples(generator, None, image_grids)
                filename = get_files_in_dir(SAVE_DIR)[0]
            else:
                for idx in range(video_range):
                    save_samples(generator, idx)

            # Sleep for a bit
            time.sleep(1)

            # Display generation complete result
            st.info("Generation done!")
            st.balloons()

            # Show the respective image / video.
            if option == "image":
                image = Image.open(filename)
                st.image(image, caption="Anime generated by DCGAN")

                if os.path.exists(filename):
                    os.remove(filename)
            else:
                vid_filename = "anime_timelapse.webm"
                generate_video(SAVE_DIR, vid_filename)

                video_file = open(vid_filename, 'rb')
                video_bytes = video_file.read()
                st.video(video_bytes)
