# Calibration README

---

## Overview

This Python project consists of multiple files that need to be executed in a specific order to achieve the desired functionality. Each file serves a distinct purpose and contributes to the overall functionality of the project.

## Contents

1. **Source Code Files**:
   - `run.py`: Reads in the serial data and uses a calibration profile to output distance.
   - `gen_deviation_graph.py`: Generates a deviation graph from the line of best fit.
   - `gen_stats.py`: Generates the line of best fit as well as the standard and absolute maximum deviation values.
   - `gen_calibration_graph.py`: Generates a graph with the calibration values and the line of best fit if there is one in the calibration file.
   - `clean_data.py`: Cleans the data in a calibration profile by specifying the endpoints in which the calibration values are valid.
   - `update_config.py`: Adds calibration points to the config for a given distance measurement.
   - `data_in.py`: Gets the raw data coming in from the microcontroller through serial.
   - `gen_config.py`: Generates a base JSON configuration file.

2. **Documentation**:
   - `README.md`: This file, providing an overview and instructions.

## Setup Instructions

To set up and run the project, follow these steps:

**Install Dependencies**: If the project requires any dependencies, ensure they are installed using `pip`:
```
pip install -r requirements.txt
```
**Execution Order**: Execute the Python files in the following order to get initially set up:
- `gen_config.py`
- `update_config.py`: This will calibrate the output when you input the distance measurement.
- `gen_calibration_graph.py`: This file can now be optionally run after the previous step to view your data graphically.
- `clean_data.py`: This can also be run optionally after updating the config file with data to clean up the endpoints.
- `gen_stats.py`: This will generate the statistics for the calibration process and line of best fit.
- `gen_deviation_graph.py`: This file can now be optionally run after the previous step to view your deviation from the polynomial of best fit.
- `run.py`: This can now be run with the calibrated data to produce an estimate of the distance.
