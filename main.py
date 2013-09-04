#coding: utf-8

import urllib2
import simplejson as json
import time

from PIL import Image, ImageDraw




# https://apigee.com/console/instagram
USER_ID = '54040411'#me
USER_ID = '37698273'#KT
TOKEN = '54040411.1fb234f.695ee9bc9bb742489e125e98630fcdf6'
PICTS_FOLDER = 'C:\gram\picts'
OUTPUT_FOLDER = 'C:\gram\output'


IMG_SIZE = 600
FRAME = 55
X_OFFSET = 400
Y_OFFSET = 100

CANVAS_X_SIZE = 3508 
CANVAS_Y_SIZE = 2480




def run():
	print "hello"
	url_list = get_links()
	save_pictures(url_list, PICTS_FOLDER)

	resized = load_and_resize(45)
	framed_dict = frame(resized)

	fit_to_canvas(framed_dict, CANVAS_X_SIZE, CANVAS_Y_SIZE)

def save_picture(file_name, url):
	f = open(file_name, 'wb')
	f.write(urllib2.urlopen(url).read())
	f.close()


def get_links(userid=USER_ID, token=TOKEN):	
	url = 'https://api.instagram.com/v1/users/%s/media/recent?access_token=%s&count=-1&' % (userid, token)
	answer = json.loads(urllib2.urlopen(url).read())

	urllist = []
	for record in answer['data']:
		img_url = record['images']['standard_resolution']['url']
		urllist.append(img_url)
	return urllist


def save_pictures(urllist, folder_path):
	mas = []
	for i in range(0, len(urllist)): 
		dic = {}
		dic['oid'] = len(urllist) - i
		dic['url'] = str(urllist[i])
		# .replace('\n', '')
		mas.append(dic)

	for obj in mas:
		file_name = PICTS_FOLDER+'\\%s.jpg' % obj['oid']
		print file_name
		save_picture(file_name, obj['url'])



def load_and_resize(amount, xpics=IMG_SIZE, ypics=IMG_SIZE):
	# image1 = Image.open('C:/gram/picts/1.jpg')
	# image1.show()
	# i = 1
	# orig = Image.open('C:/gram/picts/%s.jpg' % i)
	# orig.show()
	scope = []
	for i in range(1, amount+1):
		# scope['path'] = '%s.jpg' % i
		# scope['file'] = Image.open('C:/gram/picts/%s.jpg' % i)
		# scope['file']. show()
		orig = Image.open('C:/gram/picts/%s.jpg' % i)
		orig.copy()
		if xpics and ypics:
			orig = orig.resize((xpics, ypics))
		scope.append(orig)
		# orig.show()
		# orig.save('C:/gram/picts/resized%s.jpg' % i,)
	# 2480х3508 holst 210х297
	return scope



def frame(scope):
	framed = []
	for image in scope:
		canvas = Image.new("RGB", (IMG_SIZE+FRAME*2, IMG_SIZE+FRAME*2), (255,255,255))
		canvas.paste(image, (FRAME, FRAME))
		
		draw = ImageDraw.Draw(canvas)
		draw.line((0, 0, IMG_SIZE+FRAME*2, 0), fill="black", width=2)
		draw.line((0, 0, 0, IMG_SIZE+FRAME*2), fill="black", width=2)
		draw.line((IMG_SIZE+FRAME*2, 0, IMG_SIZE+FRAME*2, IMG_SIZE+FRAME*2), fill="black", width=2)
		draw.line((0, IMG_SIZE+FRAME*2, IMG_SIZE+FRAME*2, IMG_SIZE+FRAME*2), fill="black", width=2)
		framed.append(canvas)
		# canvas.show()
	return framed

def fit_line(canvas, line, y, image_size):
	x = X_OFFSET
	for image in line:
		canvas.paste(image, (x,y))
		x = x + image_size - 1
	# canvas.show()

