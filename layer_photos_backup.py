#!/bin/python3
import os, sys
from PIL import Image, ImageFilter, ImageFile, ImageOps, ImageShow
#from PIL import * 
import argparse


def pixelate(img, i_range, fname):
	im_orig_size=img.size
	w=im_orig_size[0]
	h=im_orig_size[1]
	print("Original height: {0} and width {1}".format(w, h))
	print("Target size for pixelated image\n Height: {0} and Width: {1}".format(i_range[0], i_range[1]))
	#im_pix=img.convert(mode="RGBA").copy().reduce(4)
	#im_pix=img.convert(mode="RGB").copy().reduce(2)
	
	###im_pix_crop=img
	
	###im_pix=img.convert(mode="RGB").copy()
	
	##im_pix=img.convert(mode="RGB")
	#im_pix_crop=im_pix.crop((100,200,420,400))
	##im_pix_crop=im_pix.crop((600,1300,920,1500))
	##im_pix.show()
	###im_pix_crop.show()
	
	#im_pix=img.convert(mode="RGBA").copy()
	#im_pix.resize(((w // i_range[0]), (h // i_range[1])), resample=Image.Resampling.BILINEAR)
	
	##im_pix_crop.resize(((320 // i_range[0]), (200 // i_range[1])), Image.Resampling.BILINEAR)
	##im_pix.resize(((w // i_range[0]), (h // i_range[1])), Image.Resampling.BILINEAR)
	
	##im_pix_crop.resize(((320 // i_range[0]), (200 // i_range[1])), Image.BILINEAR)
	#im_pix_crop.resize((i_range[0], i_range[1]), Image.BILINEAR)
	#im_pix.resize(((w // i_range[0]), (h // i_range[1])), Image.BILINEAR)
	im_pix_crop= img.resize((i_range[0], i_range[1]), Image.BILINEAR)
#	im_pix.resize((i_range[0], i_range[1]), Image.BILINEAR)
	im_pix= img.resize((i_range), Image.BILINEAR)
	#im_pix.resize(((w // i_range[0]), (h // i_range[1])), Image.NEAREST)
	

	#im_pix.resize(((w // i_range[0]), (h // i_range[1])), resample=Image.Resampling.NEAREST)
	#im_pix.resize((((w // 4) // i_range[0]), ((h // 4 ) // i_range[1])), resample=Image.Resampling.NEAREST)
	#im_pix.resize((((w // 4) // i_range[0]), ((h // 4 ) // i_range[1])), resample=Image.Resampling.BILINEAR)
	#pix_size= (int(w / i_range[0]), int(h / i_range[1]))
	pix_size= (int(w / 4), int(h / 4))
	##im_pix.show()
	#im_pix.resize(pix_size, resample=Image.Resampling.NEAREST)
	#im_pix_crop.resize((320,200), resample=Image.Resampling.NEAREST)
	im_pix.show()

	
	#im_pix.resize(pix_size, Image.NEAREST)
	#im_pix_crop.resize((320,200), Image.NEAREST)
	im_pix_crop.resize(pix_size, Image.NEAREST)
	im_pix.resize((im_orig_size), Image.NEAREST)
	#im_pix.resize(im_orig_size, resample=Image.Resampling.NEAREST)
	im_pix.show()
	im_pix_crop.show()
	##fin_image=Image.new("RGB", (im_orig_size), (255,255,255,255))
	
	#fin_image=im_pix.resize(im_orig_sizei)
	#fin_image.paste(im_pix, pix_size)
	##fin_image.paste(im_pix, (w,h))
	##fin_image.show()
	
	#fin_img_name="resize+i_range[0]+i_range[1]"+fname
	#fin_img.save(fin_image_name, "JPEG")
	##return fin_image
	return im_pix

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
		outfile = f + "_pixelated.jpeg"
		#if imgfile != outfile:
		try:

			with Image.open(imgfile) as im:
				pixel_img = pixelate(im, pixelate_size, f)
				pixel_img.save(outfile)
				
		except OSError as e:
			print("cannot convert: {0} due to error: {1}".format(imgfile, e))



