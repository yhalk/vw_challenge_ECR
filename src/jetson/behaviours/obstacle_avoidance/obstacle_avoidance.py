from Vision.vision_commands import publish_vision_info
from Sensors.sensors_simple import IR_teensy
import json


def obstacle_avoidance(dict_params, json_params, client):

    current_phase = dict_params['phase']

    #Save updated phase of exploration
    with open(json_params, "r") as jsonFile:
         data = json.load(jsonFile)
         params = data["explore"]  #need to have explore as behaviour
         phase = params["phase"]
         params["phase"] = phase - 1
         data["explore"] = params

    with open(json_params, "w") as jsonFile:
         json.dump(data, jsonFile)

    if current_phase<0:
       print("End of exploration.")
       publish_vision_info(client,topic="vision",info=["exploration",0,0])
       with open(json_params, "r") as jsonFile:
         data = json.load(jsonFile)
         params = data["explore"]  #need to have explore as behaviour
         phase = params["phase"]
         params["phase"] = 6
         data["explore"] = params

       with open(json_params, "w") as jsonFile:
         json.dump(data, jsonFile)
    else:
       print(exploration_dst[current_phase],exploration_angle[current_phase])
       print("Exploration phase: " + str(current_phase))
       publish_vision_info(client,topic="vision",info=["exploration",exploration_dst[current_phase],exploration_angle[current_phase]])
       
       
