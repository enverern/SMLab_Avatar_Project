import json

def trajectory_create(initial_position, target_position, num_of_steps):
    # Create an empty list to store the trajectory
    trajectory = []
    
    # Generate the trajectory by interpolating between the initial and target positions
    for i in range(num_of_steps):
        step = {}
        
        # Interpolate each position parameter based on the current step
        for name, value in initial_position.items():
            step[name] = value + (target_position[name] - value) * (i / num_of_steps)
        
        # Append the interpolated step to the trajectory
        trajectory.append(step)
    
    # Write the trajectory to a JSON file
    with open("generated_traj.json", "w") as outfile:
        json.dump(trajectory, outfile)  # Write the extracted JSON objects to a JSON file
    outfile.close()  # Close the output file

initial_position = {
    "J1": 0,
    "J2": 0,
    "J3": -1.57,
    "J4": 0,
    "J5": 1.57,
    "J6": 0
}
target_position = {
    "J1": 0.538,
    "J2": 0.7637362481385295,
    "J3": -1.8800761286392603,
    "J4": -0.10164862748520956,
    "J5": 0.4487,
    "J6": 0.5795
}

trajectory_create(initial_position, target_position, 100)



