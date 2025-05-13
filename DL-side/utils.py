import numpy as np
from PIL import Image

def resize_img(img, to_width, to_height):
    return np.array(Image.fromarray(img).resize((to_width, to_height), Image.Resampling.LANCZOS))