from math import ceil, log2

def write_rom(image_name, coe_name, width, depth):
	print("Generating ROM module... ", end="", flush=True)
	buildString = (
		# module header
		f"""module {image_name}_rom (\n"""
		f"""\tinput logic clock,\n"""
		f"""\tinput logic [{ceil(log2(depth)) - 1}:0] address,\n"""
		f"""\toutput logic [{width-1}:0] q\n"""
		f""");\n"""
		f"""\n"""

		# variable declarations, rom gets instantiated with the compiler directive in the comment.
		f'logic [{width-1}:0] memory [0:{depth-1}] /* synthesis ram_init_file = "{coe_name}" */;\n'
		f"""\n"""

		# always output the data at the given address
		f"""always_ff @ (posedge clock) begin\n"""
		f"""\tq <= memory[address];\n"""
		f"""end\n"""
		f"""\n"""
		f"""endmodule\n"""
	)
	# write to file
	with open(f"""./{image_name}/{image_name}_rom.sv""", "w") as f:
		f.write(buildString)

	print("Done")
