# Energy Consumption Comparison: Web Browser vs Native Jellyfin App.
## Introduction
Energy efficiency is a growing concern all over the world, and as sofware and AI develops in giant steps, it is also a concern in the software development area. As applications become more resource-intensive, understanding the energy consumption of different software configurations is essentail. In this experiment, we compare the energy consumption of streaming a small piece of a movie using the Jellyfin web browser interface versus the Jellyfin native application. By measuring the energy consumption of these two approaches, we aim to identify which method is more energy-efficient and under which circumstances.
This study follows a systematic methodology to ensure unbiased and replicable energy measurements. The results of this experiment will help users and developers make informed decisions about optimizing software for energy efficiency.
## Methodology
### Experimental Setup
To minimize external interference and for easier replicability, we will try that the environment is as controlled as possible by doing the following:
 - Close all unnecessary applications.
 - Disable notifications and background services.
 - Use a wired network connection instead of using Wi-Fi for better consistency.
 - Set a fixed screen brightness and resolution and even turn off the display when the testing starts.
 - Ensure the device where the test is being done to be connected to a power source to avoid battery problems.

### Measurement Approach
We used pyEnergiBridge to measure the energy consumption of the Jellyfin web browser interface and the Jellyfin native application while playing the same movie (Fast & Furious). The measurement process involves the following:

 - Starting the energy measurement: Using EnergiBridgeRunner.start() before launching the playback.
 - Playing the movie for a fixed duration
 - Stopping the measurement: Using EnergiBridgeRunner.stop() after the playback ends.
 - Recording the energy consumption and execution time in a csv file.
   
## Results
### Power Draw on the App
Plot description:
 - X-axis (Time in microseconds).
 - Y-axis (Power in watts): the instantaneous system power consumption.
 - Lines:
    - Green (Mean): the average power across multiple measurements at each time slice.
    - Pink (Min): the lowest power measurement observed.
    - Yellow (Max): the highest power measurement observed.
 - General Shape: there is a pronounced spike in the first ~5s, followed by a downward trend, and eventually settling into a moderately stable range of 5 to 8 watts for the mean line. 
 If we go more in more depth, we can divide the graphs in sections. We can observe that the initial spike to nearly 18W is common at the start of a video playback, as the application does video initialization, buffering, and possibly hardware-acceleration handshakes. The second section between ~5 to ~15 seconds, the mean drops from ~10W to ~6-8W. The difference between min and max indicates short bursts of higher CPU/GPU activity, we could see this section as the settling section. The third section ~15s onward, after the first peak, the power consumption drifts with less dramatic peaks. The mean line is around 6-7W, and the min line dips to around 2-3W at times, suggesting idle or partial idle states when frames are easily decoded, we could see this section as the stable section. 

 ### Power Draw on the Web Browser
 Plot description:
 - Similar Layout: same axes for time (ms) and power (W).
 - Lines: same as the previous plot.
 - General Shape: it also features a high spike initially, followed by a decline, with a somewhat amoother or narrower range than the App after the first few seconds.
 In this graph we can also divide it into different sections. The first section from 0 to ~5s, the peak reaches almost 18W again, consistent buffering or initialization. The second section from ~5-20s, the max line can reach 10-12W, while the min line dips around 3-4W. The mean line stabilizes at around 6-7W, this section could be seen as mid-range fluctuations. The last section from ~20-40+ seconds, there is a mild downward trend, though it stays fairly consistent around 5-7W for the mean, we considered this section as the later playback, since it indicates a general stable load. 
 Difference between the App and the Browser energy consumption: they both have similar behavior but the Browser may have fewer extreme downward dips than the App, this could indicate a steadier baseline overhead. On the other hand, it sometimes exhibits short bursts of activity that keep the max line slightly elevated.

 ### Energy Consumption Distribution (Violin + Box Plot)
 Plot description:
 - X-axis: Two categories, App (green) and Browser (pink).
 - Y-axis: Total energy consumption in Jules (J) over the entire test.
 - Violin Plots: Show the overall distribution (thick areas indicate more frequent values)
 - Box Plots: Show the median line, interquartile range, and possible outliers.

 The App distribution spans from roughly 220J to 340J in the extremes. The box (middle 50% of data) centers around 260-280J, with a median near to 270J. Outliers indicate some runs, where the total energy was lower or higher than the bulk measurement.

 The Browser distribution ranges similarly from ~220 to ~340J, but the distribution appears slightly shifted upward, meaning that the box is a bit higher. The median is around 280J, with the top of the box approximately around 300J. The outliers on both ends suggest variability in the measurement environment or usage pattern.

 Even though both the App and the Browser are quite similar, the Browser's median and upper quartile appear slightly higher, this suggests that the overall energy usage can be marginally greater for the Browser across these tests.

