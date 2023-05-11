from math import ceil, log2

def write_palette(image_name, palette):
	print("Generating palette module... ", end="", flush=True)

	paletteString = ""
	for i, color in enumerate(palette):
		paletteString += f"""\t{{4'h{color[0]>>4:1X}, 4'h{color[1]>>4:1X}, 4'h{color[2]>>4:1X}}},\n"""
	paletteString = paletteString[:-2]

	buildString = (
		# module header
		f"""module {image_name}_palette (\n"""
		f"""\tinput logic [{ceil(log2(len(palette))) - 1}:0] index,\n"""
		f"""\toutput logic [3:0] red, green, blue\n"""
		f""");\n"""
		f"""\n"""

		# palette definition
		f"""localparam [0:{len(palette)-1}][11:0] palette = {{\n"""
		f"""{paletteString}\n"""
		f"""}};\n"""
		f"""\n"""
		f"""assign {{red, green, blue}} = palette[index];\n"""
		f"""\n"""
		f"""endmodule\n"""
	)

	# write to file
	with open(f"""./{image_name}/{image_name}_palette.sv""", "w") as f:
		f.write(buildString)
	print("Done")
