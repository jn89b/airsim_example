# ready to run example: PythonClient/multirotor/hello_drone.py
import airsim
import os

# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

# Async methods returns Future. Call join() to wait for task to complete.
client.takeoffAsync().join()
client.moveToPositionAsync(-10, 10, -10, 5).join()


#we want to get the object position
object_name = "Sphere_2"
print(client.simListSceneObjects())

object_location = client.simGetObjectPose(object_name)

print("object location is: ", object_location)
