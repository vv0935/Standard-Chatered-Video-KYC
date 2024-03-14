import cv2
import face_recognition

# Load images and encode face features
owner_image = face_recognition.load_image_file(r"ai.jpg")
other_image = face_recognition.load_image_file(r"sai2.jpg")
owner_encoding = face_recognition.face_encodings(owner_image)[0]
other_encoding = face_recognition.face_encodings(other_image)[0]


known_face_encodings = [owner_encoding]
known_face_names = ["sai"]  # Replace with your name
# Initialize video capture
cap = cv2.VideoCapture(0)  # 0 for default camera, change it if you have multiple cameras

while True:
    ret, frame = cap.read()

    if not ret:  # Check if frame is properly read
        print("Error: Frame not captured")
        break

    # Find all face locations and encodings in the frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Compare face encoding with known face encodings
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "doesn't match"
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        # Draw rectangle and label on the frame
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
        print("owner detected")
        cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
