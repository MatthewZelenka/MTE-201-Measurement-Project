import argparse, json

import matplotlib.pyplot as plt
import numpy as np

def digital_to_voltage(array:np.ndarray):
    return (array/4095)*3.3

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Adds point to config data')
    parser.add_argument('config_file', type=str, help='Config JSON file path')
    parser.add_argument('--no-curve', dest='curve', action='store_false', help='To generate curve on graph (Defualt: True)')
    args = parser.parse_args()
    
    config:dict

    with open(args.config_file, 'r') as json_file:
        # Load the content as a dictionary
        config = json.load(json_file)
    
    x_values_data, y_values_data = zip(*config["data"])
    x_values_data = np.array(x_values_data)

    if (config["interpolation"] != None and args.curve == True):
        # Generate x values for the plot
        x_values = np.linspace(np.min(x_values_data), np.max(x_values_data), 100)

        # Generate y values using the best coefficients
        y_values = np.polyval(config["interpolation"]["coefficients"], x_values)

        # Plot the polynomial curve
        plt.plot(digital_to_voltage(x_values), y_values, color='red', label='Polynomial Fit (Degree {degree})'.format(degree=config["interpolation"]["degree"]))

        max_uncertainty_pos = config["interpolation"]["max_uncertainty_pos"] 
        max_uncertainty_neg = config["interpolation"]["max_uncertainty_neg"] 

        plt.fill_between(digital_to_voltage(x_values), y_values + max_uncertainty_neg, y_values + max_uncertainty_pos, color='gray', alpha=0.2, label='Maximum Uncertainty')

    plt.scatter(digital_to_voltage(x_values_data), y_values_data, label="Data")
    plt.xlabel('Voltage (V)')
    plt.ylabel('Distance ({unit})'.format(unit=config["unit"]))
    plt.title('Calibration {graph_type}'.format(graph_type = "Curve" if args.curve else "Scatter Plot"))
    plt.legend()
    plt.show()
