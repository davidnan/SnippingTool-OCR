import mss
import cv2
import numpy as np

with mss.mss() as sct:
    
    # Get information of monitor 2
    monitor_number = 2
    mon = sct.monitors[monitor_number]

    # The screen part to capture
    monitor = {
        "top": mon["top"],
        "left": mon["left"],
        "width": mon["width"],
        "height": mon["height"],
        "mon": monitor_number,
    }
    output = "sct-mon{mon}_{top}x{left}_{width}x{height}.png".format(**monitor)

    # Grab the data
    sct_img = sct.grab(monitor)
    img = np.array(sct.grab(monitor)) # BGR Image
    
    # Display the picture
    cv2.imshow("window", img)
    cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN) 
    cv2.waitKey(10000)
