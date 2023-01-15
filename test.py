from PIL import Image
name = "data/electro_info.png"
t = Image.open(name)
t = t.resize((666, 500))
t.save(name)