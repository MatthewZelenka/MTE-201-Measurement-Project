import json, argparse

import numpy as np

from data_in import stats_serial

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Adds point to config data')
    parser.add_argument('config_file', type=str, help='Config JSON file path')
    parser.add_argument('serial_port', type=str, help='Serial port')
    parser.add_argument('baudrate', type=int, help='Baud rate')
    parser.add_argument('--sample_size', type=int, default=1, help='Sample Size')
    args = parser.parse_args()

    config:dict
    
    ser = stats_serial(args.serial_port, args.baudrate)
    ser.open()

    while True:
        with open(args.config_file, 'r') as json_file:
            # Load the content as a dictionary
            config = json.load(json_file)
        
        data_values = []
        while ((len(data_values) != args.sample_size) 
                or (np.std(data_values) > 2)
                or (abs(max(data_values)-min(data_values)) > 20)):
            if (len(data_values) == args.sample_size):
                data_values.pop(0)
            data_values.append(ser.out())
        # for _ in range(args.sample_size):
            # data_values.append(val if ((val := ser.out()) != None) else float('inf'))

        serial_out = sum(data_values)/len(data_values)
        print(data_values)
        print("Delta: {delta}".format(delta = abs(max(data_values)-min(data_values))))
        print("STD: {std}".format(std = np.std(data_values)))
        measurementValue = float(input("Map {value} to {unit}: ".format(value = serial_out, unit=config["unit"])))
    
        if config["data"] == None:
            config["data"] = []
        config["data"] += [[num, measurementValue] for num in data_values]

        # test data write
        # config["data"] = [[i, i/2] for i in range(1000)]

        with open(args.config_file, 'w') as json_file:
            json.dump(config, json_file, indent=4)
        input("Enter to go to next entry")
