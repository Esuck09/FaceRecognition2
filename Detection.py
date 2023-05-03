def mtcnn():
    import cv2
    import torch
    import os
    from facenet_pytorch import MTCNN

    img_names = os.listdir("Student_collected/")
    if len(img_names) == 0:
        count = 0
    else:
        count = int(img_names[len(img_names)-1][:-4])

    # Initialize MTCNN face detector
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    mtcnn = MTCNN(device=device)

    # Open video capture device
    cap = cv2.VideoCapture(0)

    # Initialize variables to store captured bounding area and frame
    bounding_area = None
    captured_frame = None

    # Loop over frames from the video stream
    while True:
        # Read frame from video stream
        ret, frame = cap.read()

        # Detect faces using MTCNN
        boxes, probs = mtcnn.detect(frame)

        # Draw bounding boxes around the detected faces
        if boxes is not None:
            for i, box in enumerate(boxes):
                x1, y1, x2, y2 = box.astype(int)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Show the resulting frame
        cv2.imshow('Video', frame)

        # Check for key press events
        key = cv2.waitKey(1)
        if key == ord('a'):
            count = count + 1
            filename ='./Student_collected/' + str(count) + '.png'

            # Save the bounding area and the current frame
            if boxes is not None:
                bounding_area = boxes[0]
                captured_frame = frame.copy()

            if bounding_area is not None and captured_frame is not None:
                x1, y1, x2, y2 = bounding_area.astype(int)
                bounding_box = captured_frame[y1:y2, x1:x2]
                #
                cv2.imwrite(filename, bounding_box)
                print('Bounding box saved to disk')

        elif key == ord('q'):
            # Quit the program if the 'q' key is pressed
            break

    # Release the video capture device and close all windows
    cap.release()
    cv2.destroyAllWindows()


