import cv2
import os

# Open camera
cap = cv2.VideoCapture(0)
cv2.waitKey(1000)

# Open folder for student image
known_faces_dir = "Student_faces"

# Press 'c' to capture image
while True:
    ret, frame = cap.read()
    cv2.imshow('Register', frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        break

# Get student ID
studID = input('Enter student ID: ')

# Save the image
file_path = os.path.join(known_faces_dir, studID + '.jpg')
cv2.imwrite(file_path, frame)

# Release the camera
cap.release()

# Show the captured image
cv2.imshow('Captured Image', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()