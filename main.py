import argparse
from time import sleep

from selenium import webdriver

from pyEnergiBridge.api import EnergiBridgeRunner

parser = argparse.ArgumentParser(description='EnergiBridge')
parser.add_argument('-i', '--interval', type=int, help='Interval between measurements', dest='interval', default=100)
parser.add_argument('-o', '--output', type=str, help='Output directory', dest='output', default='results')
parser.add_argument('-b', '--browser', type=str, help='Browser to use', dest='browser', default='chrome')

runner = EnergiBridgeRunner()
if __name__ == '__main__':
    args = parser.parse_args()
    # Preparation work, don't measure yet.
    match args.browser:
        case 'chrome':
            browser = webdriver.Chrome()
        case 'firefox':
            browser = webdriver.Firefox()
        case 'edge':
            browser = webdriver.Edge()
        case 'safari':
            browser = webdriver.Safari()
        case _:
            raise ValueError('Unsupported browser')
    
    browser.get('https://web.archive.org/web/20200215124941/https://www.youtube.com/watch?v=_OBlgSz8sSM')

    runner.start(results_file='results.csv')
    # Do any task we want to measure here
    sleep(60)

    browser.close()
    energy, duration = runner.stop()
    print(f"Energy consumption (J): {energy}; Execution time (s): {duration}")
