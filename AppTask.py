import pyautogui
from time import sleep

from TaskBase import TaskBase

class AppTask(TaskBase):
    def __init__(self, app = None):
        if app is None:
            raise ValueError("App is required")
        self.app = app

        super().__init__("AppTask", "Open an app and perform a task")

    def open(self):
        pyautogui.keyDown('command')
        pyautogui.press('space')
        pyautogui.keyUp('command')
        sleep(0.5)
        pyautogui.write('Jellyfin')
        pyautogui.press('return')

    def run(self, video = None, watchtime = 30):
        if video is None:
            raise ValueError("Video is required to be able to run an AppTask")

        pyautogui.click(2864/2, 189/2)

        pyautogui.write(video)
        sleep(2.5)
        pyautogui.click(282/2, 836/2)

        sleep(watchtime)

        pyautogui.keyDown('command')
        pyautogui.press('q')
        pyautogui.keyUp('command')