# Network Designer: A good try with an NP problem in graph theory
This program is a collabrative project of ECSE 422 Fault Tolerant Computing, with [Zhanyue](https://github.com/ZhanyueZ) and [Fengqi](https://github.com/fengqiz)

## How to use:
1. Modify `path` attribute in NetworkDesigner.py (individual tester file);
2. Install dependencies. You can achieve such by running the command below;
    ```
    pip install -r requirements.txt
    ```
3. Input the cost limit;
4. The runtime comparison should be printed and the network designs for each version including cost and 
   maximum reliability should be plotted.

NOTE though optimized, attempting a tester with large number of cities (8_1.txt for instance) or specifying 
a huge cost can lead the simple algorithm to run for an unacceptably long period, indicated by a progress 
bar on terminal. You may as well comment out step 4 in main() under such scenario.