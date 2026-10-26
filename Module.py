import cv2
import mediapipe as mp
import winsound
from plyer import notification


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)


gesture1_open = False
gesture1_count = 0
gesture2_count = 0
gesture3_count = 0


def alert_user(message):
    print(message)
    winsound.Beep(1000, 500)
    notification.notify(
        title="ALERT",
        message=message,
        timeout=3
    )

while True:
    ret, img = cap.read()
    if not ret:
        break
    img = cv2.flip(img, 1)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lm = handLms.landmark


            tips = [4, 8, 12, 16, 20]

            h, w, _ = img.shape
            lmPos = []
            for id, lmC in enumerate(lm):
                lmPos.append((int(lmC.x * w), int(lmC.y * h)))

            fingers = []


            if lmPos[tips[0]][0] < lmPos[tips[0]-1][0]:  
                fingers.append(1)
            else:
                fingers.append(0)


            for id in range(1, 5):
                if lmPos[tips[id]][1] < lmPos[tips[id]-2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)


            if fingers == [0,1,1,1,1]:  
                gesture1_open = True
            elif fingers == [0,0,0,0,0] and gesture1_open:
                gesture1_count += 1
                gesture1_open = False
                if gesture1_count >= 3:
                    alert_user("HELP Signal Detected (Gesture 1)")
                    gesture1_count = 0 


            if fingers == [1,0,0,0,1]:
                gesture2_count += 1
                if gesture2_count >= 2:
                    alert_user("Someone is in Danger (Gesture 2)")
                    gesture2_count = 0
            else:
                gesture2_count = 0


            if fingers == [0,1,1,0,0]:
                gesture3_count += 1
                if gesture3_count >= 2:
                    alert_user("HOSTAGE Signal, Suspect is Armed (Gesture 3)")
                    gesture3_count = 0
            else:
                gesture3_count = 0

            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Hand Gesture Detection", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
