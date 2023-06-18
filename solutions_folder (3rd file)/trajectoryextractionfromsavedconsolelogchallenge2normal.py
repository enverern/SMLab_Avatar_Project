import json

def extract_json_lines(log_file_path):
    json_lines = []  # List to store extracted JSON lines
    
    with open(log_file_path, 'r') as file:
        log_lines = file.readlines()  # Read all lines from the log file
        
        for line in log_lines:
            line = line.strip()  # Remove leading/trailing whitespace
            
            if "Full message received" in line:
                start_index = line.index("{")  # Find the starting index of the JSON object
                new = eval(line[start_index:])  # Evaluate the JSON object as Python code
                json_lines.append(new)  # Append the extracted JSON object to the list

    with open("logtraj.json", "w") as outfile:
        json.dump(json_lines, outfile)  # Write the extracted JSON objects to a JSON file

    outfile.close()  # Close the output file

log_file_path = "ec2-54-174-51-194.compute-1.amazonaws.com-1686381038556.log" # Path to the log file
extract_json_lines(log_file_path)



