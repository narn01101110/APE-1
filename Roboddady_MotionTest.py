from Devices import Aerotech_A3200_RoboDaddy

myA3200 = Aerotech_A3200_RoboDaddy('myA3200')
myA3200.Connect()
myA3200.Move(point={'X':-100},motiontype='linear',speed=5,motionmode='incremental')
myA3200.Run()