import dxcam
from PIL import Image

print(dxcam.device_info(), dxcam.output_info())
screen_grabber = dxcam.create(device_idx=0, output_idx=0)
img = Image.fromarray(screen_grabber.grab()).resize((1920//4, 1080//4), Image.Resampling.NEAREST)
img.save("image.png")

