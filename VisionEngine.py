import cv2
import numpy as np
import requests
import file_helper


def drawBox(img, bbox):
    x, y, w, h = [int(i) for i in bbox]
    cv2.rectangle(img, (x,y), (x+w,y+h), (255, 0, 255), 3, 1)
    cv2.putText(img, "Tracking", (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)


def movementDetection():
    cap = cv2.VideoCapture(0)

    # tracker = cv2.legacy.TrackerMOSSE_create()
    tracker = cv2.legacy.TrackerCSRT_create()

    success, img = cap.read()
    bbox = cv2.selectROI("Tracking", img, False)
    tracker.init(img, bbox)

    while True:
        timer = cv2.getTickCount()
        success, img = cap.read()

        success, bbox = tracker.update(img)

        print(bbox)
        if success:
            drawBox(img, bbox)
        else:
            cv2.putText(img, "Lost", (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        fps = cv2.getTickFrequency() / cv2.getTickCount() - timer
        cv2.putText(img, str(int(fps)), (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("Tracking", img)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break


def change_dimension(frame, ratio):
    shape = frame.shape
    img = cv2.resize(frame, (shape[1] // ratio, shape[0] // ratio))
    return img


def objectMovementDetection(camera, external=None,precious= False, ratio = 1):
    cap = cv2.VideoCapture(camera)

    # tracker = cv2.legacy.TrackerMOSSE_create()
    tracker = cv2.legacy.TrackerCSRT_create()


    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    frame_height =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc('X','V','I','D')

    out = cv2.VideoWriter("output.avi", fourcc, 5.0, (1280,720))

    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    frame1 = change_dimension(frame1, ratio)
    frame2 = change_dimension(frame2, ratio)
    print(frame1.shape)

    bbox = cv2.selectROI("Tracking", frame1, False)
    tracker.init(frame1, bbox)

    while cap.isOpened():


        timer = cv2.getTickCount()
        success, img = cap.read()
        img = change_dimension(img, ratio)

        success, bbox = tracker.update(img)

        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if precious == True:
            cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

        else:
            for contour in contours:
                (x, y, w, h) = cv2.boundingRect(contour)

                if cv2.contourArea(contour) < 900:
                    continue
                cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 255), 3)


        image = cv2.resize(frame1, (1280,720))
        out.write(image)


        print(bbox)
        if success:
            drawBox(frame1, bbox)
        else:
            cv2.putText(frame1, "Lost", (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        fps = cv2.getTickFrequency() / cv2.getTickCount() - timer
        cv2.putText(frame1, str(int(fps)), (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


        if external == True:
            cv2.imshow("feed", frame1)
        else:
            get_image = frame1

        frame1 = frame2
        ret, frame2 = cap.read()
        frame2 = change_dimension(frame2, ratio)

        if external == True:
            if cv2.waitKey(40) == 27:
                break
        else:
            return get_image

    if external == True:
        cv2.destroyAllWindows()
        cap.release()
        out.release()


def objectDetection(camera, precious= False):
    cap = cv2.VideoCapture(camera)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    frame_height =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc('X','V','I','D')

    out = cv2.VideoWriter("output.avi", fourcc, 5.0, (1280,720))

    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    print(frame1.shape)
    while cap.isOpened():
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if precious == True:
            cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

        else:
            for contour in contours:
                (x, y, w, h) = cv2.boundingRect(contour)

                if cv2.contourArea(contour) < 900:
                    continue
                cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 255), 3)


        image = cv2.resize(frame1, (1280,720))
        out.write(image)
        cv2.imshow("feed", frame1)
        frame1 = frame2
        ret, frame2 = cap.read()

        if cv2.waitKey(40) == 27:
            break

    cv2.destroyAllWindows()
    cap.release()
    out.release()


# if __name__ == "__main__":
    # objectDetection(True)
    # movementDetection()
    # objectMovementDetection(camera= 'https://192.168.43.1:8080/video', precious=True, external=True, ratio= 4)
