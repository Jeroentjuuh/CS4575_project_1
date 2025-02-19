import time
from pyEnergiBridge.api import EnergiBridgeRunner

runner = EnergiBridgeRunner()

if __name__ == "__main__":
	runner.start(results_file="results.csv")
	time.sleep(3)

	joules, duration = runner.stop()
	
	print("Joules, duration", (joules, duration))
