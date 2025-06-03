import cv2
from qreader import QReader


image = cv2.cvtColor(cv2.imread("images/qr.jpg"), cv2.COLOR_BGR2RGB)

qreader = QReader()

link = qreader.detect_and_decode(image=image)

url = link[0]