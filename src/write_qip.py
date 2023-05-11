def write_qip(image_name):
	print("Generating .qip file... ", end="", flush=True)

	buildString = (
		f"""set_global_assignment -name SYSTEMVERILOG_FILE [file join $::quartus(qip_path) "{image_name}_rom.sv"]\n"""
		f"""set_global_assignment -name SYSTEMVERILOG_FILE [file join $::quartus(qip_path) "{image_name}_palette.sv"]\n"""
		f"""set_global_assignment -name SYSTEMVERILOG_FILE [file join $::quartus(qip_path) "{image_name}_example.sv"]\n"""
	)

	with open(f"""./{image_name}/{image_name}.qip""", "w") as f:
		f.write(buildString)

	print("Done")
