import cv2
from cvzone.HandTrackingModule import HandDetector
import math

# Start camera
cap = cv2.VideoCapture(0)

# Hand detector
detector = HandDetector(maxHands=1, detectionCon=0.7)

# Fullscreen window
cv2.namedWindow("Angle Finder", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Angle Finder", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

def get_angle(p1, p2):
    dx = p2[0] - p1[0]
    dy = p1[1] - p2[1]
    return int(math.degrees(math.atan2(dy, dx)))

while True:
    success, img = cap.read()
    if not success:
        print("Camera failed")
        break

    # NO LEFT/RIGHT LABEL → flipType=False
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        hand = hands[0]

        # Extract only (x, y) from (x, y, z)
        p1 = hand['lmList'][0][:2]   # Wrist
        p2 = hand['lmList'][8][:2]   # Index finger tip

        # Draw line
        cv2.line(img, p1, p2, (255, 255, 255), 4)

        # Calculate angle
        angle = get_angle(p1, p2)

        # Show angle
        cv2.putText(img, f"Angle: {angle}°",
                    (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (0, 255, 0), 4)

    cv2.imshow("Angle Finder", img)

    # ENTER key to exit
    if cv2.waitKey(1) == 13:
        break

cap.release()
cv2.destroyAllWindows()
