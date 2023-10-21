# Hand gesture tracking for media control

This repository contains an application capable of controlling media by capturing and interpreting hand gestures.
This is achieved by using opencv and mediapipe libraries.

OpenCV is used to capture the images from the webcam, while mediapipe extracts the position of several points in the hand image.
The proportional distances between these points are later used to identify specific hand gestures, such as the number 1 to 4 and the hangloose sign.

The proportions used in the application are base on my own hand and new ones cannot be easily calculated by the app, this feature is mapped for next steps of implementation.


# Requirements
Make sure you have the following requirements installed in your development environment:

- Python 3.8
- Required libraries can be installed using pip install -r requirements.txt

# Run

To run the app, execute the file `app.py`

# Common problems
Most problems encountered while running this application are related to opencv, such as camera permissions and index. Please be sure that OpenCV is reading your camera correctly.
