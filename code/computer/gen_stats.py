import json, argparse

import numpy as np

def dynamic_polyfit(x, y, max_degree):
    best_degree = 0
    best_residual = float('inf')
    best_coefficients = None

    for degree in range(1, max_degree + 1):
        coefficients = np.polyfit(x, y, degree)
        fitted_values = np.polyval(coefficients, x)
        residual = np.sum((y - fitted_values) ** 2)

        if residual < best_residual:
            best_residual = residual
            best_degree = degree
            best_coefficients = coefficients

    return best_degree, best_coefficients, best_residual

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Adds point to config data')
    parser.add_argument('config_file', type=str, help='Config JSON file path')
    args = parser.parse_args()

    config:dict
    
    with open(args.config_file, 'r') as json_file:
        # Load the content as a dictionary
        config = json.load(json_file)
            
    
    x_values, y_values = zip(*config["data"])
    max_degree = config["interpolation"]["degree"] if config["interpolation"] else 1 
    
    try:
        max_degree = int(input("Max degree (Default: {default_max_degree}): ".format(default_max_degree = max_degree)))
    except ValueError:
        pass
    
    best_degree, best_coefficients, residual = dynamic_polyfit(x_values, y_values, max_degree)
    
    # Calculate standard deviation
    std_deviation = np.sqrt(residual / (len(x_values) - best_degree - 1))
    
    # Calculate maximum uncertainty
    trend_poly = np.polyval(best_coefficients, x_values)
    max_uncertainty_pos = np.max(y_values - trend_poly)
    max_uncertainty_neg = np.min(y_values - trend_poly)

    config["interpolation"] = {
        "degree": best_degree,
        "coefficients": list(best_coefficients),
        "residual": residual,
        "std_deviation": std_deviation,
        "max_uncertainty_pos": max_uncertainty_pos,
        "max_uncertainty_neg": max_uncertainty_neg,
    }
    
    with open(args.config_file, 'w') as json_file:
        json.dump(config, json_file, indent=4)

    print("Standard Deviation:", std_deviation)
    print("Maximum Uncertainty Pos:", max_uncertainty_pos)
    print("Maximum Uncertainty Neg:", max_uncertainty_neg)
