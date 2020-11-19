import os, sys
from PIL import Image, ImageDraw, ImageFont

#def watermark():
#	return image

## Referencing tutorials on the Pillow documentation:
## https://pillow.readthedocs.io/en/stable/handbook/tutorial.html
## and this tutorial on image transforms with text, using ImageDraw module:
## https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html


##def basic_transform(image, outfile):
def basic_transform(image, watermark_txt_img):
	w, h = image.size
	drawing = ImageDraw.Draw(image)
	drawing.line((0,0) + image.size, fill=128, width=25)
	drawing.line((0, w, h, 0), fill=128, width=25)
	
	base = image.convert(mode="RGBA")

	#### *** testing file resizing ****
	test_w, test_h = (int(image.size[0] / 4), int(image.size[1] / 4))

	print("test image size: %d %d \n", test_w, test_h)
	#### *** testing file resizing ****

	##### Make new blank Image with RGBA mode
	##txt_img = Image.new("RGBA", (w, h), (255,255,255,0))
	#####

	
	######
	###	Font path has to be specified; there is no exception handling built into the truetype method for the ImageFont class,
	### 	So this will not draw an image, but it will fail to raise an exception for that failure being caused by a nonexistant path for a font file
	### 	Thus: font path has to be explicitly specified, using specifics for each machine (no library assets installed with Pillow package)
	###	fnt = ImageFont.truetype("Pillow/Tests/fonts/times.ttf", 40)
	###	fnt = ImageFont.truetype("/System/Library/Fonts/Times.ttc", 120)
	########



	#img_final = Image.alpha_composite(base, txt_img)
	#img_final.show()
	return img_final


#def create_tiled_watermark(image):
def create_tiled_watermark(image, watermark_test_outfile):
	w, h = image.size
	### Converting the Image to RGBA mode, in the context of this function, is unneccessary, 
	### and causes later anguish if you want to save the resultant image as a JPEG
	### Thus, avoid converting to RGBA if possible
	###watermark_img = image.copy().convert(mode="RGBA")
	
	watermark_img = image.copy()

	test_w, test_h = (int(w / 4), int(h / 4))

	txt_img = Image.new("RGBA", (w, h), (255,255,255,0))
	fnt = ImageFont.truetype("/System/Library/Fonts/Times.ttc", 120)

	##### f here sort of acts like a lambda; or the evaluation of that lambda, stored in a variable, that variable being f

	f = ImageDraw.Draw(txt_img)
	f.text((10,10), "is there an API call for this?", font=fnt, fill=(255,255,255,128))
	#f.text((10,10), "or mapping the body of a function", font=fnt, fill=(255,255,255,255))

	### For loop to repeatedly draw "tiles" of text image over the larger frame of the base (background_img)
	for left in range(0, w, test_w):
		for top in range(0, h, test_h):
			print("left", left, "top:", top)
			watermark_img.paste(txt_img, (left, top), txt_img)

	watermark_img.reduce(4)
	return watermark_img


if __name__ == '__main__':
	test_filename = sys.argv[1]
	print("test filename:", test_filename, "\n")
	
	for infile in sys.argv[1:]:
		img_dirname = os.path.dirname(infile)
		print("image dirname is:", img_dirname, "\n")
		f, e = os.path.splitext(infile)
		print("image name is:", f, "image extension is:", e, "\n")
		##outfile = f + "_watermark.jpg"
		#outfile = f + "_watermark" + e
		outfile = f + "_watermark.jpeg"
		text_name = "just_text_" + outfile
		
		if infile != outfile:
			try:
				with Image.open(infile) as im:
					#print(infile, im.mode, im.format, f"{im.size}x{im.mode}")
					##resized_im = im.Reduce(4)
					#watermark_txt, text_name = create_tiled_watermark(im, outfile)
					watermark_txt = create_tiled_watermark(im, text_name)
					watermark_txt.save(text_name)
					##print(watermark_txt, watermark_txt.mode, watermark_txt.format, f"{watermark_txt.size}x{watermark_txt.mode}")
					#new_im = basic_transform(im, watermark_txt)
					##new_im = basic_transform(im)
					##new_im = basic_transform(im, outfile)
					#new_im.save(outfile)
			except OSError:
				print("cannot convert", infile)
