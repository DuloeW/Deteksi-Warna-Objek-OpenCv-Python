
# import the necessary packages
from pyimagesearch.shapedetector import ShapeDetector
from pyimagesearch.colorlabeler import ColorLabeler
import imutils
import cv2

# initialize the shape detector and color labeler
sd = ShapeDetector()
cl = ColorLabeler()

# open webcam
cap = cv2.VideoCapture(1)
if not cap.isOpened():
	print("Cannot open camera")
	exit()


while True:
	ret, frame = cap.read()
	if not ret:
		print("Can't receive frame. Exiting...")
		break

	resized = imutils.resize(frame, width=300)
	ratio = frame.shape[0] / float(resized.shape[0])
	blurred = cv2.GaussianBlur(resized, (5, 5), 0)
	gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
	lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
	thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]

	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	# copy frame for drawing
	output = frame.copy()

	frame_height, frame_width = frame.shape[:2]
	center_x, center_y = frame_width // 2, frame_height // 2

	# area tengah: kotak 20% dari lebar/tinggi di tengah
	box_w, box_h = int(frame_width * 0.2), int(frame_height * 0.2)
	box_x1, box_y1 = center_x - box_w // 2, center_y - box_h // 2
	box_x2, box_y2 = center_x + box_w // 2, center_y + box_h // 2
	
	# gambar kotak area tengah
	cv2.rectangle(output, (box_x1, box_y1), (box_x2, box_y2), (255, 0, 0), 2)

	for c in cnts:
		M = cv2.moments(c)
		if M["m00"] == 0:
			continue
		cX = int((M["m10"] / M["m00"]) * ratio)
		cY = int((M["m01"] / M["m00"]) * ratio)
		shape = sd.detect(c)
		color = cl.label(lab, c)
		c = c.astype("float")
		c *= ratio
		c = c.astype("int")
		text = "{} {}".format(color, shape)
		cv2.drawContours(output, [c], -1, (0, 255, 0), 2)
		cv2.putText(output, text, (cX, cY),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

		# cek apakah pusat objek di area tengah
		if box_x1 <= cX <= box_x2 and box_y1 <= cY <= box_y2:
			cv2.putText(output, "Objek di Tengah!", (center_x - 80, center_y - box_h // 2 - 10),
						cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)

	output = imutils.resize(output, width=770)
	cv2.imshow("Realtime Color & Shape Detection", output)

	# tekan 'q' untuk keluar
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
