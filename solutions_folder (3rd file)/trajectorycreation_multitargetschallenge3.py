import numpy as np
import json

def trajectory_create(*args):
    """
    Generates a trajectory by interpolating between given positions.

    Args:
        *args: The first argument must be the initial position and target positions must be added respectively.
               The last argument must be the total number of steps.
        Format of position variables: position = {"J1": 0,"J2": 0,"J3": -1.57,"J4": 0,"J5": 1.57,"J6": 0}
    Returns:
        None
    """
    # Create an empty list to store the trajectory
    trajectory = []
    
    # Extract the points and number of steps from the input arguments
    points = args[:-1]
    num_of_steps = args[-1]
    
    # Calculate the weights for each segment based on the differences between points
    weights = np.array([])
    difference = []
    for i in range(len(points) - 1):
        difference[i] = sum(abs(np.array(list(points[i+1].values())) - np.array(list(points[i].values()))))
    
    # Calculate the weights as the ratio of each difference to the total difference
    for i in range(len(points) - 1):
        weights[i] = difference[i] / sum(difference)
    
    # Calculate the number of steps for each segment based on the weights
    partial_num_of_steps = weights * num_of_steps
    
    # Generate the trajectory by interpolating between the points
    for i in range(len(points) - 1):
        for j in range(partial_num_of_steps):
            step = {}
            
            # Interpolate each position parameter based on the current step and partial number of steps
            for name, value in points[i].items():
                step[name] = value + (points[i + 1][name] - value) * (j / int(partial_num_of_steps[i]))
            
            # Append the interpolated step to the trajectory
            trajectory.append(step)
    
    # Append the last point to the trajectory
    trajectory.append(points[-1])
    
    # Write the trajectory to a JSON file
    with open("generated_traj.json", "w") as outfile:
        json.dump(trajectory, outfile)
    outfile.close()

initial_position = {
    "J1": 0,
    "J2": 0,
    "J3": -1.57,
    "J4": 0,
    "J5": 1.57,
    "J6": 0
}
middle_position = {
    "J1": 0.5976,
    "J2": 0.4833,
    "J3": -1.9479,
    "J4": -0.0893,
    "J5": 0.5846,
    "J6": 0.5093
}
target_position = {
    "J1": 0.538,
    "J2": 0.7637362481385295,
    "J3": -1.8800761286392603,
    "J4": -0.10164862748520956,
    "J5": 0.4487,
    "J6": 0.5795
}

trajectory_create(initial_position, middle_position, target_position, 100)
