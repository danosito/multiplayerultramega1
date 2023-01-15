from PIL import Image
for i in range(1, 6):
    t = Image.open(f"data/level{str(i)}sc.png")
    t = t.resize((500, 350))
    t.save(f"data/level{str(i)}sc.png")