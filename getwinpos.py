import pyautogui
import time

while(1) :
    x, y = pyautogui.position()
    print(f"> {x}, {y}")