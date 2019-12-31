'''
This file is an example of how to interact with APE as a single-process
application.
'''

import Core
import Procedures
from AppTemplates.RoboDaddyMonolith import RoboDaddyMonolith as AppBuilder

MyApparatus = Core.Apparatus()
MyExecutor = Core.Executor()
MyApparatus.executor = MyExecutor

materials = [{'test_material': 'A'}]
# These are other tools that can be added in. Comment out the ones not used.
tools = []
# tools.append({'name': 'TProbe', 'axis': 'ZZ2', 'type': 'Keyence_GT2_A3200'})
# tools.append({'name': 'camera', 'axis': 'ZZ4', 'type': 'IDS_ueye'})
AppBuilder(MyApparatus, materials, tools)

# Define the rest of the apparatus
mat0 = list(materials[0])[0]
MyApparatus['devices']['n' + mat0]['descriptors'].append(mat0)
MyApparatus['devices']['n' + mat0]['trace_height'] = 5
MyApparatus['devices']['n' + mat0]['trace_width'] = 0.3
MyApparatus['devices']['gantry']['default']['speed'] = 1  # change the slide default from 40 to 20
MyApparatus['devices']['gantry']['n' + mat0]['speed'] = 1  # Calibration is on so this is overwritten
MyApparatus['devices']['pump0']['descriptors'].append(mat0)
MyApparatus['devices']['pump0']['pumpon_time'] = 0.0  # Time from pump on to motion, if calibration is on so this is overwritten
MyApparatus['devices']['pump0']['mid_time'] = 0.0  # time from signal sent to motion initiation
MyApparatus['devices']['pump0']['pumpoff_time'] = 0.0  # time from end-arrival to turn off pump
MyApparatus['devices']['pump0']['pumpres_time'] = 0.0
MyApparatus['devices']['pump0']['pressure'] = 10
MyApparatus['devices']['pump0']['vacuum'] = 0
MyApparatus['devices']['pump0']['COM'] = 7
MyApparatus['devices']['pump0']['trigger'] = 'com'


# Connect to all the devices in the setup
#MyApparatus.Connect_All(simulation=True)
MyApparatus.Connect_All()

# Renaming some elements for the variable explorer
information = MyApparatus['information']
proclog = MyApparatus['proclog']

# Setup information
MyApparatus['information']['materials'][mat0] = {'density': 1.92, 'details': 'Measured', 'calibrated': False}  # changed from density = 1.048
MyApparatus['information']['materials'][mat0]['do_speedcal'] = True
MyApparatus['information']['materials'][mat0]['do_pumpcal'] = False
MyApparatus['information']['ink calibration']['time'] = 10

# Setup toolpath generation and run a default
GenTP = Procedures.Toolpath_Generate(MyApparatus, MyExecutor)
GenTP.setMaterial(mat0)
GenTP.setGenerator('Ros3daTPGen')
#GenTP.setGenerator('MecodeTPGen')
#GenTP.setGenerator('TemplateTPGen')
GenTP.setParameters()  # Creates the parameter structure for TPGen
TP_gen = MyApparatus['information']['ProcedureData']['Toolpath_Generate']
TP_gen['parameters']['tiph'] = 4
TP_gen['parameters']['length'] = 5

# Create instances of the procedures that will be used
# Procedures that will almost always be used at this level

AlignPrinter = Procedures.User_FlexPrinter_Alignments_Align(MyApparatus, MyExecutor)
CalInk = Procedures.User_InkCal_Calibrate(MyApparatus, MyExecutor)
PrintTP = Procedures.Toolpath_Print(MyApparatus, MyExecutor)
TraySetup = Procedures.SampleTray_XY_Setup(MyApparatus, MyExecutor)
TrayRun = Procedures.SampleTray_Start(MyApparatus, MyExecutor)
Planner = Procedures.Planner_Combinatorial(MyApparatus, MyExecutor)


class Sample(Core.Procedure):
    def Prepare(self):
        self.name = 'Sample'
        self.GenTP = Procedures.Toolpath_Generate(self.apparatus, self.executor)
        self.PrintTP = Procedures.Toolpath_Print(self.apparatus, self.executor)
        self.Planner = Procedures.Planner_Combinatorial(self.apparatus, self.executor)
    
    def Plan(self):
        space = {}
        space['tiph'] = [0.1]
        space['Trace_height'] = [0.15]
        AppAdds = {}
        AppAdds['tiph'] = ['information', 'ProcedureData', 'Toolpath_Generate', 'parameters', 'tiph']
        AppAdds['Trace_height'] = ['devices', 'n' + mat0, 'trace_height']
        priority = ['Trace_height', 'tiph']
        self.Planner.Do({'space': space, 'Apparatus_Addresses': AppAdds, 'file': 'run.json', 'priority': priority})
        if not self.Planner.Done:
            if self.apparatus.simulation:
                import time
                time.sleep(1)
            print('Generating toolpath')
            self.GenTP.requirements['generator']['address'] = ['information', 'ProcedureData', 'Toolpath_Generate', 'generator']
            self.GenTP.Do()
            print('Printing toolpath')
            self.PrintTP.requirements['toolpath']['address'] = ['information', 'ProcedureData', 'Toolpath_Generate', 'toolpath']
            self.PrintTP.Do()


# Do the experiment
AlignPrinter.Do({'primenoz': 'n' + mat0})
CalInk.Do({'material': mat0})
TraySetup.Do({'trayname': 'test_samples', 'samplename': 'sample', 'xspacing': 14, 'xsamples': 1, 'yspacing': 15, 'ysamples': 1})
TrayRun.requirements['tray']['address'] = ['information', 'ProcedureData', 'SampleTray_XY_Setup', 'trays', 'test_samples']
TrayRun.Do({'procedure': Sample(MyApparatus, MyExecutor)})
MyApparatus.Disconnect_All()
toolpath = TP_gen['toolpath'][0]
#toolpath_parsed = tpt.parse_endofmotion(toolpath, 1E-12)
