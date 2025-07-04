import cv2
import time
import os
import mysql.connector
from ultralytics import YOLO
from twilio.rest import Client as TwilioClient
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import traceback

# ---------------------- MODEL & PATH SETUP ----------------------

model = YOLO("runs/detect/train2/weights/best.pt")
cap = cv2.VideoCapture(0)
os.makedirs("detections", exist_ok=True)

THREAT_CLASSES = ["person", "gun", "knife", "drone", "vehicle"]
CONF_THRESHOLD = 0.5

# ---------------------- MYSQL CONNECTION ----------------------

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="object_detection"
)
cursor = db.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS threat_log (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME,
        object_type VARCHAR(50),
        confidence FLOAT,
        image_path VARCHAR(255)
    )
""")

# ---------------------- TWILIO WHATSAPP ----------------------

TWILIO_SID = "ACXXXXXXXXXXXXXXXXXXXXXXXXXXX"
TWILIO_TOKEN = "your_twilio_auth_token"
TWILIO_FROM = "whatsapp:+14155238886"
TWILIO_TO = "whatsapp:+91xxxxxxxxxx"

twilio_client = TwilioClient(twilio_sid, twilio_token)

# ---------------------- SENDGRID EMAIL ----------------------

SENDGRID_API_KEY = "your_sendgrid_api_key"
EMAIL_FROM = "your_verified_sender@example.com"
EMAIL_TO = "your_email@example.com"


# ---------------------- ALERT FUNCTIONS ----------------------

def log_event(obj_type, conf, image_path):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    sql = "INSERT INTO threat_log (timestamp, object_type, confidence, image_path) VALUES (%s, %s, %s, %s)"
    values = (timestamp, obj_type, conf, image_path)
    cursor.execute(sql, values)
    db.commit()

def send_whatsapp_alert(message_text):
    try:
        message = twilio_client.messages.create(
            from_=twilio_from,
            to=twilio_to,
            body=message_text
        )
        print(f"[WHATSAPP SENT] SID: {message.sid}")
    except Exception as e:
        print(f"[WHATSAPP ERROR] {e}")

def send_email_alert(subject, body_text):
    try:
        message = Mail(
            from_email=EMAIL_FROM,
            to_emails=EMAIL_TO,
            subject=subject,
            plain_text_content=body_text
        )
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"[EMAIL SENT] Status: {response.status_code}")
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
        traceback.print_exc()

def process_frame(frame):
    results = model.predict(frame, conf=CONF_THRESHOLD)
    boxes = results[0].boxes
    threats_detected = []
    for box in boxes:
        cls_id = int(box.cls)
        cls_name = model.names[cls_id]
        conf = float(box.conf)
        if cls_name in THREAT_CLASSES:
            threats_detected.append((cls_name, conf, box.xyxy[0].cpu().numpy()))
    return threats_detected, results[0].plot()

# ---------------------- MAIN LOOP ----------------------

while True:
    ret, frame = cap.read()
    if not ret:
        break

    threats, annotated_frame = process_frame(frame)

    if threats:
        timestamp = int(time.time())
        image_path = f"detections/threat_{timestamp}.jpg"
        cv2.imwrite(image_path, frame)

        alert_classes = []
        for obj_type, conf, _ in threats:
            log_event(obj_type, conf, image_path)
            alert_classes.append(f"{obj_type} ({conf:.2f})")

        # Alert text
        alert_msg = f"🚨 Alert: {', '.join(alert_classes)} detected at {time.ctime(timestamp)}"

        # Send alerts
        send_whatsapp_alert(alert_msg)
        send_email_alert("🚨 Threat Detected", alert_msg)

        print(f"[ALERT] {alert_msg}")

    cv2.imshow("output.jpg", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ---------------------- CLEANUP ----------------------

cap.release()
cv2.destroyAllWindows()
cursor.close()
db.close()
