def recognition():
    import face_recognition
    import os
    import shutil
    from datetime import datetime

    # Load images of known faces and their names
    known_faces_dir = "Student_faces"
    known_face_encodings = []
    known_face_names = []

    # Create attendance file
    attendance_file = open("attendance.txt", "a")

    for filename in os.listdir(known_faces_dir):
        image = face_recognition.load_image_file(os.path.join(known_faces_dir, filename))
        encoding = face_recognition.face_encodings(image)[0]
        name = os.path.splitext(filename)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(name)

    # Load test images and find faces in each image
    test_images_dir = "Student_collected"
    unknown_faces_dir = "Unknown_faces"

    for filename in os.listdir(test_images_dir):
        test_image_path = os.path.join(test_images_dir, filename)
        test_image = face_recognition.load_image_file(test_image_path)
        face_locations = face_recognition.face_locations(test_image)
        face_encodings = face_recognition.face_encodings(test_image, face_locations)

        # Get date time of the image created
        image_created_time = datetime.fromtimestamp(os.path.getctime(test_image_path))

        # Loop through each face in the test image
        for face_encoding in face_encodings:
            # See if the face is a match for the known faces
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match was found, print student attendance is signed
            if True in matches:
                match_index = matches.index(True)
                name = known_face_names[match_index]
                # Append student names and register time into attendance text file
                attendance_file.write(name + "," + str(image_created_time) + "\n")
                print(f"Attendance signed for {name}")
                os.remove(test_image_path)
            else:
                unknown_image_path = os.path.join(unknown_faces_dir, filename)
                shutil.move(test_image_path, unknown_image_path)
                print(f"Unknown face detected in {filename}. Image moved to {unknown_faces_dir}.")

    attendance_file.close()

