from PIL import Image
t = Image.open("data/fon.jpg")
t = t.resize((1000, 700))
t.save("data/fon.jpg")