def fit_to_canvas(img_dict, width, height):

	# canvas.show()
	image_size = img_dict[0].size[0]
	
	pictures_amount_x = width / image_size
	pictures_amount_y = height / image_size

	pictures_on_canvas = pictures_amount_x * pictures_amount_y

	print "VSEGO FOTO " + str(len(img_dict))
	print "PO SHIRINE " + str(pictures_amount_x)
	print "PO VISOTE " + str(pictures_amount_y)
	print "NA LIST " + str(pictures_on_canvas)

	output = []

	listov = (len(img_dict) / pictures_on_canvas) + 1
	# print 20/12
	print "LISTOV " + str(listov)

	lines = zip(*[iter(img_dict)] * pictures_amount_x)
	print "VSEGO LINIY " + str(len(lines))

	# canvas = Image.new("RGB", (width,height), (255,255,255))
	# canvas.show()


	# print len(lines)

	canvas = Image.new("RGB", (width,height), (255,255,255))
	y = Y_OFFSET
	for line_num in range(0, len(lines)):
		fit_line(canvas, lines[line_num], y, image_size)
		y = y + image_size - 1
		print (line_num + 1) % pictures_amount_y
		# print (line_num + 1) == (pictures_on_canvas / (pictures_on_canvas / pictures_amount_x) - 1):
		if line_num == len(lines)-1:
			output.append(canvas)
		if (line_num + 1) % pictures_amount_y == 0:
			print "NEW CANVAS"
			output.append(canvas)
			canvas = Image.new("RGB", (width,height), (255,255,255))
			y = Y_OFFSET
	for holst in output:
		holst.show()
		# print dir(time)
		print str(time.time())[:-3]
		file_name = OUTPUT_FOLDER+'\\%s.jpg' % str(time.time())[:-3]
		holst.save(file_name, 'JPEG')
		# holst.
		# print line
		# fit_line(canvas, line, Y_OFFSET, image_size)


	# for obj in mas:
	# 	file_name = PICTS_FOLDER+'\\%s.jpg' % obj['oid']
	# 	print file_name
	# 	save_picture(file_name, obj['url'])

	# ======
	# output = []
	# for l in range(1, len(lines)):
	# 	y = Y_OFFSET
	# 	canvas = Image.new("RGB", (width,height), (255,255,255))
	# 	while l <= pictures_amount_y:
	# 		i = 0
	# 		x = X_OFFSET
	# 		while i < len(lines[l]):
	# 			canvas.paste(lines[l][i], (x,y))
	# 			# canvas.show()
	# 			x = x + image_size - 1
	# 			i += 1
	# 			print l, i
	# 		print "===="
	# 		y = y + image_size
	# 		l = l + 1
	# 	print "+++"
	# 	x = 0
	# 	y = 0
	# 	canvas.show()
	# 	output.append(canvas)



		# if i == pictures_amount_y:
		# 	print "DDDDDDDDDDD"
		# 	x = X_OFFSET
		# 	y = Y_OFFSET
		# 	i = 0

		# =====









	# for line in lines:
	# 	i = 0
	# 	x = X_OFFSET
	# 	# for i in range(0, len(line)):
	# 	# 	print line[i]
	# 	while i < len(line):
	# 		# print i
	# 		# print line[i]
	# 		canvas.paste(line[i], (x,y))
	# 		x = x + image_size
	# 		i += 1
	# 	y = y + image_size
	# canvas.show()

	# output = []
	# for l in range(0, len(lines)):
	# 	i = 0
	# 	x = X_OFFSET
	# 	# for i in range(0, len(line)):
	# 	# 	print line[i]
	# 	while i < len(lines[l]):
	# 		# print i
	# 		# print line[i]
	# 		canvas.paste(lines[l][i], (x,y))
	# 		x = x + image_size
	# 		i += 1
	# 	y = y + image_size
	# 	l = l + 1
	# 	if l >= pictures_amount_y:
	# 		# canvas.show()
	# 		output.append(canvas)
	# 		canvas = Image.new("RGB", (width,height), (255,255,255))
	# 		x = X_OFFSET
	# 		y = Y_OFFSET
	# 		i = 0
	# # i = 0
	# # output.append(canvas)




	# i = 0
	# output.append(canvas)

	# for item in output:
	# 	item.show()

	# for lane in range(0, len(lines)):
		


	# canvas = Image.new("RGB", (width,height), (255,255,255))
	# while img_num <= len(img_dict):
	# 	while canvas_num <= len(img_dict) / pictures_on_canvas + 1:
	# 		line = 1
	# 		x = 0
	# 		y = 0
	# 		position = 1
	# 		while line <= pictures_amount_y and img_num <= len(img_dict):
	# 			while position <= pictures_amount_x and img_num <= len(img_dict):
	# 				image = img_dict[img_num]
	# 				canvas.paste(image, (x,y))
	# 				canvas.show()
	# 				# image.show()
	# 				print img_num + 1
	# 				print "canvas %s" % canvas_num
	# 				print "line %s" % line
	# 				print "photo %s" % position
	# 				img_num = img_num + 1
	# 				position = position + 1
	# 			x = x + width
	# 			y = y + width
	# 			line = line + 1
	# 		canvas_num = canvas_num + 1


		# print line 


	# while img_num <= len(img_dict):
	# 	img_num = img_num + 1
	# 	while img_num <= pictures_on_canvas:
	# 		print img_num
	# 		print canvas_num
	# 		print "---"
	# 	canvas_num = canvas_num + 1
		# while img_num < pictures_on_canvas:
			# print img_num
		# time.sleep(2)
		# print 'img_num %s' % img_num
		# for canvas_num in range(0, 5):
		# 	print canvas_num
			# print 'canvas_num %s' % len(img_dict)/pictures_on_canvas
			
			# canvas = Image.new("RGB", (width,height), (255,255,255))
			# canvas.show()
			
			# canvas.paste(img_dict[img_num], (0,0))
			# output.append(canvas)

# resized = load_and_resize(40, IMG_SIZE, IMG_SIZE)
# framed_dict = frame(resized)


# fit_to_canvas(framed_dict, CANVAS_X_SIZE, CANVAS_Y_SIZE)
# print len(get_links())



#==================================
# import aggdraw
# image = Image.new("RGB", (320,320), (0,0,0))

# draw = ImageDraw.Draw(image)

# draw.ellipse((10,10,300,300), fill="red", outline="red")

# del draw

# image.save('C:/gram/picts/ellips.png', 'PNG')







			


#####
#####



# image1 = Image.open('C:/gram/picts/1.jpg')
# image2 = Image.open('C:/gram/picts/1.jpg')

# image3 = Image.merge('RGB', (image1, image2))

# image3.save('C:/gram/picts/ellips.jpg', 'JPG')

if  __name__ ==  "__main__" :
	run()