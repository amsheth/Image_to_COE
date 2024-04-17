# Image_to_COE

Generates SystemVerilog modules that can be used to convert it and use an COE file. 
## Guys Please read the entire Readme including FAQ's and some Notes/Recommendations to make sure you understand what to do.

Credit to @https://github.com/iandailis for allowing me to modify his code to create a COE file.

# How to use:

1) Download Python 3 (developed on 3.11.1 for Windows 10).
2) Download this entire repository.
3) Open a terminal inside this repository. (PowerShell on Windows) (Optional: Use a python virtual environment (Not Recommended), instructions below).
4) Run ```pip install -r requirements.txt```. This installs all the required packages.
5) Run ```python main.py```.
6) Follow the instructions in the terminal. There are two provided images to try out: ```cat.jpg``` and ```butterfly.jpg```.
7) Look at the output image in the generated folder and verify that your chosen settings look okay.
8) In the IP Catalog look up "Block Memory Generator" under Memories and Storage Elements.
9) Change the Component name to ...\_rom, Memory Type to Single Port Rom and Port A Width and Depth according to what the Image has generated. Disable the Enable Port Type (Set it as **Always enabled**).
11) Add the generated .COE file in the Other Options page. You do not need to fill the remaining Memory Locations.
12) Load the 2 .sv files (palette, and example) to your Vivado project.
13) Instantiate the example module in your project, connect all the signals, compile, program, and verify that you see your generated image on the screen!

# Generated Files:

These files are found in ```<image_name>/```
<!-- * ```<image_name>.qip``` - Quartus IP file. **ADD TO QUARTUS PROJECT** -->
* ```<image_name>.COE``` - COE based Memory Initialization File with palettized image data in row-major order.  **ADD TO VIVADO PROJECT**
* ```<image_name>_example.py``` - example color mapper file.
* ```<image_name>_out.png``` - output generated png.
* ```<image_name>_palette.sv``` - output palettes in a SystemVerilog file.
* ```<image_name>_rom.sv``` - inferred ROM initialized by the .mif file.


# Python Files:

* ```main.py``` - top python file, execute this.
* ```src/palettizer.py``` - generates palettes and palettized image.
* ```src/write_example.py``` - generates the example module.
* ```src/write_coe.py``` - generates the Memory Initialization File (MIF).
* ```src/write_palette.py``` - generates the palette module.
* ```src/write_png.py``` - generates the output picture.
* ```src/write_rom.py``` - generates the inferred ROM module.

# FAQ:

* *Warning (10858): Verilog HDL warning at <image_name>_rom.sv(7): object memory used but never assigned*  
Don't worry about it.

* *Warning (10230): Verilog HDL assignment warning at <image_name>_example.sv(12): truncated value with size 32 to match size of target (11)*  
Also don't worry about it.
* *The .blank is meant to be filled by the vde we get from vga controller.*
* If you dont know where the enable pin option is in the IP use .ena(1)
* pip is not recognized as name .... Make sure you have python installed and sometimes it doesnt work with 3.12 so you should download the python 3.11 from Microsoft store. (Linux users can use sudo)
* The depth and the width are give in the COE files.
* the VGA_clk is the 25Mhz clk.
* If you have multiple versions of Python first install python 3.11 from Microsoft store and use ```python3.11``` instead of ```python```.
 
<!-- * *Error (127001): Can't find Memory Initialization File or Hexadecimal (Intel-Format) File ./<image_name>/<image_name>.mif for ROM instance ALTSYNCRAM*  
The comment on <image_name>_rom.sv (7) is a compiler directive to initialize the inferred M9K memory with the contents in a given .mif file. This error message means it couldn't find the generated .mif file. There are a few things you can do here:
	* Option 1 (recommended): Make sure the generated folder is in the same place as the .qpf (quartus project) file. The specified path in the generated rom assumes this.
	* Option 2 (could be easier): Change the path in the compiler directive to the actual path of the generated .mif file. The path can also be an absolute path. -->
	
<!-- * *Error (170040): Can't place all RAM cells in design*  
Oh no! You have no M9K RAM cells left. You have a few options here:  
	* Reduce the resolution for your image when generating.
	* Reduce the number color bits for your image when generating.
	* (difficult and usually overkill) Use SDRAM and frame buffers.
	 -->
* *How does this tool work?*  
Ian took this from ECE 311 Lab 4 Exercise 6 the provided LM Quantizer, somewhat simplified it, then created a bunch of wrapper code that generates the modules and assets. Here is some further reading into k-means clustering:  
https://en.wikipedia.org/wiki/K-means_clustering  
https://scikit-learn.org/stable/modules/clustering.html#k-means  

# Notes/Recommendations:

* Use a virtual environment when installing python packages. Makes your future life easier. Instructions are here: https://docs.python.org/3/library/venv.html  
Essentially, do:
	1) ```python -m venv .venv``` This creates a virtual environment, the files being inside a directory ```.venv/```

	2) ```./.venv/Scripts/Activate.ps1``` This activates the virtual environment. Use a different activation script depending on your operating system. In this case, .ps1 is for Windows PowerShell

	Now, you can download packages without cluttering the global directory!

* The picture in the ROM is stored in row-major order. At every address is stored one pixel's palette index.

* If you are making sprites, **don't just use the example**! Instead, instantiate and use the rom and the palette in your existing color mapper module similarly to the example, then change the rom address calculation and other stuff (yes this isn't that specific, but sprites are a very broad thing with many implementations).

* To do transparency for your sprites:
	1) In the original image, make the background color drastically different from the rest of the image. Hot pink is usually a good color.
	2) Use the tool and regenerate the modules/assets.
	3) When setting the VGA R/G/B outputs based on DrawX/Y, don't just look at sprite_on. Also make sure the palette module's r/g/b output isn't that same hot pink.  

* Deciding how many colors to use depends on your image. You will need to make a compromise between resolution and number of colors. Some images are mostly of one range of colors, while others may go across the entire spectrum. For example, "butterfly.jpg" is mostly yellow, so you can get away with only using 4 bits and thus having the full 640x480 resolution. "cat.jpg" uses many more colors though, so it will look better if you use more bits for more colors and sacrifice some resolution.

Enjoy!
-Arnav Sheth

<!-- 8) Put the entire generated folder into your quartus project directory (that's the same place as your .qpf file). -->
