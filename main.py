from imageio.v2 import imread
from PIL.Image import fromarray
from numpy import asarray

from src.palettizer import palettizer
from src.write_coe import write_coe
from src.write_rom import write_rom
from src.write_palette import write_palette
from src.write_example import write_example
from src.write_qip import write_qip
from src.write_png import write_png

from os import makedirs

def main():
	# open input image
	image_path = input("Input image (eg: waterfall.jpeg): ")
	image = imread(image_path).astype("uint8")

	# get number of colors to compress into
	k = int(input("Number of bits per pixel to store: "))

	# get resized image dimensions
	image_x = int(input("Desired output horizontal resolution: "))
	image_y = int(input("Desired output vertical resolution: "))

	# check if parameters will fit into the M9k blocks
	mbits_available = 182*1024*8 # 182 M9k blocks * 1024 bytes per block * 8 bits per block
	mbits_used = image_x*image_y*k
	print(f"""Using {mbits_used} / {mbits_available} available M9k memory bits""")
	if (mbits_used > mbits_available):
		print("WARNING: DESIGN PROBABLY WON'T FIT INTO M9K BLOCKS")
	else:
		print("Design may still not fit. M9k block usage is weird.")

	# resize the image
	print("Resizing image... ", end="", flush=True)
	image_resized = asarray(fromarray(image).resize((image_x, image_y)))
	print("Done")

	# get the palettized image and the array of palettes
	image_palettized, palette = palettizer(image_resized, 2**k)

	# set the image name and create the directory, if it does not exist
	image_shape = image_resized.shape
	image_name = image_path.rsplit('.')[0] # cut the file extension
	try:
		makedirs(image_name)
	except:
		pass

	# create the coe (memory instantiation file)
	width, depth, coe_name = write_coe(image_palettized, k, image_name)

	# create the ROM that will read the coe
	write_rom(image_name, coe_name, width, depth)

	# create the palette module
	write_palette(image_name, palette)

	# create the example, which will use the palette and ROM modules
	write_example(image_name, image_shape, width, depth)

	# create the qip file
	write_qip(image_name)

	# show the result
	write_png(image_palettized, palette, image_name, image_shape)

	print(f"""Output files are in ./{image_name}/""")


if (__name__ == "__main__"):
	main()
