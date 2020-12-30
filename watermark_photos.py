import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter


## Referencing tutorials on the Pillow documentation:
## https://pillow.readthedocs.io/en/stable/handbook/tutorial.html
## and this tutorial on image transforms with text, using ImageDraw module:
## https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html

def make_fragment_image(image, offset_int, reduction_factor):
	w, h = image.size
	##drawing = ImageDraw.Draw(image)

	offset_w = offset_int // 3
	offset_h = offset_int % 3
	
	#offset_w = offset_int // 9
	#offset_h = offset_int % 9

	reduction_val = 3^reduction_factor

	#### *** resizing of original input image by factor of 9 ****

	##new_base_img_size = (int(w / 9),  int(h / 9))
	new_base_img_size = (int(w / reduction_val),  int(h / reduction_val))
	new_base_w, new_base_h = new_base_img_size[0], new_base_img_size[1]
	new_base = image.convert(mode="RGBA").copy().resize(new_base_img_size)
	
	
	### creating new crop dimensions for background 
	crop_base_size = list(map(lambda x: int(x / 3), new_base_img_size))
	new_crop_base_w, new_crop_base_h = (crop_base_size[0], crop_base_size[1])
	
	crop_l, crop_t = (offset_w * new_crop_base_w, offset_h * new_crop_base_h)
	crop_dim = (crop_l, crop_t, crop_l + new_crop_base_w, crop_t + new_crop_base_h)

	##crop_l, crop_t = (offset_w * new_base_w, offset_h * new_base_h)
	##crop_dim = (crop_l, crop_t, crop_l + new_base_w, crop_t + new_base_h)

	#border_size_dim = (int(new_base_w / 3), int(new_base_h / 3))
	border_size_dim = list((int(new_base_w / 9), int(new_base_h / 9)))
	

	crop_w_border_size = list(map(lambda x, y: x + y, new_base_img_size, border_size_dim))
	##crop_w_border_size = list(map(lambda x, y: x + y, crop_base_size, border_size_dim))
	
	tile_image = new_base.crop(crop_dim)
	
	background_crop_img = Image.new("RGB", (crop_w_border_size), (0, 0, 0, 255))
	##background_crop_img = Image.new("RGBA", (crop_w_border_size), (0, 0, 0, 255))
	background_crop_img.paste(tile_image, (crop_l, crop_t))
	background_crop_img.show()

	return background_crop_img



def basic_transform(image, watermark_txt_img):
	w, h = image.size
	drawing = ImageDraw.Draw(image)
	drawing.line((0,0) + image.size, fill=128, width=25)
	drawing.line((0, w, h, 0), fill=128, width=25)
	
	base = image.convert(mode="RGBA")

	#### *** testing file resizing ****
	test_w, test_h = (int(image.size[0] / 4), int(image.size[1] / 4))

	background_image = Image.new("RGBA", (test_w, test_h), (255,255,255,255))


	print("test image size: %d %d \n", test_w, test_h)
	#### *** testing file resizing ****

	##### Make new blank Image with RGBA mode
	##txt_img = Image.new("RGBA", (w, h), (255,255,255,0))
	#####

	median_filter = image.filter(ImageFilter.MedianFilter(int((w* h) / 2)))
	median_filter.show()

	
	######
	###	Font path has to be specified; there is no exception handling built into the truetype method for the ImageFont class,
	### 	So this will not draw an image, but it will fail to raise an exception for that failure being caused by a nonexistant path for a font file
	### 	Thus: font path has to be explicitly specified, using specifics for each machine (no library assets installed with Pillow package)
	###	fnt = ImageFont.truetype("Pillow/Tests/fonts/times.ttf", 40)
	###	fnt = ImageFont.truetype("/System/Library/Fonts/Times.ttc", 120)
	########



	img_final = Image.alpha_composite(base, txt_img)
	#img_final.show()
	#return img_final
	return img_final


#def create_tiled_watermark(image):
def create_tiled_watermark(image, watermark_test_outfile):
	w, h = image.size
	### Converting the Image to RGBA mode, in the context of this function, is unneccessary, 
	### and causes later anguish if you want to save the resultant image as a JPEG
	### Thus, avoid converting to RGBA if possible
	###watermark_img = image.copy().convert(mode="RGBA")
	
	new_base_img_size = (int(w / 9),  int(h / 9))

	##test_w, test_h = (int(w / 4), int(h / 4))
	test_w, test_h = (int(w / 2), int(h / 2))
	
	watermark_img = image.copy().resize((test_w, test_h))


	#txt_img = Image.new("RGBA", (w, h), (255,255,255,0))
	txt_img = Image.new("RGBA", (test_w, test_h), (255,255,255,0))
	fnt = ImageFont.truetype("/System/Library/Fonts/Times.ttc", 24)



	##### f here sort of acts like a lambda; or the evaluation of that lambda, stored in a variable, that variable being f

	f = ImageDraw.Draw(txt_img)
	#text_content = "is there an API call for this? "
	text_content = "tales from your venerated New England prep school: part 1 "
	f.text((10,10), text_content, font=fnt, fill=(255,255,255,128))
	
	#f.text((10,10), "is there an API call for this? ", font=fnt, fill=(255,255,255,128))
	#f.text((10,10), "or mapping the body of a function", font=fnt, fill=(255,255,255,255))


	### get font length, width in pixels
	text_w, text_h = f.textsize(text_content, fnt)
	##text_w, text_h = f.textsize(f.text, fnt)
	##print("text_w:", text_w, " text_h:", text_h, "\n")

	##how many tiles can fit in this image?
	num_tiles_w, num_tiles_h = (int(w / text_w), int(h / text_h))
	##print("num_tiles_w:", num_tiles_w, " num_tiles_h:", num_tiles_h, "\n")


	### For loop to repeatedly draw "tiles" of text image over the larger frame of the base (background_img)
	for left in range(0, test_w, text_w):
		for top in range(0, test_h, text_h):
			#print("left", left, "top:", top)
			watermark_img.paste(txt_img, (left, top), txt_img)


	watermark_img.reduce(4)
	watermark_img.show()
	return watermark_img


if __name__ == '__main__':
	test_filename = sys.argv[1]
	
	for infile in sys.argv[1:]:
		img_dirname = os.path.dirname(infile)
		f, e = os.path.splitext(infile)
		basename_f = f.split('/')[-1]
		outfile = basename_f + "_watermark" + e
		text_name = "just_text_" + outfile
		
		if infile != outfile:
			try:
				with Image.open(infile) as im:
					watermark_txt = create_tiled_watermark(im, text_name)
					#watermark_txt.save(text_name)
					#new_im = basic_transform(im, watermark_txt)
					#new_im.save(outfile)
					for x in range(6, 9):
						new_im_name = "fragment_" + str(x) + "_" + outfile
						new_fragment = make_fragment_image(im, x, 1)
						new_fragment.save(new_im_name)
						new_tile_fragment_name = "watermark_" + new_im_name
						new_tile_watermark = create_tiled_watermark(new_fragment, text_name)
						new_tile_watermark.save(new_tile_fragment_name)
						print("new file name: ", new_im_name, "\n")

			except OSError:
				print("cannot convert", infile)
