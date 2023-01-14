from PIl import Image
t = Image.open("data/gameover.png")
t = t.resize(1000, 700)
t.save("data/gameover.png")