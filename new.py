# Based on Zed code - Person Fall detection using raspberry pi camera and opencv lib. Link: https://www.youtube.com/watch?v=eXMYZedp0Uo
import cv2
import time
import requests
import json

TOKEN = "6539441771:AAGigJ7cDkKrIUGq8WpHMVvtWOAB5tGbU20"
chat_id = input("Enter your id: ")
message = "ЧЕЛОВЕК УПАЛ!"
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"



fitToEllipse = False
cap = cv2.VideoCapture("50 Ways to Fall.mp4")
time.sleep(2)

fgbg = cv2.createBackgroundSubtractorMOG2()
j = 0
fall_detected = False

while (1):
    ret, frame = cap.read()

    # Convert each frame to gray scale and subtract the background
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fgmask = fgbg.apply(gray)

        # Find contours
        contours, _ = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:

            # List to hold all areas
            areas = []

            for contour in contours:
                ar = cv2.contourArea(contour)
                areas.append(ar)

            max_area = max(areas, default=0)

            max_area_index = areas.index(max_area)

            cnt = contours[max_area_index]

            M = cv2.moments(cnt)

            x, y, w, h = cv2.boundingRect(cnt)

            cv2.drawContours(fgmask, [cnt], 0, (255, 255, 255), 3, maxLevel=0)

            if h < w:
                j += 1

            if j > 10 and not fall_detected:
                requests.get(url).json()  # Эта строка отсылает сообщение
                fall_detected = True
                cv2.putText(fgmask, 'FALL', (x, y), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # Take a screenshot of the video
                screenshot_name = f"fall_{time.time()}.jpg"
                cv2.imwrite(screenshot_name, frame)

                # Send the screenshot to the user
                files = {'photo': open(screenshot_name, 'rb')}
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={chat_id}", files=files)

            if h > w:
                fall_detected = False  # Reset flag
                j = 0
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.imshow('video', frame)

            if cv2.waitKey(33) == 27:
                break
    except Exception as e:
        break
        print(e)

cv2.destroyAllWindows()


