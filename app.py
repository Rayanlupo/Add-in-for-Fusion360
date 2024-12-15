import wakatime
try: 
    import adsk.core
    import adsk.fusion
    import adsk.cam
except ImportError:
    adsk = None
import json
import os 
import requests
class MockApp:
    def userInterface(self):
        print("Mock Ui called")
class adsk:
    core = MockApp()
    fusion = MockApp()
    cam = MockApp()
def run(context):
    ui = None;
    try: 
        app = adsk.core.application.get()
        ui = app.userInterface
        uia.messageBox("Hello user")
    excep: 
    if ui: 
        ui.messsageBox("Failed: \n{}".format(traceback.formate_exc()))