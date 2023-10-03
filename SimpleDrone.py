import airsim
import os

"""
Ripped most of this code from


https://github.com/jn89b/utm/blob/noetic/utm/scripts/uas/simple_flight_drone.py

Api used from
https://microsoft.github.io/AirSim/api_docs/html/

"""

class SimpleFlightDrone():
    """Control the SimpleFlight AirsimDrone"""
    def __init__(self):
        self.client = airsim.MultirotorClient()
        self.world_client =  airsim.VehicleClient()
        
        self.client.confirmConnection()
        self.client.enableApiControl(True)
    
    def arm(self) -> None:
        self.client.armDisarm(True)
        
    def disarm(self) -> None:
        self.client.armDisarm(False)
        
    def takeoff(self, position:list, alt_m:float) -> None:
        self.client.takeoffAsync().join()
        self.client.moveToPositionAsync(position[0], position[1], position[2], alt_m).join()
        
    def get_current_state(self) -> dict:
        return self.client.simGetGroundTruthKinematics()
    
    def get_current_position(self) -> list:
        return self.client.simGetGroundTruthKinematics().position
    
    def move_to_position(self, position:list, vel_ms:float, timeout_sec:float=3) -> None:
        self.client.moveToPositionAsync(
            position[0], position[1], position[2], vel_ms, timeout_sec).join()    

    def get_object_position(self, object_name:str) -> list:
        return self.client.simGetObjectPose(object_name).position

def some_helpful_examples(simpledrone:SimpleFlightDrone) -> None:
    # this returns all the states 
    print(simpledrone.get_current_state())
    
    #here's how to get the position and the 
    print(simpledrone.get_current_position().x_val)    



"""
If you are using position commands you can keep it consistent with
Unreal Engine frames.

For velocity commands airsim takes it in NED frame
"""

if __name__=='__main__':
    
    simpledrone = SimpleFlightDrone()
    simpledrone.arm()
    takeoff_position = [10, 10, -10] #These positions are in NED Frame
    airspeed_ms = 5 #m/s
    simpledrone.takeoff(takeoff_position, airspeed_ms)
    
    #THIS has to be the Unreal ID of the object
    target_object = "Sphere_2"
    object_vector = simpledrone.get_object_position(target_object)
    offset_height_m = -20 # REMEMBER NEGATIVE IS UP IN Z
    print("object location is: ", object_vector)  
    dt = 0.1 
    
    while True:
        try:
            object_vector = simpledrone.get_object_position(target_object)
            object_location = [object_vector.x_val, object_vector.y_val, object_vector.z_val + offset_height_m]
            simpledrone.move_to_position(object_location, airspeed_ms, dt)
            
        except KeyboardInterrupt:
            print("Keyboard Interrupt")
            break

    
    
    



    