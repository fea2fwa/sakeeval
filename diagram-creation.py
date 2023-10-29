import cv2
import numpy as np

# 線を描画する関数
def draw_line(image, point1, point2, color, thickness, flag):
    if flag == 1:
        # 点線を描画する
        length = int(np.linalg.norm(np.array(point1) - np.array(point2)))
        step = 8  # 10ピクセルごとに点を打つ
        for i in range(0, length, 2*step):
            start = (point1[0] + int((point2[0] - point1[0]) * i / length), 
                     point1[1] + int((point2[1] - point1[1]) * i / length))
            end = (point1[0] + int((point2[0] - point1[0]) * (i + step) / length), 
                   point1[1] + int((point2[1] - point1[1]) * (i + step) / length))
            cv2.line(image, start, end, color, thickness)
    else:
        # 通常の線を描画する
        cv2.line(image, point1, point2, color, thickness)

# 画像を読み込む
image = cv2.imread('basic_wine.png')

# 線の始点と終点
lines = [
    {"start": (225, 72), "end": (240, 127), "color": (0, 165, 255), "thickness": 6, "flag": 0},  # 太さを6に、色をオレンジに
    {"start": (240, 127), "end": (1362, 182), "color": (210, 210, 210), "thickness": 6, "flag": 1},  # 太さを6に、色を薄い灰色に
    {"start": (1362, 182), "end": (800, 235), "color": (210, 210, 210), "thickness": 6, "flag": 1},  # 太さを6に、色を薄い灰色に
    {"start": (800, 235), "end": (1000, 287), "color": (0, 165, 255), "thickness": 6, "flag": 0},  # 太さを6に、色を薄い灰色に
    {"start": (1000, 287), "end": (300, 342), "color": (0, 165, 255), "thickness": 6, "flag": 0},  # 太さを6に、色を薄い灰色に
    {"start": (300, 342), "end": (600, 510), "color": (0, 165, 255), "thickness": 6, "flag": 0},  # 太さを6に、色を薄い灰色に
]

# 線を描画する
for line in lines:
    draw_line(image, line["start"], line["end"], line["color"], line["thickness"], line["flag"])

# 画像を表示する
cv2.imshow('Image with Lines', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
