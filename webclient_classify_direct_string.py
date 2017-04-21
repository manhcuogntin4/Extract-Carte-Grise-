import SOAPpy
from PIL import Image
import glob
import sys
import pickle
reload(sys)
import base64
import cv2
server = SOAPpy.SOAPProxy("http://127.0.0.1:5000/")

#server = SOAPpy.SOAPProxy("http://34.251.67.157:80/")

CLASSES = ('__background__', # always index 0
           'carte', 'mrz', 'numero', 'date', 'nom','prenom','adresse', 'ville', 'marque', 'type_mine')
def readFileImages(strFolderName):
	print strFolderName
	image_list = []
	st=strFolderName+"*.png"
	for filename in glob.glob(st): #assuming gif
	    image_list.append(filename)
	return image_list

def writeFileOCR(f, txt_ocr):
	f.write(txt_ocr)
	return annotations

def ocr_Images(image_list, f):
	for filename in image_list:
		result=server.detect_carte_grise(filename)
			# with open(f, 'wb') as output:
			# 	pickle.dump(it, output, pickle.HIGHEST_PROTOCOL)
		print result[0][0][1].__dict__.keys()
		# for cls in list(result[0][0][1][0]):
		# 	#if result[0][0][1][cls] is not None: 
		# 		print cls[0] 

path="t.png"


def convert_image_to_string(path):
	image=cv2.imread(path,1)
	cv2.imwrite("out.png",image)
	with open("out.png", "rb") as imageFile:
		st = base64.b64encode(imageFile.read())
	return st



st=convert_image_to_string(path)



#data  = json.dumps(a[0][0])
result=server.classify_image_string(st)
print result

#result = server.detect_carte_grise(filename)

