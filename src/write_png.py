from numpy import zeros as np_zeros
from imageio import imsave

def write_png(image_palettized, palette, image_name, image_shape):
	print("Generating output image... ", end="", flush=True)

	output_image = np_zeros(image_shape, dtype="uint8")
	for i, palette_index in enumerate(image_palettized):
		output_image[i // image_shape[1]][i % image_shape[1]] = palette[palette_index]

	output_name = f"""./{image_name}/{image_name}_out.png"""
	imsave(output_name, output_image)

	print("Done")