#test input_image
import cv2
import numpy as np 
import imutils


digit_w = 30
digit_h = 60
model_svm = cv2.ml.SVM_load('svm.xml')

# Ham fine tune bien so, loai bo cac ki tu khong hop ly

image = cv2.imread("barcode.png",0)
gaussian_3 = cv2.GaussianBlur(image, (9,9), 10.0)
unsharp_image = cv2.addWeighted(image, 1.5, gaussian_3, -0.5, 0, image)
#blurred = cv2.blur(barcode, (3, 3))
binary = cv2.threshold(unsharp_image, 127, 255, cv2.THRESH_BINARY_INV)[1]
cont, _  = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#cont = imutils.grab_contours(cont)

#a = sorted(cont, key = cv2.contourArea, reverse = True)
a = cont
plate_info = ""
count = 0
for c in a:
	(x, y, w, h) = cv2.boundingRect(c)
	ratio = h/w
	if 1.2<ratio<3: # Chon cac contour dam bao ve ratio w/h
		cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
		rect = cv2.minAreaRect(c)
		box = cv2.cv.BoxPoints(rect) if imutils.is_cv2() else cv2.boxPoints(rect)
		box = np.int0(box)
		# draw a bounding box arounded the detected barcode and display the
		# image
		cv2.drawContours(image, [box], -1, (0, 255, 0), 3)
        # Tach so va predict
		curr_num = binary[y:y+h,x:x+w]
		curr_num = cv2.resize(curr_num, dsize=(digit_w, digit_h))
		_, curr_num = cv2.threshold(curr_num, 30, 255, cv2.THRESH_BINARY)

		cv2.imshow("Image2", curr_num)
		cv2.waitKey(0)
		curr_num = np.array(curr_num,dtype=np.float32)
		curr_num = curr_num.reshape(-1, digit_w * digit_h)
		# Dua vao model SVM
		result = model_svm.predict(curr_num)[1]
		result = int(result[0, 0])
		if result<=9: # Neu la so thi hien thi luon
			result = str(result)
		else: #Neu la chu thi chuyen bang ASCII
			result = chr(result)

		plate_info +=result
		count +=1
print(count)
print(plate_info)
cv2.imshow("Image2", binary)
cv2.waitKey(0)
cv2.imshow("Image2", image)
cv2.waitKey(0)