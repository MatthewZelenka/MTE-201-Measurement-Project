import json, argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Adds point to config data')
    parser.add_argument('config_file', type=str, help='Config JSON file path')
    parser.add_argument('--upper', type=int, default=None, help='Upper bound')
    parser.add_argument('--lower', type=int, default=None, help='Lower bound')
    args = parser.parse_args()

    config:dict
    
    with open(args.config_file, 'r') as json_file:
        # Load the content as a dictionary
        config = json.load(json_file)
        
    new_data_values = []

    for pair in config["data"]:
        x_value = pair[0]
        if ((True if (args.upper == None) else args.upper > x_value) and (True if (args.lower == None) else args.lower < x_value)):
            new_data_values.append(pair)
    
    config["data"] = new_data_values 

    with open(args.config_file, 'w') as json_file:
        json.dump(config, json_file, indent=4)
