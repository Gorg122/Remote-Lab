import os

import time
import cv2


def Video():
    #cap = cv2.VideoCapture(0)

    HIGH_VALUE = 10000
    WIDTH = HIGH_VALUE
    HEIGHT = HIGH_VALUE

    capture = cv2.VideoCapture(0)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    capture.set(cv2.CAP_PROP_AUTOFOCUS, 1)
    frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cur_dir = os.getcwd()
    print(cur_dir)
    print(frame_width)
    print(frame_height)
    files = "video_timing.txt"
    timing = open(files)
    time_rest = timing.readline()
    print(time_rest)
    timing.close()

    tik = time.time()
    print(tik)
    tok = 0.0
    out = cv2.VideoWriter('video/output.mp4', fourcc, 30.0, (frame_width, frame_height))

    print("tok = ", tok)
    print("tok-tik = ", tok - tik)
    start = 0
    while(capture.isOpened() and (tok-tik<=int(time_rest) or (start == 1))):
        ret, frame = capture.read()
        tok = time.time()
        if ret==True :
            out.write(frame)
            if int(tok - tik) >= int(time_rest):
                break
        else:
            break

    # Release everything if job is finished
    capture.release()
    out.release()
    cv2.destroyAllWindows()
    time.sleep(4)
    files_2 = "video_done.txt"
    done_chek = open(files_2, "w")
    done_chek.write("done")
    done_chek.close()
    quit()
if __name__ == '__main__':
    Video()


import cv2
import time
import numpy as np
import json

video_path = 'video.mp4'
cap = cv2.VideoCapture(video_path)

# Создайте окно для просмотра видео
cv2.namedWindow('Video')

# Инициализируйте переменные для управления воспроизведением
paused = False

# Задайте координаты квадратов массивом
rectangles = [
    [(261, 360), (267, 365)],
    [(284, 360), (290, 365)],
    [(306, 359), (312, 364)],
    [(332, 359), (338, 364)],
    [(355, 358), (361, 363)],
    [(381, 358), (387, 363)],
    [(403, 357), (410, 362)],
    [(427, 356), (434, 361)],
    [(453, 356), (459, 361)],
    [(476, 355), (482, 360)],
    # First number
    [(32, 390), (37, 395)],
    [(12, 390), (17, 395)],
    [(22, 383), (27, 388)],
    [(22, 402), (27, 407)],
    [(18, 422), (23, 427)],
    [(8, 412), (13, 417)],
    [(28, 412), (33, 417)],
    # Second number
    [(72, 390), (77, 395)],
    [(52, 390), (57, 395)],
    [(62, 383), (67, 388)],
    [(62, 402), (67, 407)],
    [(58, 422), (63, 427)],
    [(48, 412), (53, 417)],
    [(68, 412), (73, 417)],
    # Third number
    [(117, 387), (122, 392)],
    [(98, 387), (103, 392)],
    [(107, 380), (112, 385)],
    [(107, 399), (112, 404)],
    [(103, 419), (108, 424)],
    [(93, 409), (98, 414)],
    [(113, 409), (118, 414)],
    # Fourth number
    [(155, 387), (160, 392)],
    [(138, 387), (143, 392)],
    [(148, 380), (153, 385)],
    [(145, 399), (150, 404)],
    [(146, 419), (151, 424)],
    [(136, 409), (141, 414)],
    [(153, 409), (158, 414)],
    # Fifth number
    [(198, 387), (203, 392)],
    [(178, 387), (183, 392)],
    [(188, 380), (193, 385)],
    [(188, 399), (193, 404)],
    [(186, 419), (191, 424)],
    [(176, 409), (181, 414)],
    [(196, 409), (201, 414)],
    # Sixth number
    [(240, 385), (245, 390)],
    [(220, 385), (225, 390)],
    [(230, 378), (235, 383)],
    [(228, 397), (233, 402)],
    [(228, 417), (233, 422)],
    [(218, 407), (223, 412)],
    [(238, 407), (243, 412)],
]


# Rectangles for numbers
diode_mask_old = [False] * len(rectangles)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # To grayscale

    color = (255, 0, 0)
    diode_mask_new = [False] * len(rectangles)
    flag_mask_changed = False

    for idx, rect in enumerate(rectangles):
        cv2.rectangle(frame, rect[0], rect[1], color, 2)  # Draw rectangle

        # Извлечь область квадрата из кадра
        x1, y1 = rect[0]
        x2, y2 = rect[1]
        roi = frame[y1:y2, x1:x2]  # Truncated frame for one diode

        diode_mask_new[idx] = bool(roi.mean(axis=(0, 1)) > 230)  # Switched on condition

    if diode_mask_new != diode_mask_old:
        diode_mask_old = diode_mask_new
        flag_mask_changed = True

    cv2.imshow('Video', frame)

    key = cv2.waitKey(30)

    if flag_mask_changed:   # Print only if diode mask changed
        json_data = json.dumps(diode_mask_new)
        print(json_data)

    # Обработка клавиш:
    if key == ord('q'):
        break
    elif key == ord('r'):
        # Сброс в начало видео (нажмите 'r')
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)


# Освободите видеопоток и закройте окно
cap.release()
cv2.destroyAllWindows()