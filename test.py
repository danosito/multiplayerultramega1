from PIL import Image
hydro_image = 'hydro.png'
electro_image = 'electroman.png'
pyro_image = 'fireman.png'
cryo_image = 'crioman.png'
anemo_image = 'anemoman.png'
geo_image = 'geoman.png'
dendro_image = 'dendroman.png'
scaled = []
perss = [hydro_image, pyro_image, cryo_image, anemo_image, geo_image, electro_image, dendro_image]
for name in perss:
    scaled.append("load_image(\"" + name.replace(".png", "") + "_scaled.png\")")
print("[", end="")
for i in scaled:
    print(i, end=", ")
