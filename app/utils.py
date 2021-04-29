import os

import cv2
import streamlit as st
import torch
from torchvision.utils import save_image

from . import STATS, LATENT_SIZE, SAVE_DIR


def denorm(img_tensors):
    return img_tensors * STATS[1][0] + STATS[0][0]


def save_samples(generator, index=None, tensor_size=8):
    latent_tensors = torch.randn(tensor_size*tensor_size, LATENT_SIZE, 1, 1, device=torch.device('cpu'))

    fake_images = generator(latent_tensors)

    if not index:
        fake_fname = "generated-image.png"
    else:
        fake_fname = "generated-images-{0:0=4d}.png".format(index)

    save_image(denorm(fake_images), os.path.join(SAVE_DIR, fake_fname), nrow=8)


@st.cache(suppress_st_warning=True, ttl=5, max_entries=128)
def get_files_in_dir(directory):
    files = [os.path.join(directory, f) for f in os.listdir(directory) if directory in f]
    files.sort()

    return files


def generate_video(generated_location, save_filename):
    files = get_files_in_dir(generated_location)

    # *"MP4V" was planned to use for MP4, unfortunately browsers don't support it, Hence used VP80 for `.webm`
    out = cv2.VideoWriter(save_filename, cv2.VideoWriter_fourcc(*"VP80"), 1, (530, 530))
    [out.write(cv2.imread(fname)) for fname in files]
    out.release()
