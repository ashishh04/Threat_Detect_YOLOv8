# 🚨 ThreatDetect - Real-Time Threat Detection System

ThreatDetect is a real-time, GPU-accelerated object detection system using a custom-trained YOLOv8 model. It identifies potential threats such as persons, guns, knives, drones, and vehicles via webcam, logs events to a MySQL database, saves evidence snapshots, and sends instant alerts via WhatsApp and Email.

---

## ✅ Features

* 🎯 Real-time object detection with YOLOv8 (trained on 5 classes)
* ⚡ GPU-accelerated with RTX 3050 Ti
* 🖼️ Snapshot capture on detection
* 📃 Logs all detections to MySQL database
* 📩 Sends email alerts via SendGrid
* 💬 Sends WhatsApp alerts via Twilio sandbox
* 📊 Streamlit dashboard to review detections

---

## ⚒️ Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 📂 Folder Structure

```
ThreatDetect/
├── yolo_alerts_combined.py       # Core detection and alert script
├── config.py                     # API keys and email credentials (not tracked)
├── requirements.txt              # Dependencies
├── detections/                   # Saved threat images
├── dataset/                      # Training data and data.yaml
├── runs/detect/train2/best.pt    # Trained YOLOv8 model
├── dashboard/
│   └── dashboard.py              # Streamlit UI for detection logs
└── README.md                     # This file
```

---

## 🔐 config.py Format

Create a file named config.py in the root directory:

```python
# Twilio
TWILIO_SID = "ACXXXXXXXXXXXXXXXXXXXXXXXXXXX"
TWILIO_TOKEN = "your_twilio_auth_token"
TWILIO_FROM = "whatsapp:+14155238886"
TWILIO_TO = "whatsapp:+91xxxxxxxxxx"

# SendGrid
SENDGRID_API_KEY = "your_sendgrid_api_key"
EMAIL_FROM = "your_verified_sender@example.com"
EMAIL_TO = "your_email@example.com"
```

---

## 🚀 Run Detection System

Start real-time detection and alerting:

```bash
python yolo_alerts_combined.py
```

Quit with:

```bash
q
```

---

## 📊 View Dashboard

Launch the Streamlit dashboard:

```bash
streamlit run dashboard/dashboard.py
```

---

## 🧪 Testing

* Lower CONF\_THRESHOLD in the script if detections are missed.
* Use webcam or test images to simulate threats.
* Check MySQL threat\_log table for detection history.

---

## 🧠 Model Info

* Trained on 30k+ images for 5 classes
* Model path: runs/detect/train2/weights/best.pt
* mAP: >0.85 on average

---

## 📦 Deployment

### Option 1: Run from Source

```bash
pip install -r requirements.txt
python yolo_alerts_combined.py
```

### Option 2: Batch Launcher (Windows)

Create a file named `run.bat` with:

```bat
@echo off
python yolo_alerts_combined.py
pause
```

### Option 3: Build Executable (Optional)

```bash
pip install pyinstaller
pyinstaller --onefile yolo_alerts_combined.py
```

Find the .exe in the `dist/` folder.

### Option 4: GitHub Hosting

Upload the project (excluding credentials) to a GitHub repository:

```
.gitignore:
config.py
__pycache__/
detections/
runs/
```

Add project description, screenshots, and tags.

---

## 🙌 Credits

Developed by: A Ashish
Powered by: YOLOv8, Twilio, SendGrid, Streamlit, MySQL
