import Devices
import time

sim_state = True # Simulation state.  Set to False to interact with gantry
log = ''  # Just something to keep track of what has been done

# Create and instance of the device and set its simulations state
gantry = Devices.Aerotech_A3200_RoboDaddy('gantry')
gantry.simulation = sim_state

# Connect to the device
log += gantry.Connect()
# Here is where I would test out various device procedures
log += gantry.Disconnect()
# Print the log to see if it makes sense.
print(log)
