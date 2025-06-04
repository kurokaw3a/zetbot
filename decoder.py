from qreader import QReader
import cv2
from database import update_qr

def decode_qr(path):
 
 qreader = QReader()

 image = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)

 link = qreader.detect_and_decode(image)
 update_qr(str(link).strip("(),").strip("'"))
 
 
 


