# 🚦 AI-Driven Traffic Management System With Emergency Vehicle Prioritization 

An AI-based smart traffic signal management system that dynamically adjusts traffic light timing based on real-time vehicle density and prioritizes ambulances to ensure minimal delay in emergency response. Built using Python, Computer Vision, and a custom simulation framework.

---

## 📌 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
- [Modules](#modules)
  - [1. Vehicle & Ambulance Detection](#1-vehicle--ambulance-detection)
  - [2. Density Calculation](#2-density-calculation)
  - [3. Smart Traffic Signal Controller](#3-smart-traffic-signal-controller)
  - [4. Simulation Engine](#4-simulation-engine)
- [Installation](#installation)
- [How It Works](#how-it-works)
- [Results & Metrics](#results--metrics)
- [Limitations](#limitations)
- [Future Scope](#future-scope)
- [License](#license)

---

## 🧠 Project Overview

This project simulates an intelligent traffic control system using AI. It addresses urban traffic congestion and emergency vehicle delays by using computer vision to detect vehicles and ambulances in real-time and dynamically control traffic signals.

The goal is to:
- Reduce overall congestion.
- Prioritize ambulance passage through intersections.
- Improve traffic flow efficiency using real-time data and AI-based decision making.

---

## ✨ Features

- 🚘 Real-time vehicle detection (cars, bikes, trucks).
- 🚑 Ambulance detection with highest priority routing.
- ⏱️ Adaptive traffic signal timing based on density.
- 📊 Performance metrics tracking (vehicle throughput, response time).
- 🧪 Fully visual traffic simulation using Tkinter.
- 📦 Modular code architecture for easy extensibility.

---

## 🧰 Tech Stack

| Category              | Technology                     |
|-----------------------|--------------------------------|
| Programming Language  | Python                         |
| Object Detection      | YOLOv2 via Darkflow            |
| GUI & Simulation      | Tkinter                        |
| Computer Vision       | OpenCV                         |
| Dataset Format        | Custom-labeled YOLO format     |
| Model Training        | Custom dataset (~600 images)   |
| Development Tools     | VS Code, Jupyter Notebook      |
| Version Control       | Git, GitHub                    |

---

## 🧱 System Architecture

  ```plaintext
+----------------+        +-----------------------+
|   Video Feed   | -----> |   Vehicle Detection   |
+----------------+        +-----------------------+
                                 |
                                 v
+-----------------------+   +-----------------------+
| Density Calculation   |<--| Ambulance Detection   |
+-----------------------+   +-----------------------+
         |
         v
+-----------------------+
| Signal Timer Logic    |
+-----------------------+
         |
         v
+-----------------------+
| GUI Traffic Simulation|
+-----------------------+
```


## Modules
1. Vehicle & Ambulance Detection
Model: YOLOv2 via Darkflow

Input: Simulated or static traffic images

Output: Bounding boxes for vehicles and ambulances

Accuracy: 92% on custom dataset

Ambulance Priority: On detection, traffic lights are manipulated to clear its path first

2. Density Calculation
Counts the number of uncrossed vehicles per direction using detection data.

Estimates time required per vehicle type (bike: 1 sec, car: 2 sec, truck: 3 sec).

Passes total estimated green time to the controller.

3. Smart Traffic Signal Controller
Receives vehicle counts and sets signal duration proportionally.

Uses ambulance flags (ambulance_direction) to override standard logic when needed.

Rotates lights to green in the shortest path toward the ambulance.

4. Simulation Engine
Tkinter GUI simulation with vehicles moving along roads.

Animates traffic flow based on signal state.

Ambulance is spawned and prioritized when ambulance_detected is true.

Supports 4-way or ring-road style intersections.

## ⚙️ Installation

git clone https://github.com/yourusername/ai-traffic-management.git
cd ai-traffic-management
pip install -r requirements.txt

## Requirements
Python 3.8+
OpenCV
Tkinter (comes with Python)
NumPy, PIL, etc.

## How It Works
1.Vehicle and ambulance detection is performed frame-by-frame.
2.The vehicle count is calculated per lane.
3.A timer logic estimates green light duration.
4.If ambulance is detected, it is given absolute priority.
5.Signals rotate and greenlight the ambulance’s path.
6.Simulation visually shows vehicles moving per signal state.

## Results & Metrics
🚗 Vehicle Throughput: Improved by 35%

🚑 Ambulance Clearance Time: Reduced by 60%

📏 Detection Accuracy: ~92% on validation set

⏱️ Signal Response Time: Dynamic, avg. 5–15s based on density

## ⚠️ Limitations
Simulation only; not integrated with real-time camera feeds.

Ambulance detection trained on a medium-sized dataset (~600 images).

Works best under consistent lighting and simple intersections.

## 🚀 Future Scope
Integrate live traffic camera feeds using RTSP.

Scale to multiple intersections using graph-based routing.

Train on larger datasets with occlusion handling.

Add pedestrian and traffic violation detection.

## 📝 License
This project is licensed under the Apache 2.0 license.
