from numpy import array as np_array
from sklearn.cluster import KMeans
from warnings import catch_warnings, simplefilter

def palettizer(image, k):
	"""
	I took this code from the LM Quantizer in ECE 311 Lab 4, 
	and slightly refactored it. 
	"""
	print("Palettizing image... ", end="", flush=True)
	# easier variable names
	n_rows, n_cols = image.shape[0], image.shape[1]

	# create k-means object
	kmeans = KMeans(n_clusters = k)

	# reshape pixel value to be like data points
	pixel_vals = np_array([image[row,col] for row in range(n_rows) for col in range(n_cols)])
	
	# catch FutureWarnings because sklearn things
	with catch_warnings():
		simplefilter(action='ignore', category=FutureWarning)
		# fit the k-means model to pixel data and get color labels
		image_palettized = kmeans.fit_predict(pixel_vals)

	# get the palette
	palette = kmeans.cluster_centers_.astype("uint8")

	# compress colors to 4 bit
	for i in range(len(palette)):
		for j in range(len(palette[i])):
			palette[i][j] &= 0xF0

	print("Done")
	return image_palettized, palette
