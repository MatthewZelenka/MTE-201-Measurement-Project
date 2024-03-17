import argparse, json

import matplotlib.pyplot as plt
import numpy as np

def digital_to_voltage(array:np.ndarray):
    return (array/4095)*3.3

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Adds point to config data')
    parser.add_argument('config_file', type=str, help='Config JSON file path')
    args = parser.parse_args()
    
    config:dict

    with open(args.config_file, 'r') as json_file:
        # Load the content as a dictionary
        config = json.load(json_file)
    
    if (config["interpolation"] == None):
        print("Generate statistics first")
        exit()

    x_values_data, y_values_data = zip(*config["data"])
    x_values_data = np.array(x_values_data)

    y_values_deviation = y_values_data-np.polyval(config["interpolation"]["coefficients"], x_values_data)

    plt.scatter(digital_to_voltage(x_values_data), y_values_deviation, label="Data")
    plt.xlabel('Voltage (V)')
    plt.ylabel('Distance From Actual Length ({unit})'.format(unit=config["unit"]))
    plt.title('Deviation Plot')
    plt.legend()
    plt.show()
