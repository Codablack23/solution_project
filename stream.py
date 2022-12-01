import numpy as np
import cv2

def showCam(ip):
    capture = cv2.VideoCapture(ip)
    fourcc = cv2.VideoWriter_fourcc(*'PIM1')
    out = cv2.VideoWriter('clip.avi',fourcc, 20.0, (640,480))

    while(True):
        # Capture frame-by-frame
        ret, frame = capture.read()
        if ret==True:
                frame = cv2.flip(frame,0)
                print(frame)
                # write the flipped frame
                out.write(frame)

                cv2.imshow('frame',frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        else:
            break

    # When everything done, release the capture
    capture.release()
    cv2.destroyAllWindows()