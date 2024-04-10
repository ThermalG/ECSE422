# Network Designer: A good try with an NP problem in graph theory
**! ONLY FOR GRADING REFERENCE. WON'T BE UPDATED IN THIS REPOSITORY.**
The program is a collabrative project of ECSE 422 Fault Tolerant Computing, with [Zhanyue](https://github.com/ZhanyueZ) and [Fengqi](https://github.com/fengqiz)

## How to use:
1. Clone repository;
2. Modify `path` attribute in NetworkDesigner.py (individual tester file);
3. Install dependencies. You can achieve such by running the command below;
    ```
    pip install -r requirements.txt
    ```
4. Input the cost limit;
5. The runtime comparison should be printed and the network designs for each version including cost and 
   maximum reliability should be plotted.

NOTE though optimized, attempting a tester with large number of cities (8_1.txt for instance) or specifying 
a huge cost can lead the simple algorithm to run for an unacceptably long period, indicated by a progress 
bar on terminal. You may as well comment out step 4 in main() under such scenario.
