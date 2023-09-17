#!/bin/python3
import os, sys
from PIL import Image, ImageFilter, ImageFile, ImageOps, ImageShow
import argparse


################################################################################################################
#           Generate a pixelated image for a given input image (.jpg format), 
#	    Scaling the image to squares of size N x N
#	    Where N is the integer value of the square length for interpolation of image file
#	    
#
################################################################################################################


def crop_greyscale(img, i_range, fname):
	im_orig_size=img.size
	w=im_orig_size[0]
	h=im_orig_size[1]
	print("Original height: {0} and width {1}".format(w, h))
	print("Target size for pixelated image\n Height: {0} and Width: {1}".format(i_range[0], i_range[1]))

	im_pix_crop= img.resize((i_range[0], i_range[1]), Image.BILINEAR)

	pix_size= (int(w / 4), int(h / 4))
	crop_greyscale=im_pix_crop.convert("L")
	crop_greyscale.show()	

	return crop_greyscale

def merge():
	return 0


################################################################################################################
#           Argparse template - more detailed/fine-grained command line controls
#
################################################################################################################

def setup_options():
	parser = argparse.ArgumentParser(description='A utility to transform input image files into their pixelated equivalents, transforming pixels based on input size of transformation matrix')
	parser.add_argument('-file', nargs=1, type=str, help='Input image to which to apply transformation functions')
	parser.add_argument('-size', nargs=2, type=int, help='Image size to be used for creating scaled, output pixelated image')
	args = parser.parse_args()
	return parser, args

################################################################################################################
#
################################################################################################################


if __name__ == '__main__':
	#test_filename = sys.argv[1]
	#print("test filename:", test_filename, "\n")
	parser,args=setup_options()
	imgfile_list=args.file	
	pixelate_scale=args.size
	#print("imgfile list: {0}".format(imgfile_list))
	imgfile=args.file[0]
	#print("imgfile: {0}".format(imgfile))

	if pixelate_scale is None:
		pixelate_size = (320,200)
	else:
		pixelate_size = (pixelate_scale[0], pixelate_scale[1])
	print("pixelate scale: {0}".format(pixelate_size))
	if imgfile is not None:
		img_dirname = os.path.dirname(imgfile)
		print("image dirname is:", img_dirname, "\n")
		f, e = os.path.splitext(imgfile)
		print("image name is:", f, "image extension is:", e, "\n")
		outfile = f + "_ascii.bmp"
		outfile2 = f + "_ascii2.bmp"
		pix_list = f + "_asciiart_hex_list3.txt"
		#if imgfile != outfile:
		asciichars = ["@", "J", "D", "%", "*", "P", "+", "Y", "$", ",", "."]
		
		try:
			with Image.open(imgfile) as im:
				new_width=pixelate_size[0]
				greyscale_crop_img = crop_greyscale(im, pixelate_size, f)
				greyscale_bitvals = list(greyscale_crop_img.getdata())
				ascii_pixels=[ asciichars[grey_pixel //25] for grey_pixel in greyscale_bitvals]
				ascii_pixels=''.join(ascii_pixels)
				count_ascii_pixels=len(ascii_pixels)
				
				ascii_image=[ascii_pixels[index:index+new_width] for index in range(0, count_ascii_pixels, new_width)]
				ascii_image='\n'.join(ascii_image)
				print(ascii_image)			
	
				with open(outfile, 'w') as px:
					px.write(ascii_image)	
			
				pix_hexvals=list(map(lambda x: hex(x), greyscale_bitvals))
				bitmap_rows=pixelate_scale[1]
				bitmap_cols=pixelate_scale[0]
				with open(pix_list, 'w') as px:
					for i in range(0, bitmap_rows):
						pixrow=','.join((pix_hexvals[j]) for j in range(bitmap_cols*i, (bitmap_cols*i+bitmap_cols)))
						print("pixel row for pixel {0}: {1}".format(i, pixrow))
						px.write('db ' + pixrow + '\n')
		
		except OSError as e:
			print("cannot convert: {0} due to error: {1}".format(imgfile, e))



