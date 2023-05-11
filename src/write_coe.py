
def write_coe(image_palettized, k, image_name):
	"""
	https://www.intel.com/content/www/us/en/programmable/quartushelp/13.0/mergedProjects/reference/glossary/def_coe.htm
	"""
	print("Generating coe (Memory Instantiation File)... ", end="", flush=True)

	width = k
	depth = len(image_palettized)

	buildString = (
		# construct header
		f""";This .COE file specifies initialization values for a block """
		f""";memory of depth={depth}, and width={width}. In this case, values are """
		f""";specified in hexadecimal format.\n"""
		f"""memory_initialization_radix=10;\n"""
		f"""memory_initialization_vector="""
	)

	# write data in address : data format
	for i, palette_index in enumerate(image_palettized):
		buildString += f"""\n{palette_index},"""
	
	buildString += f""";\n"""

	# write the data to the file
	coe_name = f"""./{image_name}/{image_name}.COE"""
	with open(coe_name, "w") as f:
		f.write(buildString)

	print("Done")
	return width, depth, coe_name
