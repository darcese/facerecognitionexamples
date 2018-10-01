import cv2
import numpy as np
import datetime
import face_recognition

def nothing(x):
    pass

cap = cv2.VideoCapture(0)

answer = "dan"
dan = "dan"
sam = "sam"
neither = "neither"
font = cv2.FONT_ITALIC

control_window = "control window -- q to quit all"

cv2.namedWindow(control_window)
category_switch = 'Left for Sam \n Middle for Dan \n Right for neither'
cv2.createTrackbar(category_switch, control_window,0,2, nothing)
capture_switch = 'Left for Capture OFF \nRight for Capture ON'
cv2.createTrackbar(capture_switch, control_window,0,1, nothing)

control_width = 600
control_height= 500
img = np.zeros((control_height,control_width,3), np.uint8)

while 1:

    ret, frame = cap.read()

    cv2.imshow('current frame --- q to quit all', frame)
    face_locations = face_recognition.face_locations(frame)

    if face_locations != []:
        face_points = face_locations[0]
        face = frame[face_points[0]:face_points[2], face_points[3]:face_points[1]]

        cv2.imshow('your face --- q to quit all', face)

        if face_points[2] - face_points[0] < control_height and (face_points[1] - face_points[3]) < control_width :
            img[0: face_points[2] - face_points[0], 0 : face_points[1] - face_points[3]] = face
            cv2.putText(img, 'The captured image will be from the',
                              (5, 400), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(img, 'your face window if there is a face.',
                                (5, 430), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(img, 'If no face, then from current frame.',
                            (5, 460), font, 1, (255, 255, 255), 1, cv2.LINE_AA)

        else:
            pass

    cv2.imshow(control_window, img)
    saving = cv2.getTrackbarPos(capture_switch, control_window)
    category = cv2.getTrackbarPos(category_switch, control_window)
    if category == 0:
        answer = "sam"
    elif category == 1:
        answer = "dan"
    else:
        answer = "neither"

    if saving:
        if answer == "neither":
            cv2.imwrite("/Users/danielarcese/Desktop/docs/facedatacollection/" + answer
                        + str(datetime.datetime.now()).replace(" ", "-") + '.png', frame)
        else:
            if saving and face_locations != []:
                cv2.imwrite("/Users/danielarcese/Desktop/docs/facedatacollection/" + answer
                            + str(datetime.datetime.now()).replace(" ", "-") + '.png', face)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

