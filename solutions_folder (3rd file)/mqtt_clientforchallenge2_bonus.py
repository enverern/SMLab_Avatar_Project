import paho.mqtt.client as mqtt

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe("/DF/anim/json/ProductionLine") # Topic to subscribe
    else:
        print("Connection failed with error code", rc)

def on_message(client, userdata, msg):
    traj = eval(msg.payload.decode())
    sending_message = conv(traj)
    publish_message(client, sending_message)

def publish_message(client, message):
    # Publish the message to the same client
    topic = "/DF/anim/json/RoboticCell" # Topic to publish
    payload = str(message)
    client.publish(topic, payload)

def conv(data):
    # create a dictionary (second_dict) to utilize while creating the animation file
    second_dict = {}
    
    # specify the variables in the context section of animation file
    second_dict["context"] = {"assetTrail": False, "UnitOfMeasureScale": 1, "Zup": False, "RepoAnim": ""}

    # create nodes, sequences, and bookmarks sections as a part of animation file 
    second_dict["nodes"] = []
    for name, value in data.items():
        # create a node for each joint and assign the id according to the hierarchy of the robot
        # there is 10 joints in the trajectory file, but only 6 of them are avaliable in the robot and the rest are not used
        if int(name[1:]) <= 6:
            # assign the initial rotation of each joint

            # each joint can rotate only around Z-axis according to URDF file that has Z-up coordinate system,
            # but we need to rotate around Y-axis according to the animation file that has Y-up coordinate system so assign the value to Y-axis
            node = {
                "id": "Robot_1.Link_" + name[1:],
                "actions": [
                    {
                        "event": {
                            "type": "show",
                            "rotation": [0, value, 0], 
                            "placementRelTo": "Robot_1.Joint_" + name[1:]
                        }
                    }
                ]
            }

            # append each node to the nodes section of the animation file initially
            second_dict["nodes"].append(node)
    return second_dict

# Create MQTT client instance
client = mqtt.Client()

# Assign callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
broker_url = "broker.emqx.io"
broker_port = 1883
client.connect(broker_url, broker_port)

# Start the MQTT loop
client.loop_forever()
