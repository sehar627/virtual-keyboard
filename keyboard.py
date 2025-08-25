import mediapipe as mp
import pyautogui
import math
import cv2

capture=cv2.VideoCapture(0)
width  = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)) 
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)) 



mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hand=mp_hands.Hands(max_num_hands=1)

tipIds = [4, 8, 12, 16, 20]

#on_screen keyboard
keys = [["Q","W","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L"],
        ["Z","X","C","V","B","N","M"," "]]  

key_size = 50  
pinch=None

def draw_keyboard(frame):
    y = 20
    for row in keys:  
        x= 20
        for key in row:
            cv2.rectangle(frame, (x, y), (x+key_size, y+key_size), (255,0,0), 2)
            cv2.putText(frame, key, (x+15, y+40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
            x += key_size + 10
        y+= key_size + 10


def get_key_pressed(key_x, key_y):
    y= 20
    for row in keys:
        x=20
        for key in row:
            if x < key_x < x+key_size and y < key_y < y+key_size:
                return key
            x += key_size + 10
        y += key_size + 10
    return None


def process_hand(image, hand_landmarks):

    global pinch
   
    if hand_landmarks:
        landmarks = hand_landmarks[0].landmark

        # index finger tip and thumb tip
        finger_tip_x = int((landmarks[8].x)*width)
        finger_tip_y = int((landmarks[8].y)*height)

        thumb_tip_x = int((landmarks[4].x)*width)
        thumb_tip_y = int((landmarks[4].y)*height)

        # Draw pointer
        cv2.circle(image, (finger_tip_x, finger_tip_y), 8, (0,255,0), -1)

        distance = ((finger_tip_x - thumb_tip_x)**2 + (finger_tip_y - thumb_tip_y)**2) ** 0.5

        key_pressed=get_key_pressed(finger_tip_x,finger_tip_y)
        print(key_pressed)


        if distance < 20 and key_pressed:
            if not pinch:  
                pinch = True
                if key_pressed == " ":
                    pyautogui.press("space")
                else:
                    pyautogui.press(key_pressed.lower())
        else:
            pinch = False  
  

while True:
    
        ret,frame=capture.read()
        frame= cv2.flip(frame,1)

        rgb_frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result= hand.process(rgb_frame)
        hand_landmarks=result.multi_hand_landmarks

        if hand_landmarks:
                for landmarks in hand_landmarks:
                    mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)
                        
        draw_keyboard(frame)
        process_hand(frame,hand_landmarks)
        cv2.imshow("On-Screen Keyboard", frame)
        if cv2.waitKey(1) & 0XFF==ord('q'):
                break
capture.release()
cv2.destroyAllWindows()         