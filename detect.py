import threading                                                    # Import threading module
import winsound                                                     # Import winsound module                             

import cv2                                                          # Import OpenCV module                            
import imutils                                                      # Import imutils module           

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)                                           # Capture video from webcam
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)                              # Set frame width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)                             # Set frame height


_, start_frame = cap.read()                                         # Read first frame
start_frame = imutils.resize(start_frame, width=500)                # Resize frame
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)         # Convert to grayscale
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)            # Apply Gaussian blur

alarm_status = False                                                # Set alarm status to False
alarm_mode = False                                                  # Set alarm mode to False
alarm_counter = 0                                                   # Set alarm counter to 0

def alarm():                                                        # Define alarm function
    # specify what you want if alarm is triggered
    global alarm                                                    # Use global variable
    for i in range(10):                                              # Loop 5 times
        if not alarm_mode:                                          # If alarm mode is False
            break
        
        print("Alarm triggered!")                                   # Print alarm triggered
        winsound.Beep(2500, 1000)                                   # Play beep sound at 2500Hz for 1000ms
    alarm = False                                                   # Set alarm to False  


while True:                                                         # Loop forever
    _, frame = cap.read()                                           # Read frame
    frame = imutils.resize(frame, width=500)                        # Resize frame
    
    if alarm_mode:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)          # Convert to grayscale
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)            # Apply Gaussian blur

        difference = cv2.absdiff(frame_bw, start_frame)                                                 # Calculate difference between start frame and current frame
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]                            # Apply threshold to calculate difference

        start_frame = frame_bw                                                                          # Set start frame to current frame

        if threshold.sum() > 1000000:                                                                       # If difference is greater than 300
             alarm_counter += 1                                                                         # Increment alarm counter by 1
        else:
            if alarm_counter > 0:                                                                       # If alarm counter is greater than 0
                alarm_counter -= 1                                                                      # Decrement alarm counter by 1

        cv2.imshow("Cam_Threshold", threshold)                                                              # Show threshold image
    else:
        cv2.imshow("Cam", frame)                                                                            # Show frame
        
    if alarm_counter > 50:                                                                                  # If alarm counter is greater than 20

            if not alarm_status:                                                                        # If alarm status is False
                alarm_status = True                                                                     # Set alarm status to True
                print("Alarm triggered!")                                                               # Print alarm triggered
                threading.Thread(target=alarm).start()                                                  # Start alarm thread
                #alarm_counter += 1                                                                      # Increment alarm counter by 1

                print("Alarm counter: {}".format(alarm_counter))                                        # Print alarm counter
    
    key_pressed = cv2.waitKey(30)                                                                        # Wait for key press
    if key_pressed == ord('t'):                                                                         # If key pressed is t
         alarm_mode = not alarm_mode                                                                    # Toggle alarm mode
         alarm_counter = 0                                                                              # Set alarm counter to 0

    if key_pressed == ord('q'):                                                                         # If key pressed is q
         alarm_mode = False                                                                             # Set alarm mode to False
         break                                                                                           # Break loop
    

cap.release()                                                                                           # Release video capture
cv2.destroyAllWindows()                                                                                 # Destroy all windows

            


        

