"""monocular-camera-calibration.py

    This Python script is a modification of the version found in the following URL:
    https://docs.opencv.org/3.4/dc/dbb/tutorial_py_calibration.html

    Author: Ana Bárbara Quintero García
    Organisation: Universidad de Monterrey
    Contact: ana.quinterog@udem.edu
    "Doy mi palabra que he hecho esta actividad con Integridad Académica.”


    EXAMPLE OF USAGE:
    python3 get-measurements.py --cam_index 0 --Z 56 --cal_file calibration-parameters/calibration_data.json
    ### EDIT: CAM INDEX AND "56" VALUE OF DISTANCE Z
"""

# Import standard libraries
import numpy as np
import argparse
from numpy.typing import NDArray
from typing import List
import cv2
import math
import json

F = False 

#ARRYAS
CoordX=[]
CoordY=[]
DisX=[]
DisY=[]
distance=[]
Increasing=[]


### Include the function def undistort_image for image distortion correction.
from monocular_camera_calibration_helpers import( 
    undistort_images
)


# Load data from calibration_data.json
def load_calibration_info(cal_file):
    """
    A function to load calibration information from a specified file.

    Parameters:
    cal_file (str): The file path to the calibration data.

    Returns:
    tuple: A tuple containing the focal length (f), principal point x-coordinate (cx), and principal point y-coordinate (cy).
    """
    with open(cal_file, 'r') as f:
        calibration_data = json.load(f)

    # Extract required values
    focal_length = calibration_data["camera_matrix"][0][0]  # Focal length (f)
    cx = calibration_data["camera_matrix"][0][2]           # Principal point x-coordinate (cx)
    cy = calibration_data["camera_matrix"][1][2]           # Principal point y-coordinate (cy)

    return focal_length, cx, cy

def compute_XYZ(x,y, calibration_info):
    """
    Esta función calcula las coordenadas en el plano del objeto utilizando
    como entrada las coordenadas del punto picado y los parámetros de 
    calibración
    """
    Z= calibration_info["Z"]
    X= Z*(x-calibration_info["cx"])/calibration_info["f"]
    Y= Z*(y-calibration_info["cy"])/calibration_info["f"]

    DisX.append(X)
    DisY.append(Y)

    print(f"X: {X}\t Y: {Y} \t Z: {Z}")

# Function to handle mouse events
def mouse_callback(event, x, y, flags, param):
       #check for left mouse button
    if event== cv2.EVENT_LBUTTONDOWN:
        #cv2.circle(frame,(x,y),5,(0,255,0),-1)
        
        CoordX.append(x)
        CoordY.append(y)


    if event == cv2.EVENT_RBUTTONDOWN:
        F = True

      

def open_webcam():
    global F 

    # Open the default camera (index 0)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Unable to open webcam.")
        return

    # Create a window to display the webcam feed
    cv2.namedWindow('Webcam')

    cv2.setMouseCallback('Webcam', mouse_callback)


    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        k = cv2.waitKey(1) 

        if k == ord(' '):
            F = True
        if k == ord('q'):
            break

        # Set mouse callback function
        
        if len(CoordX)>0:
            for i in range(len(CoordX)):
                cv2.circle(frame,(CoordX[i],CoordY[i]),10,(0,255,0),10)
                if i>0:
                    cv2.line(frame,(CoordX[i-1],CoordY[i-1]),(CoordX[i],CoordY[i]),(0,255,0),10)    
            if F == True:
                cv2.line(frame,(CoordX[len(CoordX)-1],CoordY[len(CoordY)-1]),(CoordX[0],CoordY[0]),(0,255,0),10)
                print("FLAG TRUE")
                

        if not ret:
            print("Error: Unable to capture frame.")
            break
        #frame =cv2.circle(frame, (250, 230), 100, (255, 0, 0), 10)  # Draw a blue circle at the clicked location

        # Display the resulting frame
        cv2.imshow('Webcam', frame)

        
        


    # Release the camera and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()


def Perimeter(DisX,DisY):
    """
    Calculate the perimeter after shape has ended being made

    Parameters:
    - DisX: list of x-coordinates
    - DisY: list of y-coordinates

    returns print of total perimeter
    """
   
    disTot=0
    print()
    for i in range(len(DisX)-1):
        dis=float(math.sqrt(((DisX[i+1]-DisX[i])**2)+((DisY[i+1]-DisY[i])**2)))
        disTot+=dis
        distance.append(dis)
            
        
    print("Distance per segment:")
    for i in range(len(distance)):
        print(f"P{i}-P{i+1}: {distance[i]}")    
    
    print()
    print(f"Perimetro: {disTot} \t")
    
    Ordering(distance)

def Ordering(distance):
    """
    sorts the distance list in increasing order of all line segments

    parameters: 
    all line lenghts

    outputs:
    line lenghts in increasing order
    """
    
    print()
    Increasing=sorted(distance)
    print("Increasing order:")
    for i in range(len(Increasing)):
        for j in range(len(distance)):
            if Increasing[i]==distance[j]:
                print(f"P{j}-P{j+1}: {Increasing[i]}")
    distance.clear()
    Increasing.clear()


# Parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--Z", type=float, default=56, help="Distance Z (default: 56)")
    parser.add_argument("--cal_file", type=str, default="calibration_data.json", 
                        help="Path to the calibration file (default: calibration_data.json)")
    return parser.parse_args()



if __name__ == "__main__":
     

    
    open_webcam()

    # Parse command-line arguments
    args = parse_arguments()

    # Load calibration info from calibration_data.json
    focal_length, cx, cy = load_calibration_info(args.cal_file)

    # Fill calibration_info dictionary
    calibration_info = {
        "f": focal_length,
        "cx": cx,
        "cy": cy,
        "Z": args.Z
    }

    # Print the filled calibration_info dictionary
    print(calibration_info)
