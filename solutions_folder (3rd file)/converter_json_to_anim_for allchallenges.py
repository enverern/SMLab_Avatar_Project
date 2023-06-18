import json

# Import the trajectory file (in JSON format) to be converted into an animation file (also in JSON format)
with open("trajectory_1.json", "r") as read_file:
    # Assign the imported trajectory to the mylist variable
    mylist = json.load(read_file)

def conv(data):
    # Create a dictionary (second_dict) to be used while creating the animation file
    second_dict = {}
    
    # Specify the variables in the context section of the animation file
    second_dict["context"] = {
        "assetTrail": False,
        "UnitOfMeasureScale": 1,
        "Zup": False,
        "RepoAnim": ""
    }

    # Create sections for nodes, sequences, and bookmarks as part of the animation file 
    second_dict["nodes"] = []
    second_dict["sequences"] = []
    second_dict["bookmarks"] = []

    # Initialize the actual time to 0
    actual_time = 0

    for name, value in data[0].items():
        # Create a node for each joint and assign an ID according to the robot's hierarchy
        # There are 10 joints in the trajectory file, but only 6 of them are available in the robot and the rest are not used
        if int(name[1:]) <= 6:
            # Assign the initial rotation of each joint

            # Each joint can rotate only around the Z-axis according to the URDF file, which has a Z-up coordinate system.
            # However, we need to rotate around the Y-axis according to the animation file, which has a Y-up coordinate system. So assign the value to the Y-axis.
            node = {
                "id": "Robot_1.Link_" + name[1:],
                "actions": [
                    {
                        "trigger": {
                            "type": "timestamp",
                            "data": str(actual_time)
                        },
                        "event": {
                            "type": "show",
                            "rotation": [0, value, 0],
                            "placementRelTo": "Robot_1.Joint_" + name[1:]
                        }
                    }
                ]
            }
            
            # Append each node to the nodes section of the animation file initially
            second_dict["nodes"].append(node)
    
    # For each time step in the trajectory file, create an action for each joint and assign the rotation values to each joint
    for link in data[1:]:
        # Increment the actual time according to the time step of the trajectory file
        actual_time += 100 

        # Iterate through the joints and create an action for each joint for each time step
        for name, value in link.items():
            if int(name[1:]) <= 6:
                # Create an action for each joint, assign the rotation and time values to each joint
                action = {
                    "trigger": {
                        "type": "timestamp",
                        "data": str(actual_time)
                    },
                    "event": {
                        "type": "show",
                        "rotation": [0, value, 0],
                        "placementRelTo": "Robot_1.Joint_" + name[1:]
                    }
                }
                # Append each action to the actions section of the related node (joint)
                second_dict["nodes"][int(name[1:])-1]["actions"].append(action)
    
    # We have action sequences for each joint in the nodes section of the animation file

    # Create an animation file in JSON format and write the second_dict, which has the animation file format, to the file
    with open("anim_traj1.json", "w") as outfile:
        json.dump(second_dict, outfile) 
    outfile.close()
           
conv(mylist)
read_file.close()

