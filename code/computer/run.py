import argparse, json

import numpy as np

from data_in import stats_serial

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Adds point to config data')
    parser.add_argument('config_file', type=str, help='Config JSON file path')
    parser.add_argument('serial_port', type=str, help='Serial port')
    parser.add_argument('baudrate', type=int, help='Baud rate')
    args = parser.parse_args()

    config:dict

    SAMPLE_SIZE = 2000
    sample_array = []
    
    with open(args.config_file, 'r') as json_file:
        # Load the content as a dictionary
        config = json.load(json_file)
    
    ser = stats_serial(args.serial_port, args.baudrate)
    ser.open()
    

    max_uncertainty_pos = config["interpolation"]["max_uncertainty_pos"] 
    max_uncertainty_neg = config["interpolation"]["max_uncertainty_neg"] 
    
    x_values_data, y_values_data = zip(*config["data"])
    
    x_values_data_min = min(x_values_data) + max_uncertainty_neg

    x_values_data_max = max(x_values_data) + max_uncertainty_pos

    while True:
        serial_value = ser.out()
        sample_array.append(serial_value)
        if (
                (serial_value == None or serial_value > x_values_data_max or serial_value < x_values_data_min) 
                and ((len(sample_array) != SAMPLE_SIZE) 
                or (np.std(sample_array) > 2)
                or (abs(max(sample_array)-min(sample_array)) > 20))):
            continue
        current_value = np.polyval(config["interpolation"]["coefficients"], serial_value)
        print("Value from {max_value} {unit} to {min_value} {unit}".format(max_value=current_value+max_uncertainty_pos, min_value=current_value+max_uncertainty_neg, unit=config["unit"]))
