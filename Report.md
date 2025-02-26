# Energy Consumption Comparison: Web Browser vs Native Jellyfin App.
## Introduction
Energy efficiency is a growing concern all over the world, and as sofware and AI develops in giant steps, it is also a concern in the software development area. As applications become more resource-intensive, understanding the energy consumption of different software configurations is essentail. In this experiment, we compare the energy consumption of streaming a small piece of a movie using the Jellyfin web browser interface versus the Jellyfin native application. By measuring the energy consumption of these two approaches, we aim to identify which method is more energy-efficient and under which circumstances.
This study follows a systematic methodology to ensure unbiased and replicable energy measurements. The results of this experiment will help users and developers make informed decisions about optimizing software for energy efficiency.
## Methodology
### Experimental Setup
To minimize external interference and for easier replicability, we will try that the environment is as controlled as possible by doing the following:
 - Close all unnecessary applications.
 - Disable notifications and background services.
 - The experiment should have been done with a wired connection in order to obtain the best results, but this was not possible since at the time where the experiment was tested the only available connection was a 4G connection from the phone of one of the members of the group.
 - Set a fixed screen brightness and resolution and even turn off the display when the testing starts.
 - Ensure the device where the test is being done to be connected to a power source to avoid battery problems.

### Measurement Approach
We used pyEnergiBridge to measure the energy consumption of the Jellyfin web browser interface and the Jellyfin native application while playing the same movie (Fast & Furious). The measurement process involves the following:

 - Starting the energy measurement: Using EnergiBridgeRunner.start() before launching the playback.
 - Playing the movie for a fixed duration
 - Stopping the measurement: Using EnergiBridgeRunner.stop() after the playback ends.
 - Recording the energy consumption and execution time in a csv file.


