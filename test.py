from PIL import Image
t = Image.open("data/portal.png")
t = t.resize((50, 100))
t.save("data/portal.png")