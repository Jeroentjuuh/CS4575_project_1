import argparse
from time import sleep

import pandas as pd

from selenium import webdriver

from pyEnergiBridge.api import EnergiBridgeRunner

from BrowserTask import BrowserTask
from AppTask import AppTask

parser = argparse.ArgumentParser(description='EnergiBridge')
parser.add_argument('-o', '--output', type=str, help='Output directory', dest='output', default='results')
parser.add_argument('-t', '--task', type=str, help='Task to perform', dest='task', default='browser', choices=['browser', 'app'])
parser.add_argument('--iterations', type=int, help='Number of iterations', dest='iterations', default=10)
parser.add_argument('--video', type=str, help='Video to test', dest='video', choices=["2 Fast 2 Furious", "Moana 2"])
parser.add_argument('--codec', type=str, help='Codec to test', dest='codec', choices=["h264", "av1"], default='h264')

runner = EnergiBridgeRunner()
if __name__ == '__main__':
    args = parser.parse_args()
    if args.task == 'browser':
        energies = []
        durations = []
        # TESTING FOR BROWSER
        print("Start tests for browser: Chrome")
        for i in range(args.iterations):
            print(f"Iteration {i+1}")
            runner.start(results_file=f"data/{args.codec}_{args.output}_browser_{i+1}.csv")
            browser = webdriver.Chrome()

            browser.maximize_window()
            browser_task = BrowserTask('https://jellyfin.delft.roelofvdg.nl', browser)
            browser_task.open()
            sleep(2)
            
            browser_task.run(video=args.video)

            # Before starting next task, stop measuring and sleep for 10 seconds
            energy, duration = runner.stop()
            energies.append(energy)
            durations.append(duration)
            print(f"Iteration: {i+1}, Energy consumption (J): {energy}; Execution time (s): {duration}")

            sleep(30)

        print(f"Average energy consumption (J): {sum(energies)/len(energies)}; Average execution time (s): {sum(durations)/len(durations)}")
        res = pd.DataFrame([energies, durations])
        res.to_csv(f"data/{args.codec}_{args.output}_browser_summary.csv", index=False)

    if args.task == 'app':
        energies = []
        durations = []
        print("Start tests for App version")
        for i in range(args.iterations):
            runner.start(results_file=f"data/{args.codec}_{args.output}_app_{i+1}.csv")
            app_task = AppTask('Jellyfin')
            app_task.open()
            sleep(2)
            
            app_task.run(video=args.video)

            energy, duration = runner.stop()
            energies.append(energy)
            durations.append(duration)

            print(f"Iteration: {i+1}, Energy consumption (J): {energy}; Execution time (s): {duration}")
            sleep(30)
        
        print(f"Average energy consumption (J): {sum(energies)/len(energies)}; Average execution time (s): {sum(durations)/len(durations)}")
        res = pd.DataFrame([energies, durations])
        res.to_csv(f"data/{args.codec}_{args.output}_app_summary.csv", index=False)


    
