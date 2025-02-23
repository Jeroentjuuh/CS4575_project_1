import argparse
from time import sleep

import pyautogui

from selenium import webdriver

from pyEnergiBridge.api import EnergiBridgeRunner

from BrowserTask import BrowserTask
from AppTask import AppTask

parser = argparse.ArgumentParser(description='EnergiBridge')
parser.add_argument('-i', '--interval', type=int, help='Interval between measurements', dest='interval', default=100)
parser.add_argument('-o', '--output', type=str, help='Output directory', dest='output', default='results')
parser.add_argument('-b', '--browser', type=str, help='Browser to use', dest='browser', default='chrome')

runner = EnergiBridgeRunner()
if __name__ == '__main__':
    runner.start(results_file='results.csv')
    # args = parser.parse_args()
    # # Preparation work, don't measure yet.
    # match args.browser:
    #     case 'chrome':
    #         browser = webdriver.Chrome()
    #     case 'firefox':
    #         browser = webdriver.Firefox()
    #     case 'edge':
    #         browser = webdriver.Edge()
    #     case 'safari':
    #         browser = webdriver.Safari()
    #     case _:
    #         raise ValueError('Unsupported browser')
    # browser.maximize_window()
    
    # browser_task = BrowserTask('https://jellyfin.delft.roelofvdg.nl', browser)
    # browser_task.run(video='2 Fast 2 Furious')

    app_task = AppTask('Jellyfin')
    app_task.run(video='2 Fast 2 Furious')

    energy, duration = runner.stop()
    print(f"Energy consumption (J): {energy}; Execution time (s): {duration}")
