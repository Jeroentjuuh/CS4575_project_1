import pyautogui
from time import sleep

from TaskBase import TaskBase

class AppTask(TaskBase):
    def __init__(self, app = None):
        if app is None:
            raise ValueError("App is required")
        self.app = app

        super().__init__("AppTask", "Open an app and perform a task")

    def run(self, video = None, watchtime = 30):
        if video is None:
            raise ValueError("Video is required to be able to run an AppTask")
        
        pyautogui.keyDown('command')
        pyautogui.press('space')
        pyautogui.keyUp('command')
        sleep(0.5)
        pyautogui.write('Jellyfin')
        pyautogui.press('return')

        sleep(5)

        screenWidth, screenHeight = pyautogui.size()
        currentMouseX, currentMouseY = pyautogui.position()
        x, y = pyautogui.locateCenterOnScreen('searchIcon.png', confidence=0.9, grayscale=True)
        print(screenWidth, screenHeight)
        print(currentMouseX, currentMouseY)
        print(x, y)
        pyautogui.click(x/2, y/2)

        pyautogui.write('2 fast 2 furious')
        loaded = False
        while loaded is False:
            try:
                x, y = pyautogui.locateCenterOnScreen('2Fast2Furious.png', confidence=0.9, grayscale=True)
                loaded = True
            except:
                sleep(1)
        pyautogui.click(x/2, y/2)

        sleep(watchtime)

        pyautogui.keyDown('command')
        pyautogui.press('q')
        pyautogui.keyUp('command')