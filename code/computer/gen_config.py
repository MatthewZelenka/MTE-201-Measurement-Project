import json, argparse

def write_base_config(output_file:str, unit:str):
    config = {
        "unit": unit,
        "interpolation": None,
        "data": None,
    }
    with open(output_file, 'w') as json_file:
        json.dump(config, json_file, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Write dictionary to JSON file')
    parser.add_argument('output_file', type=str, help='Output JSON file path')
    args = parser.parse_args()
    
    write_base_config(args.output_file, str(input("Unit: ")))
