import os

import torch
from torchvision.utils import save_image

from . import STATS, LATENT_SIZE, SAVE_DIR


def denorm(img_tensors):
    return img_tensors * STATS[1][0] + STATS[0][0]


def save_samples(index, generator):
    latent_tensors = torch.randn(64, LATENT_SIZE, 1, 1, device=torch.device('cpu'))

    fake_images = generator(latent_tensors)
    fake_fname = 'generated-images-{0:0=4d}.png'.format(index)

    save_image(denorm(fake_images), os.path.join(SAVE_DIR, fake_fname), nrow=8)


def get_files_in_dir(directory):
    files = [os.path.join(directory, f) for f in os.listdir(directory) if directory in f]
    files.sort()

    return files
