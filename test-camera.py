import cv2
import time

cap = cv2.VideoCapture(0)
time.sleep(0.1)

while cap.isOpened():
    ret, frame_mare = cap.read()
    if ret is False:
        break
    H, W, _ = frame_mare.shape
    if H > 480 and W > 640:
        frame = cv2.resize(frame_mare, (640, 480), interpolation=cv2.INTER_AREA)
    else:
        frame = frame_mare

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, binarization = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
    cv2.imshow("frame", frame)
    cv2.imshow("binarizare", binarization)
    cv2.waitKey(1)  # 1=readare automata // 0=redare la buton
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()