#encoding:utf-8


import cv2
import numpy as np
import sys

# 角点:顺时针，左上角开始
px = 10
P = [[0*px, 0*px], [243*px, 0*px], [243*px, 146*px], [0*px, 146*px]]
P_arr = np.array(P, np.float32)
proj_width = 243*px
proj_height = 146*px

img_pt = []
a4_width = int(297*px)
a4_height = int(210*px)
a4_xs = 28*px
a4_ys = 34*px


# Mouse回调
def OnMouse(event, x, y, flags, param):
    if event==cv2.EVENT_LBUTTONDOWN:
        pt = [x, y]
        img_pt.append(pt)


# 用法： python3 main.py path
if __name__=="__main__":
    # 读入图片
    if(len(sys.argv)!=2):
        print("正确的用法为： python3 main.py path")
        sys.exit(-1)
    img_path = sys.argv[1]
    img = cv2.imread(img_path)
    if(img is None):
        print("图片路径错误")
        sys.exit(-1)
    # 窗口获取像素坐标
    cv2.namedWindow("Original Image", 0)
    cv2.setMouseCallback("Original Image", OnMouse)
    cv2.imshow("Original Image", img)
    cv2.waitKey(0)
    # 获取Homography
    img_pt_arr = np.array(img_pt, np.float32)
    H, ret = cv2.findHomography(img_pt_arr, P_arr)
    # Warp
    retImg = cv2.warpPerspective(img, H, (proj_width, proj_height))
    h, w, c = retImg.shape
    print(h, w, c)
    # Insert warped to A4 paper
    a4_pp = np.ones((a4_height, a4_width, 3), np.uint8)*255
    a4_ye = a4_ys+h
    a4_xe = a4_xs+w
    a4_pp[a4_ys:a4_ye, a4_xs:a4_xe, :] = retImg
    cv2.imwrite("A4.jpg", a4_pp)
