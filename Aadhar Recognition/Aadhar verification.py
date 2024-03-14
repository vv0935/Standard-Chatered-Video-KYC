#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install pytesseract


# In[5]:


import cv2
import numpy as np
import pytesseract

# Function to extract Aadhaar number using EAST text detection
def extract_aadhaar_number(image):
    # Load the pre-trained EAST text detection model
    model_path = 'frozen_east_text_detection.pb'
    net = cv2.dnn.readNet(model_path)

    # Resize the image to a fixed width and height
    new_width, new_height = 320, 320
    resized_image = cv2.resize(image, (new_width, new_height))

    # Normalize the image and prepare it for input to the model
    blob = cv2.dnn.blobFromImage(resized_image, 1.0, (new_width, new_height), (123.68, 116.78, 103.94), True, False)
    net.setInput(blob)

    # Forward pass through the network to perform text detection
    output_layer_names = ["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"]
    (scores, geometry) = net.forward(output_layer_names)

    # Decode the predictions
    rectangles, confidences = [], []
    for i in range(scores.shape[2]):
        # Extract the confidence (probability) associated with the prediction
        confidence = scores[0, 0, i, 0]

        # Filter out weak predictions by ensuring the confidence is greater than the minimum confidence
        if confidence > 0.5:
            # Extract the coordinates of the bounding box for the text region
            x1, y1, x2, y2 = geometry[0, 0, i, 3:7] * np.array([image.shape[1], image.shape[0], image.shape[1], image.shape[0]])

            # Append the bounding box coordinates and confidence to the lists
            rectangles.append((x1, y1, x2, y2))
            confidences.append(float(confidence))

    # Apply non-maxima suppression to remove overlapping bounding boxes
    indices = cv2.dnn.NMSBoxes(rectangles, confidences, 0.5, 0.4)

    # Loop over the indices
    detected_text = ''
    for i in indices:
        i = i[0]
        # Extract the bounding box coordinates
        (x1, y1, x2, y2) = rectangles[i]

        # Extract the region of interest (ROI) containing the text
        roi = image[int(y1):int(y2), int(x1):int(x2)]

        # Perform OCR (text recognition) on the ROI using pytesseract
        text = pytesseract.image_to_string(roi, config='--psm 6')

        # Append the detected text to the result
        detected_text += text.strip()

    # Filter out non-numeric characters
    aadhaar_number = ''.join(filter(str.isdigit, detected_text))

    return aadhaar_number

# Function to start Aadhaar verification
def start_verification():
    # Prompt the user to enter Aadhaar number
    user_aadhaar_number = input("Enter your Aadhaar number: ")

    # Initialize video capture
    cap = cv2.VideoCapture(0)  # 0 for default camera, change it if you have multiple cameras

    while True:
        ret, frame = cap.read()

        if not ret:  # Check if frame is properly read
            print("Error: Frame not captured")
            break

        cv2.imshow("Frame", frame)

        # Wait for user to press 'c' to capture image
        if cv2.waitKey(1) & 0xFF == ord('c'):
            # Save the captured image to a file
            cv2.imwrite("captured_image.jpg", frame)
            break

    cap.release()
    cv2.destroyAllWindows()

    # Load the captured image
    captured_image = cv2.imread("captured_image.jpg")

    # Extract Aadhaar number from the captured image
    detected_aadhaar_number = extract_aadhaar_number(captured_image)

    # Compare the detected Aadhaar number with the user-entered Aadhaar number
    if detected_aadhaar_number == user_aadhaar_number:
        print("Aadhaar number verified successfully!")
    else:
        print("Aadhaar number verification failed!")

# Start Aadhaar verification process
start_verification()


# In[ ]:




