# SmartAssist Vision: AI-Powered Mobility Aid
![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?logo=opencv)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-4-red?logo=raspberrypi)
![MobileNetSSD](https://img.shields.io/badge/MobileNet--SSD-Object%20Detection-orange)
![IoT](https://img.shields.io/badge/IoT-Smart%20Systems-blueviolet)
![Edge AI](https://img.shields.io/badge/Edge-AI-success)
![Accessibility](https://img.shields.io/badge/Accessibility-Assistive%20Technology-brightgreen)
![Computer Vision](https://img.shields.io/badge/Computer-Vision-yellowgreen)
![Status](https://img.shields.io/badge/Status-Completed-success)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi-black)
![Language](https://img.shields.io/badge/Language-Python-blue)
![Deployment](https://img.shields.io/badge/Deployment-Offline%20AI-success)
![Project](https://img.shields.io/badge/Final%20Year-Project-orange)
## AI-Powered Mobility Aid for the Visually Impaired

SmartAssist Vision is a wearable assistive technology designed to enhance independent mobility for visually impaired individuals through real-time object detection, obstacle awareness, and voice-guided navigation.

The system combines Computer Vision, Edge AI, Distance Sensing, and Speech Feedback to provide situational awareness without requiring internet connectivity.

---

## Project Overview

Traditional mobility aids provide limited information about surrounding objects and obstacles.

SmartAssist Vision addresses this challenge by:

* Detecting objects in real time using MobileNet-SSD
* Identifying object position (Left, Center, Right)
* Measuring obstacle distance using an HC-SR04 ultrasonic sensor
* Providing voice instructions through earphones
* Running entirely on a Raspberry Pi 4

---

## Key Features

* Real-Time Object Detection
* Voice-Guided Navigation
* Obstacle Alert System
* Distance Measurement
* Offline Edge AI Processing
* Portable Wearable Design
* Low-Cost Implementation

---

## Technology Stack

### Hardware

* Raspberry Pi 4
* USB Camera
* HC-SR04 Ultrasonic Sensor
* Earphones / Headphones
* Power Bank
* Wearable Helmet Mount

### Software

* Python
* OpenCV
* MobileNet-SSD
* NumPy
* RPi.GPIO
* eSpeak
* Raspberry Pi OS

---

## System Workflow

1. Camera captures surroundings
2. MobileNet-SSD detects nearby objects
3. Position logic identifies object location
4. Ultrasonic sensor measures obstacle distance
5. Raspberry Pi processes sensor data
6. Voice feedback is delivered through earphones

---

## Development Phases

### Phase 1 – Laptop Development & Testing

* Camera Validation
* MobileNet-SSD Testing
* Object Position Detection
* Voice Output Testing

### Phase 2 – Raspberry Pi Deployment

* Raspberry Pi Integration
* Ultrasonic Sensor Integration
* Distance Classification
* Voice Feedback System
* Complete Wearable Deployment

---

## Example Voice Outputs

* Person on the left
* Chair in center
* Bottle on the right
* Caution table very close

---

## Project Architecture

Camera → MobileNet-SSD → Object Detection

HC-SR04 → Distance Measurement

Raspberry Pi → Data Fusion

eSpeak → Voice Guidance

---

## Applications

* Assistive Technology
* Smart Mobility Systems
* Wearable AI Devices
* Edge AI Solutions
* Accessibility Research

---

## Future Enhancements

* GPS Navigation Assistance
* Emergency SOS Feature
* Face Recognition
* AI Scene Understanding
* Mobile Application Integration
* Coral TPU Acceleration

---

## Author

**Fardin Imran Shaikh**

---

## License

This project is intended for educational and research purposes.
