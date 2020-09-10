import cv2
import numpy as np


def canny_edge_detector(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray_image, (5, 5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny

def region_of_interest(image):
    L_camera = image.shape[1]
    H_camera = image.shape[0]
    roi_poligon = np.array([[[10, 500], [10, 400], [300, 250], [500, 250], [800, 500], [800, 500]]], dtype=np.int32)
   # roi_poligon = np.array([[(0, 0.8*H_camera), (0.25*L_camera, 0.3*H_camera),
   #                          (0.75*L_camera, 0.3*H_camera), (L_camera, 0.8*H_camera)]], dtype=np.int32)
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, roi_poligon, 255)
    masked_frame = cv2.bitwise_and(image, mask)
    return masked_frame

def create_coordinates(image, line_parameters): #coordonatele benzii
    try:
        slope, intercept = line_parameters
    except:
        slope, intercept = 1, 0
    y1 = image.shape[0]
    y2 = int(y1 * (3 / 5))
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])


def average_slope_intercept(image, lines): #separa liniile in stanga si dreapta si creeaza o linie medie
    left_fit = []
    right_fit = []
    try:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)

            # It will fit the polynomial and the intercept and slope
            parameters = np.polyfit((x1, x2), (y1, y2), 1)
            slope = parameters[0]
            intercept = parameters[1]
            if slope < 0:
                left_fit.append((slope, intercept))
            else:
                right_fit.append((slope, intercept))
    except:
        pass

    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_line = create_coordinates(image, left_fit_average)
    right_line = create_coordinates(image, right_fit_average)
    return np.array([left_line, right_line])

def display_lines(image, lines): #afiseaza liniile
    line_image = np.zeros_like(image)
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            cv2.line(line_image, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 10)
    return line_image


cap = cv2.VideoCapture("cameraE.avi")

while (cap.isOpened()):
    check, frame = cap.read()

    frame2=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    rows = frame.shape[0]
    cols = frame.shape[1]

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV);

    for i in range(0, cols):
        for j in range(0, rows):
            hsv[j, i][1] = 255;


    frame3 = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB);

    cv2.imshow("Frame", frame3)


    _,th=cv2.threshold(frame2,190,255,cv2.THRESH_BINARY)
    r, g, b = cv2.split(frame)
    _, tb=cv2.threshold(b, 190, 255, cv2.THRESH_BINARY)
    _, tg = cv2.threshold(g, 190, 255, cv2.THRESH_BINARY)
    _,tr = cv2.threshold(r, 190, 255, cv2.THRESH_BINARY)


    input = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    points1 = np.float32([[210, 100], [430, 100], [0, 260], [640, 260]])
    points2 = np.float32([[0, 0], [640, 0], [0, 480], [640, 480]])
    P = cv2.getPerspectiveTransform(points1, points2)
    output = cv2.warpPerspective(input, P, (640, 480))

    canny_image = canny_edge_detector(frame)
    cropped_image = region_of_interest(canny_image)

    lines = cv2.HoughLinesP(cropped_image, 2, np.pi / 180, 190,
                            np.array([]), minLineLength=10,
                            maxLineGap=5)

    averaged_lines = average_slope_intercept(frame, lines)
    line_image = display_lines(frame, averaged_lines)
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)

    #cv2.imshow("output", output)
    cv2.imshow("b", tb)
    cv2.imshow("g", tg)
    cv2.imshow("r", tr)
    cv2.imshow("TH", th)

    #cv2.namedWindow("results", cv2.WINDOW_NORMAL)
    #cv2.imshow("results", combo_image)
    #cv2.resizeWindow("results", 768, 432)

    #cv2.namedWindow("roi", cv2.WINDOW_NORMAL)
   # cv2.imshow("roi", cropped_image)
    #cv2.resizeWindow("roi", 768, 432)

    cv2.waitKey(0)  # 1=readare automata // 0=redare la buton
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()