import numpy as np
import cv2

#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(r'http://124.70.166.171:7081/live/live.m3u8?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NfbW9kZSI6IkhPTE8iLCJjaGFubmVsX2lkIjowLCJkZXZpY2VfaWQiOiIyMTAyNDEyNTM5OVNNNjAwMjk1NyIsImV4cGlyZV90aW1lIjoxNjMyODg5NTI4LCJyZXF1ZXN0X2lkIjoiNjNlYWEzMzAtOGU4Mi00NjFiLTgxYmQtY2Y3YTYwOWZlMzkxIiwic3RyZWFtX3R5cGUiOjAsInVzZXJfaWQiOiIiLCJ1c2VyX3R5cGUiOiJFTlRFUlBSSVNFIiwidXVpZCI6IjQyZGM5YzFiLTIxMjAtMTFlYy05MGEyLWZhMTYzZTI5ZGI2OSJ9.29ilj59P4dmR7a_mTZkC7vEHW488dxlJP-GKB03-qb4&device_id=21024125399SM6002957&channel_id=0&stream_type=0')
# 定义解码器并创建VideoWrite对象
# linux: XVID、X264; windows:DIVX
# 20.0指定一分钟的帧数
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('output.avi', fourcc, 25.0, (640, 480))

while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        frame = cv2.flip(frame, 0)

        # 写入帧
        out.write(frame)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# 释放内存
cap.release()
out.release()
cv2.destroyAllWindows()