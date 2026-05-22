# Navigation Assist for the Visually Impaired

An AI-powered navigation assistance system designed to help visually impaired individuals navigate their environment safely using real-time object detection and audio guidance.

## Overview

This project implements a distributed system for real-time obstacle detection and spatial awareness. It utilizes a Raspberry Pi for mobile video capture and a laptop for high-performance computer vision processing. The system identifies common obstacles (cars, people, stairs, etc.), estimates their distance from the user, and provides verbal instructions on how to avoid them.

## Architecture

The system is divided into two main components:

1.  **Raspberry Pi (Video Capture & Streaming):**
    -   Captured using a Raspberry Pi camera module.
    -   Streams live video over a local network using a Flask-based web server.
    -   Handled by `ProjectCode(RaspberryPi).py`.

2.  **Laptop (Processing & Guidance):**
    -   Receives the video stream from the Raspberry Pi.
    -   Uses **YOLOv8** (You Only Look Once) for real-time object detection.
    -   Estimates distance to detected objects based on their bounding box height and known real-world dimensions.
    -   Provides audio feedback via **pyttsx3** (Text-to-Speech) if an object is in the user's direct path.
    -   Handled by `ProjectCode(Laptop).py`.

## Key Features

-   **Real-time Object Detection:** Identifies cars, buses, people, stairs, potholes, speed bumps, and cell phones.
-   **Distance Estimation:** Calculates approximate distance (in meters) to obstacles using focal length calibration.
-   **Intelligent Path Monitoring:** Only alerts the user to objects within a specific "path zone" (central third of the frame).
-   **Directional Guidance:** Advises the user to "Move slightly to your left" or "right" based on the obstacle's position.
-   **Audio Alerts:** Hands-free interaction through voice notifications.

## Requirements

The project requires Python 3.x and the following libraries:

-   `opencv-python`
-   `ultralytics` (YOLOv8)
-   `pyttsx3`
-   `picamera2` (Raspberry Pi side)
-   `flask`

You can install the dependencies using:

```bash
pip install -r requirements.txt
```

## Usage

1.  **Raspberry Pi Setup:**
    -   Connect the camera.
    -   Run `python ProjectCode(RaspberryPi).py`.
    -   Note the IP address of the Raspberry Pi.

2.  **Laptop Setup:**
    -   Update the `feed_laptopIP` variable in `ProjectCode(Laptop).py` with the Raspberry Pi's IP address.
    -   Run `python ProjectCode(Laptop).py`.
    -   The system will start detecting objects and providing audio guidance.

## Project Structure

-   `ProjectCode(RaspberryPi).py`: Flask server for streaming camera feed.
-   `ProjectCode(Laptop).py`: Main processing script with YOLOv8 and TTS.
-   `requirements.txt`: Python dependencies.
-   `Project PPT.pptx`: Presentation file.
-   `Project Report - 1.pdf`: Detailed project documentation.
-   `Video File.mp4`: Demo video.