## Implications of the Results
- Start-Up Cost vs. Steady State: Both the App and the Browser show significant spikes in power usage at the beginning of the test. This penalty can be attributed to video buffering, decoding initialization and other overhead tasks.  After a few seconds, power usage declines and settles into a more stable range. This represents normal playback once the buffering is complete and the decoder is running smoothly. The initial burst could be minimized, by optimizing buffering and preloading. If the app or browser could predict how much data was going to be needed for the next few seconds of playback, it might fetch it more efficiently, hence reducing the size or duration of the initial spike. Similarly, if the initial part of the video was delivered at a lower bitrate, just for a few seconds, it could shorten the time spent in high CPU/GPU usage while decoding large frames. Furthermore, making sure that the GPU driver or integrated graphics driver is up to date can help ensure the best hardware decode path is used. Additionally, only initializing components of the player like advanced UI elements, could help the system not to overload the system at once. 
- Total energy perspective: The browser has slightly higher total energy consumption compared to the app. Even if the browser doesn't always hit the extreme peaks, the overall consumption is higher. This suggests the browser might keep certain components active or run at a higher baseline power state. On the other hand, the app might have to do more work upfront, but then idle more efficiently, resulting in a lower median total energy usage. We think that the total energy usage could be minimized by doing the following: with respect to the browser, it could help to use an incognito window for fewer add-ons and to have a minimal environment. For app specific purposes, by reducing data processing once the playback is stable could help minimize the total energy usage. On top of that, modern GPUs can also reduce clock speeds when load is low, so dynamic clocking could be crucial. In addition, scaling down CPU frequency when full power is not needed could also help, even though this is normally done automatically.
- Practical implications: 
    - Battery impact: On laptops, tablets, or phones, every extra joules consumed every few seconds can shorten playback time. If the browser constantly run at a higher energy consumption baseline, the battery will drain quicker over a long playback.
    - Performance tuning: if we are aiming to minimize system power, we need to identify and remover overhead, this could be done by using profiling tools like Intel Power Gadget (Mac/Windows) or powertop (Linux) or by optimizing code, for the app we could ensure efficient video decode libraries, and for the browser we could limit background pages, or unnecessary DOM updates.
    - User experience: the initial spikes can generate heat and noise (due to the fans trying to cool down the device). This could be fixed by making a proper thermal management and by watching the video in lower resolution.

## Limitations
While this study provides valuable insights into the energy consumption differences between the Jellyfin web browser interface and the native application, several limitations must be acknowledged:

- Codec Testing: We tested only one video codec, so our results may not apply to other codecs that use hardware differently. 
- Operating System: We tested exclusively on macOS, and results will likely vary on other operating systems due to differences in power management, hardware optimization, and system architecture.
- Caching: We didn’t account for caching in the native app, which might store more data than the browser and affect power use over time.
- Hardware: We tested on just one device, so the results might be different on others with different CPU, GPU, and power management capabilities.
- Network Influence: Even though we used a wired connection, network conditions such as latency, bandwidth fluctuations, and server response times could still influence energy measurements.
- Duration: We measured energy use for only 40 seconds, so we might have missed longer-term trends like power-saving features or background processes (such as software updates or notifications). These factors can affect energy consumption, but since our experiment was short, their impact over time remains unknown.

Despite these limitations, our study provides a useful baseline for comparing the energy efficiency of Jellyfin’s web and native app streaming experiences. Future work could expand on these findings by testing multiple codecs, operating systems, and hardware configurations and so on. 

## Conclusion
Our study compared the energy consumption of streaming Fast & Furious through the Jellyfin web browser interface and the Jellyfin native app. The results shows that both methods follow a similar power usage pattern, with an initial spike (~18W) followed by stabilization. However, the browser tends to have a slightly higher median energy consumption and fewer extreme dips than the app, indicating a steadier baseline. At the same time, the browser occasionally shows short bursts of activity that keep its peak power levels slightly elevated.

While these findings provide insight into the energy efficiency of both approaches, our study had some limitations. We only tested one video codec, used a single hardware setup, and measured energy consumption over a short period. As a result, the findings may not fully apply to other conditions.

Overall, this experiment serves as a starting point for understanding the impact of energy consumption across different approachesFuture research could explore different codecs, devices, operating systems, and longer playback durations to get a more complete picture of energy efficiency in media streaming applications.
