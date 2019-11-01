from PIL import Image


image = Image.open("resources/encode.png")
image.resize((423, 542)).save("resources/encode_resize.png")
