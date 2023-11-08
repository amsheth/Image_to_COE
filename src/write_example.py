from math import ceil, log2

def write_example(image_name, image_shape, width, depth):
	print("Generating example module... ", end="", flush=True)

	# build the file
	buildString = (
		# module header
		f"""module {image_name}_example (\n"""
		f"""\tinput logic vga_clk,\n"""
		f"""\tinput logic [9:0] DrawX, DrawY,\n"""
		f"""\tinput logic blank,\n"""
		f"""\toutput logic [3:0] red, green, blue\n"""
		f""");\n"""
		f"""\n"""

		# variable instantiations
		f"""logic [{ceil(log2(depth))-1}:0] rom_address;\n"""
		f"""logic [{width-1}:0] rom_q;\n"""
		f"""\n"""
		f"""logic [3:0] palette_red, palette_green, palette_blue;\n"""
		f"""\n"""
		f"""logic negedge_vga_clk;\n"""
		f"""\n"""

		f"""// read from ROM on negedge, set pixel on posedge\n"""
		f"""assign negedge_vga_clk = ~vga_clk;\n"""
		f"""\n"""

		f"""// address into the rom = (x*xDim)/640 + ((y*yDim)/480) * xDim\n"""
		f"""// this will stretch out the sprite across the entire screen\n"""
		f"""assign rom_address = ((DrawX * {image_shape[1]}) / 640) + (((DrawY * {image_shape[0]}) / 480) * {image_shape[1]});\n"""
		f"""\n"""

		# set rgb values synchronously, taking into account the blank signal 
		f"""always_ff @ (posedge vga_clk) begin\n"""
		f"""\tred <= 4'h0;\n"""
		f"""\tgreen <= 4'h0;\n"""
		f"""\tblue <= 4'h0;\n"""
		f"""\n"""
		f"""\tif (blank) begin\n"""
		f"""\t\tred <= palette_red;\n"""
		f"""\t\tgreen <= palette_green;\n"""
		f"""\t\tblue <= palette_blue;\n"""
		f"""\tend\n"""
		f"""end\n"""
		f"""\n"""

		# instantiate the ROM
		f"""{image_name}_rom {image_name}_rom (\n"""
		f"""\t.clka   (negedge_vga_clk),\n"""
		f"""\t.addra (rom_address),\n"""
		f"""\t.douta       (rom_q)\n"""
		f""");\n"""
		f"""\n"""

		# instantiate the palette
		f"""{image_name}_palette {image_name}_palette (\n"""
		f"""\t.index (rom_q),\n"""
		f"""\t.red   (palette_red),\n"""
		f"""\t.green (palette_green),\n"""
		f"""\t.blue  (palette_blue)\n"""
		f""");\n"""
		f"""\n"""

		f"""endmodule\n"""
	)
	# write to file
	with open(f"""./{image_name}/{image_name}_example.sv""", "w") as f:
		f.write(buildString)

	print("Done")
