# Driver Health Monitoring System
# Project Overview
The Driver Health Monitoring System is designed to detect driver fatigue, monitor head posture, and sense drowsiness by analyzing face landmarks using Google MediaPipe. Additionally, the system integrates external sensors like MQ-3 (alcohol detection), LM35 (temperature sensor), and a heart rate sensor to monitor various aspects of the driver's health and environment. This project was developed using a Raspberry Pi for processing and sensor interfacing.

# Features
Drowsiness detection using eye closure rate analysis.
Yawn detection by monitoring mouth openness using MediaPipe Face Mesh.
Head posture detection to identify if the driver’s head is in a risky position (e.g., looking away from the road).
Alcohol detection using the MQ-3 sensor.
Body temperature monitoring using the LM-35 temperature sensor.
Heart rate monitoring using a heart rate sensor to detect abnormal heart conditions.
# Components Used
* Raspberry Pi (any model with GPIO support, such as Raspberry Pi 4)
* Google MediaPipe for real-time face mesh detection.
* MQ-3 Gas Sensor for alcohol detection.
* LM-35 Temperature Sensor for body temperature monitoring.
* Heart Rate Sensor for measuring pulse.
* Camera for capturing the driver’s face and running MediaPipe.
# System Workflow
1) Face Detection & Landmark Recognition: The camera captures the driver's face in real-time, and MediaPipe Face Mesh detects face landmarks, focusing on key regions such as the eyes, mouth, and head. This allows the system to determine drowsiness (eye closure), yawning (mouth opening), and head posture (deviation from the forward-looking position).

2) Alcohol Detection: The MQ-3 gas sensor continuously monitors the air for alcohol content. If the sensor detects alcohol above a certain threshold, a warning is triggered.

3) Temperature Monitoring: The LM-35 sensor measures the driver's body temperature, alerting the system if it rises beyond a healthy threshold.

4) Heart Rate Monitoring: The heart rate sensor tracks the driver’s pulse, and abnormal rates (either too high or too low) trigger a warning.

5) Alert Mechanism: If any of the health parameters exceed predefined limits, the system generates an alert (visual, auditory, or via connected systems) to ensure the driver's safety.

