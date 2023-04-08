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


def pixelate(img, i_range, fname):
	im_orig_size=img.size
	w=im_orig_size[0]
	h=im_orig_size[1]
	print("Original height: {0} and width {1}".format(w, h))
	print("Target size for pixelated image\n Height: {0} and Width: {1}".format(i_range[0], i_range[1]))

	##im_pix_crop.resize(((320 // i_range[0]), (200 // i_range[1])), Image.BILINEAR)
	#im_pix_crop.resize((i_range[0], i_range[1]), Image.BILINEAR)
	#im_pix.resize(((w // i_range[0]), (h // i_range[1])), Image.BILINEAR)
	im_pix_crop= img.resize((i_range[0], i_range[1]), Image.BILINEAR)
#	im_pix.resize((i_range[0], i_range[1]), Image.BILINEAR)
	im_pix= img.resize((i_range), Image.BILINEAR)
	#im_pix.resize(((w // i_range[0]), (h // i_range[1])), Image.NEAREST)
	

	pix_size= (int(w / 4), int(h / 4))
	im_pix.show()
	#crop_orig=im_pix_crop.convert("P",palette=Image.ADAPTIVE,colors=24)
	crop_orig=im_pix_crop.convert("P",palette=Image.ADAPTIVE,colors=256)
	im_pix_crop.resize(pix_size, Image.NEAREST)
	im_pix.resize((im_orig_size), Image.NEAREST)
	im_pix.show()
	#im_pix_crop.show()
	crop_orig.show()
	
	return im_pix, crop_orig

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
	print("imgfile list: {0}".format(imgfile_list))
	imgfile=args.file[0]
	print("imgfile: {0}".format(imgfile))

	
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
		outfile = f + "_pixelated.bmp"
		outfile2 = f + "_pixelated2.bmp"
		pix_list = f + "_pixel_list3.txt"
		#if imgfile != outfile:
		try:

			with Image.open(imgfile) as im:
				pixel_img,crop_pixel_img = pixelate(im, pixelate_size, f)
				pixel_img.save(outfile)
				crop_pixel_img.save(outfile2)
				pix_bitvals = list(crop_pixel_img.getdata())
				for i in range(0,len(pix_bitvals),9):
					pixval=pix_bitvals[i]
					print("byte value for pixel{0}: {1}".format(i, pixval))
				pix_hexvals=list(map(lambda x: hex(x), pix_bitvals))
				with open(pix_list, 'w') as px:
					for i in range(0, (len(pix_hexvals) - 320), 320):
						pixrow=','.join((pix_hexvals[j]) for j in range(i, i+320))
						px.write('db ' + pixrow + '\n')
		
		except OSError as e:
			print("cannot convert: {0} due to error: {1}".format(imgfile, e))



