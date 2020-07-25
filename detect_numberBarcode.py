import cv2
import numpy as np
import glob

def run():
	def sort_contours(cnts):

			reverse = False
			i = 0
			boundingBoxes = [cv2.boundingRect(c) for c in cnts]
			(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
																					key=lambda b: b[1][i], reverse=reverse))
			return cnts

	# Dinh nghia cac ky tu tren bien so
	char_list =  '0123456789ABCDEFGHKLMNPRSTUVXYZ'

	# Ham fine tune bien so, loai bo cac ki tu khong hop ly
	def fine_tune(lp):
			newString = ""
			for i in range(len(lp)):
					if lp[i] in char_list:
							newString += lp[i]
			return newString

	digit_w = 30
	digit_h = 60

	# test = cv2.imread('so32.png', 0)

	# curr_num = np.array(test,dtype=np.float32)
	# curr_num = curr_num.reshape(-1, digit_w * digit_h)

	model_svm = cv2.ml.SVM_load('svm.xml')
	# result = model_svm.predict(curr_num)[1]
	# result = int(result[0, 0])
	# print(result)
	# Chuyen doi anh bien so
	barcode = cv2.imread("barcode.png",1)
	cv2.imshow("barcode", barcode)
	cv2.waitKey()
	barcode = cv2.convertScaleAbs(barcode, alpha=(1))
	cv2.imshow("gray", barcode)
	cv2.waitKey()
	roi = barcode

	# Chuyen anh bien so ve gray
	gray = cv2.cvtColor(barcode, cv2.COLOR_BGR2GRAY)
	cv2.imshow("gray", gray)
	cv2.waitKey()
	# Ap dung threshold de phan tach so va nen
	binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)[1]
	cv2.imshow("binary", binary)
	cv2.waitKey()

	# Segment kí tự
	kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
	cv2.imshow("kernel3", kernel3)
	cv2.waitKey()
	# thre_mor = cv2.morphologyEx(binary, cv2.MORPH_DILATE, kernel3)
	# cv2.imshow("Anh bien so sau threshold", thre_mor)
	# cv2.waitKey()
	thre_mor = binary
	cont, _  = cv2.findContours(thre_mor, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)


	plate_info = ""
	x_pre = 0
	w_pre =0
	dem = 1
	for c in sort_contours(cont):
		#print(c)
		(x, y, w, h) = cv2.boundingRect(c)
		ratio = h/w
		if x < (x_pre + w_pre*0.5):
			continue
		if 1.2<ratio<3: # Chon cac contour dam bao ve ratio w/h
			if h/roi.shape[0]>=0.06: # Chon cac contour cao tu 60% bien so tro len
							# Ve khung chu nhat quanh so

				cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)
							# Tach so va predict
				curr_num = thre_mor[y:y+h,x:x+w]
				curr_num = cv2.resize(curr_num, dsize=(digit_w, digit_h))
				_, curr_num = cv2.threshold(curr_num, 30, 255, cv2.THRESH_BINARY)
				curr_num = np.array(curr_num,dtype=np.float32)
				curr_num = curr_num.reshape(-1, digit_w * digit_h)

				# Dua vao model SVM
				result = model_svm.predict(curr_num)[1]
				result = int(result[0, 0])
				if result<=9: # Neu la so thi hien thi luon
					result = str(result)
				else: #Neu la chu thi chuyen bang ASCII
					result = chr(result)
				x_pre = x
				w_pre = w
				plate_info +=result
	#cv2.imshow("Cac contour tim duoc", roi)
	#cv2.waitKey()

	# Viet bien so len anh

	# Hien thi anh
	#print("Bien so=", plate_info)
	#cv2.imshow("Hinh anh output",barcode)
	#cv2.waitKey()
	return plate_info