# import the necessary packages
import numpy as np
import argparse
import imutils
import glob
import cv2

def detectBarcode(inputImage):
	def sort_contours(cnts):

			reverse = False
			i = 0
			boundingBoxes = [cv2.boundingRect(c) for c in cnts]
			(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes), key=lambda b: b[1][i], reverse=reverse))
			return cnts

	ap = argparse.ArgumentParser()

	ap.add_argument("-v", "--visualize",
		help="Flag indicating whether or not to visualize each iteration")
	args = vars(ap.parse_args())
	template = cv2.imread("template.png")
	template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
	template = cv2.Canny(template, 50, 200)
	(tH, tW) = template.shape[:2]
	#cv2.imshow("Template", template)
	# load the image, convert it to grayscale, and initialize the
	# bookkeeping variable to keep track of the matched region
	image = cv2.imread(inputImage)
	if image.shape[1] > 3000:
		scale_percent = 20 # percent of original size
	elif image.shape[1] > 2000:
		scale_percent = 60 # percent of original size
	else:
		scale_percent = 100 # percent of original size
	width = int(image.shape[1] * scale_percent / 100)
	height = int(image.shape[0] * scale_percent / 100)
	dim = (width, height)
	# resize image
	image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	found = None
	# loop over the scales of the image
	for scale in np.linspace(0.2, 1.0, 20)[::-1]:
		# resize the image according to the scale, and keep track
		# of the ratio of the resizing
		resized = imutils.resize(gray, width = int(gray.shape[1] * scale))
		r = gray.shape[1] / float(resized.shape[1])
		# if the resized image is smaller than the template, then break
		# from the loop
		if resized.shape[0] < tH or resized.shape[1] < tW:
			break
	# detect edges in the resized, grayscale image and apply template
		# matching to find the template in the image
		edged = cv2.Canny(resized, 50, 200)
		result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
		(_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
		if args.get("visualize", False):
		# draw a bounding box around the detected region
			clone = np.dstack([edged, edged, edged])
			cv2.rectangle(clone, (maxLoc[0], maxLoc[1]),
				(maxLoc[0] + tW, maxLoc[1] + tH), (0, 0, 255), 2)
			cv2.imshow("Visualize", clone)
			cv2.waitKey(0)
		# the bookkeeping variable
		if found is None or maxVal > found[0]:
			found = (maxVal, maxLoc, r)
	# unpack the bookkeeping variable and compute the (x, y) coordinates
	# of the bounding box based on the resized ratio
	(_, maxLoc, r) = found
	(startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
	(endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
	# draw a bounding box around the detected result and display the image
	barcode = image[startY:endY,startX:endX]

	#cat chinh xac barcode
	barcode = cv2.resize(barcode, dsize=(500, 300))

	barcode = cv2.convertScaleAbs(barcode, alpha=(1))

	roi = barcode.copy()

	# Chuyen anh bien so ve gray
	gray = cv2.cvtColor(barcode, cv2.COLOR_BGR2GRAY)

	# Ap dung threshold de phan tach so va nen
	binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)[1]

	cont, _  = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	count = 0
	for c in sort_contours(cont):
		#print(c)
		(x, y, w, h) = cv2.boundingRect(c)
		ratio = h/w
		if 4<ratio: # Chon cac contour dam bao ve ratio w/h
			if h/roi.shape[0]>=0.06: # Chon cac contour cao tu 60% bien so tro len
							# Ve khung chu nhat quanh so
				if count == 0:
					(x_start, y_start, w_start, h_start) = (x, y, w, h)
				count +=1
				cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)
				(x_end, y_end, w_end, h_end) = (x, y, w, h)
	w_bar = int((x_end - x_start))
	h_bar = int(h_start*1.12)
	if int(w_bar*0.12) > x_start:
		x_start = 1
	else:
		x_start = int(x_start - w_bar*0.12)

	w_bar = int(w_bar*1.2)
	if w_bar > 500:
		w_bar = 499
	if (y_end + h_bar) > 300:
		h_bar = 299
	else:
		h_bar = y_end + h_bar

	barcode_new = barcode[y_start:h_bar, x_start:x_start+w_bar]
	barcode_new = cv2.resize(barcode_new, dsize=(300,200))
	cv2.waitKey()
	cv2.imwrite("barcode.png", barcode_new)


