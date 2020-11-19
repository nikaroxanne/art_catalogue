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

	##background_img = image.copy().convert(mode="RGBA", format="JPEG")

	##test_img = base.copy().reduce(4)
	#test_img.resize(int(w / 12), int(h / 12))


	#### *** testing file resizing ****
	test_w, test_h = (int(image.size[0] / 4), int(image.size[1] / 4))

	print("test image size: %d %d \n", test_w, test_h)
	#### *** testing file resizing ****



	##print("test image size: %d %d \n", test_img.size[0], test_img.size[1])

	##txt_img = Image.new("RGBA", ((image.size[0] / 4),(image.size[1] / 4)), (255,255,255,0))
	#txt_img = Image.new("RGBA", (test_w, test_h), (255,255,255,0))

	##### Make new blank Image with RGBA mode
	##txt_img = Image.new("RGBA", (w, h), (255,255,255,0))
	#####

	##test_w, test_h = test_img.size
	#txt_img = Image.new("RGBA", image.size, (255,255,255,0))
	
	###font path has to be specified; there is no exception handling built into the truetype method for the ImageFont class,
	## so this will not draw an image, but it will fail to raise an exception for that failure being caused by a nonexistant path for a font file
	### Thus: font path has to be explicitly specified, using specifics for each machine (no library assets installed with Pillow package)

	###fnt = ImageFont.truetype("Pillow/Tests/fonts/times.ttf", 40)

	####fnt = ImageFont.truetype("/System/Library/Fonts/Times.ttc", 120)

	##### f here sort of acts like a lambda; or the evaluation of that lambda, stored in a variable, that variable being f


	### For loop to repeatedly draw "tiles" of text image over the larger frame of the base (background_img)
	#f = ImageDraw.Draw(txt_img)
	#f.text((10,10), "is there an API call for this?", font=fnt, fill=(255,255,255,128))
	#f.text((10,10), "or mapping the body of a function", font=fnt, fill=(255,255,255,255))

	#for left in range(0, w, test_w):
	#	for top in range(0, h, test_h):
	#		print("left: %d, top: %d", left, top)
			#test_img.paste(txt_img, (left, top))
			#base.paste(txt_img, (left, top))
	#		background_img.paste(txt_img, (left, top))

	##print("Made text image.")

	##txt_img.show()
	##just_txt = "txt" + outfile
	##txt_img.save(just_txt)

	##test_img.show()
	
	##base.show()
	##text_name = "just_text_" + str(outfile) 
	##base.save(text_name)
	
	##return base

	##img_final = Image.alpha_composite(base, txt_img)
	#img_final = Image.alpha_composite(image, txt_img)
	##img_final = Image.alpha_composite(base, background_img)

	##img_final = Image.alpha_composite(background_img, watermark_txt_img)
	img_final = Image.alpha_composite(base, watermark_txt_img)

	##print("img final mode: %s", img_final.mode)
	#img_final.show()

	##img_final.save(outfile)
	return img_final


	##image.show()
	##return image

#def create_tiled_watermark(image):
def create_tiled_watermark(image, watermark_test_outfile):
	w, h = image.size
	##watermark_img = image.copy().convert(mode="RGBA")
	watermark_img = image.copy()

	print(watermark_img.mode, watermark_img.format, f"{watermark_img.size}x{watermark_img.mode}")

	#test_w, test_h = (int(image.size[0] / 4), int(image.size[1] / 4))
	test_w, test_h = (int(w / 4), int(h / 4))

	##print("test image size: %d %d \n", test_w, test_h)
	txt_img = Image.new("RGBA", (w, h), (255,255,255,0))
	fnt = ImageFont.truetype("/System/Library/Fonts/Times.ttc", 120)

	##### f here sort of acts like a lambda; or the evaluation of that lambda, stored in a variable, that variable being f

	f = ImageDraw.Draw(txt_img)
	f.text((10,10), "is there an API call for this?", font=fnt, fill=(255,255,255,128))
	#f.text((10,10), "or mapping the body of a function", font=fnt, fill=(255,255,255,255))

	for left in range(0, w, test_w):
		for top in range(0, h, test_h):
			print("left", left, "top:", top)
			watermark_img.paste(txt_img, (left, top), txt_img)

	#watermark_img.show()
	##text_name = "just_text_" + str(outfile) 
	##text_name = "just_text.png"

	##background_img.save(text_name)
	##print(watermark_img.mode, watermark_img.format, f"{watermark_img.size}x{watermark_img.mode}")
	#return watermark_img, text_name
	##text_name = "just_text_constellation.jpeg"

	#watermark_img.save(os.path.join(watermark_test_outfile))
	#print("watermark outfile name:", watermark_test_outfile)
	#watermark_img.convert(mode="RGB")
	watermark_img.reduce(4)
	#print(watermark_img.mode, watermark_img.format, f"{watermark_img.size}x{watermark_img.mode}")
	#watermark_img.save(watermark_test_outfile)
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
