import cv2
import mediapipe as mp 
import random
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

choices = ["rock", "paper", "scissors"]

user_score = 0
computer_score = 0

def get_hand_sign(lm_list):
    fingers = []


    if lm_list[4][0] > lm_list[3][0]:
        fingers.append(1)
    else:
        fingers.append(0)

    finger_tips = [8, 12, 16, 20]
    for tip in finger_tips:
        if lm_list[tip][1] < lm_list[tip - 2][1]:
            fingers.append(1)
        else:
            fingers.append(0)

    if fingers == [0, 0, 0, 0, 0]:
        return "rock"
    elif fingers == [1, 1, 1, 1, 1]:
        return "paper"
    elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
        return "scissors"
    else:
        return "unknown"


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)  

    user_choice = "..."
    computer_choice = "..."
    result = ""  
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm_list = []
            for lm in hand_landmarks.landmark:
                lm_list.append((int(lm.x * w), int(lm.y * h)))

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if lm_list:
                user_choice = get_hand_sign(lm_list)  
                
                if user_choice in choices:
                    computer_choice = random.choice(choices)  

                    if user_choice == computer_choice:
                        result = "Draw!"
                    elif (user_choice == "rock" and computer_choice == "scissors") or \
                        (user_choice == "paper" and computer_choice == "rock") or \
                        (user_choice == "scissors" and computer_choice == "paper"):
                        result = "You Win!"
                        user_score += 1
                    else:
                        result = "Computer Wins!"
                        computer_score += 1

                    cv2.putText(frame, f"You: {user_choice}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                    cv2.putText(frame, f"PC : {computer_choice}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
                    cv2.putText(frame, f"Result: {result}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(frame, f"Your Score: {user_score}", (10, 170), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                    cv2.putText(frame, f"PC Score  : {computer_score}", (10, 210), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)


                    time.sleep(2)

    cv2.imshow("Rock Paper Scissors", frame)

    if cv2.waitKey(1) & 0xFF == 27:  
        break

cap.release()
cv2.destroyAllWindows()
