from PIL import Image
t = "data/level4sc.png"
n = Image.open(t).resize((500, 350))
n.save(t)