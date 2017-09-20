import ev3control.master as master
import IR_control as remoteControl
import ev3dev.ev3 as ev3
import sensors_simple # needed?? probably not
from ev3control.messages import *
import csv
import os

def data_collection_and_camera(cmd,run,ir,path,fileID):

    if (cmd==ir.REMOTE.BAECON_MODE_ON):
       path = "run_"+str(run)
       if (not os.path.exists(path)):
               os.mkdir(path)
       fileID = open(path+"/features.csv","a",newline='')
       writer = csv.writer(fileID)       
       record = 1
       return record,fileID,path,run,writer
    elif (cmd==ir.REMOTE.NONE):
       record = 0
       run = run + 1
       if (path!=None):
           fileID.close()
       return record,None,None,run,None

    return 0,None,None,run,None
          
        
def motor_control(client,topic,cmd,ir): 
    speedA = 0
    speedB = 0
    if (cmd==ir.REMOTE.RED_UP):
        speedA = -250
        master.publish_cmd(client,topic, RunMethodMessage('LargeMotor(outA)','run_forever',{'speed_sp':str(speedA)}))
        master.publish_cmd(client,topic, RunMethodMessage('LargeMotor(outD)','run_forever',{'speed_sp':str(-speedA)}))
    elif (cmd==ir.REMOTE.RED_DOWN):
        speedA = 250
        master.publish_cmd(client,topic, RunMethodMessage('LargeMotor(outA)','run_forever',{'speed_sp':str(speedA)}))
        master.publish_cmd(client,topic, RunMethodMessage('LargeMotor(outD)','run_forever',{'speed_sp':str(-speedA)}))
    elif (cmd==ir.REMOTE.BLUE_UP):
        speedB = -250
        master.publish_cmd(client,topic, RunMethodMessage('LargeMotor(outD)','run_forever',{'speed_sp':str(speedB)}))
        master.publish_cmd(client,topic, RunMethodMessage('LargeMotor(outA)','run_forever',{'speed_sp':str(-speedB)}))
    elif (cmd==ir.REMOTE.BLUE_DOWN):
        speedB = 250
        master.publish_cmd(client,topic, RunMethodMessage('LargeMotor(outD)','run_forever',{'speed_sp':str(speedB)}))
        master.publish_cmd(client,topic, RunMethodMessage('LargeMotor(outA)','run_forever',{'speed_sp':str(-speedB)}))
    elif (cmd==ir.REMOTE.RED_UP_AND_BLUE_UP):
        speedA = 250
        master.publish_cmd(client,topic, RunMethodMessage('LargeMotor(outA)','run_forever',{'speed_sp':str(speedA)}))
        speedB = 250
        master.publish_cmd(client,topic, RunMethodMessage('LargeMotor(outD)','run_forever',{'speed_sp':str(speedB)}))
    elif (cmd==ir.REMOTE.RED_DOWN_AND_BLUE_DOWN):
        speedA = -250
        master.publish_cmd(client,topic, RunMethodMessage('LargeMotor(outA)','run_forever',{'speed_sp':str(speedA)}))
        speedB = -250
        master.publish_cmd(client,topic, RunMethodMessage('LargeMotor(outD)','run_forever',{'speed_sp':str(speedB)}))
    elif (cmd==ir.REMOTE.BAECON_MODE_ON):
        master.publish_cmd(client,topic, SetAttrMessage('LargeMotor(outA)','stop_action','brake'))
        master.publish_cmd(client,topic, SetAttrMessage('LargeMotor(outD)','stop_action','brake'))
        master.publish_cmd(client,topic, SetAttrMessage('LargeMotor(outA)','command','stop'))
        master.publish_cmd(client,topic, SetAttrMessage('LargeMotor(outD)','command','stop'))
    else:
        print("Pass motors")
        pass
    return speedA,speedB,0,0
        
def gripper_control(client,topic,cmd,ir):
    speed_lift = 0
    speed_grip = 0

    if (cmd==ir.REMOTE.RED_UP):
        speed_lift = 100
        master.publish_cmd(client,topic, RunMethodMessage('LargeMotor(outB)','run_to_rel_pos',{'position_sp':str(40),'speed_sp':str(speed_lift)}))
    elif (cmd==ir.REMOTE.RED_DOWN):
        speed_lift = -100
        master.publish_cmd(client,topic, RunMethodMessage('LargeMotor(outB)','run_to_rel_pos',{'position_sp':str(50),'speed_sp':str(speed_lift)}))
    elif (cmd==ir.REMOTE.BLUE_UP):
        speed_grip = 300
        master.publish_cmd(client,topic, SetAttrMessage('MediumMotor(outC)','speed_sp',str(speed_grip)))
        master.publish_cmd(client,topic, SetAttrMessage('MediumMotor(outC)','command','run-forever'))
    elif (cmd==ir.REMOTE.BLUE_DOWN):
        speed_grip = -300
        master.publish_cmd(client,topic, SetAttrMessage('MediumMotor(outC)','speed_sp',str(speed_grip)))
        master.publish_cmd(client,topic, SetAttrMessage('MediumMotor(outC)','command','run-forever'))
    elif (cmd==ir.REMOTE.BAECON_MODE_ON):
        master.publish_cmd(client,topic, SetAttrMessage('LargeMotor(outB','stop_action','hold'))
        master.publish_cmd(client,topic, SetAttrMessage('MediumMotor(outC)','stop_action','hold'))
        master.publish_cmd(client,topic, SetAttrMessage('LargeMotor(outB)','command','stop'))
        master.publish_cmd(client,topic, SetAttrMessage('MediumMotor(outC)','command','stop'))
    else:
        print("Pass gripper")
        pass
    return 0,0,speed_lift,speed_grip
    

def emergency(client,topic,cmd,ir):
    
    sA = None
    sB = None
    sC = None
    sD = None
    if (cmd==ir.REMOTE.BAECON_MODE_ON):
        master.publish_cmd(client,topic, SetAttrMessage('LargeMotor(outA)','stop_action','brake'))
        master.publish_cmd(client,topic, SetAttrMessage('LargeMotor(outB)','stop_action','brake'))
        master.publish_cmd(client,topic, SetAttrMessage('LargeMotor(outD)','stop_action','brake'))
        master.publish_cmd(client,topic, SetAttrMessage('MediumMotor(outC)','stop_action','brake'))
        master.publish_cmd(client,topic, SetAttrMessage('LargeMotor(outA)','command','stop')) 
        master.publish_cmd(client,topic, SetAttrMessage('LargeMotor(outB)','command','stop'))
        master.publish_cmd(client,topic, SetAttrMessage('LargeMotor(outD)','command','stop'))
        master.publish_cmd(client,topic, SetAttrMessage('MediumMotor(outC)','command','stop'))
        sA = 0
        sB = 0
        sC = 0
        sD = 0
    else:
        print("Pass emergency")
        pass
    return sA,sB,sC,sD
    


call_channel = { 0 : motor_control,
                 1 : gripper_control,
                 3 : emergency
               }


def ir_to_control(client,topic,sensors):

    ir = sensors['IR_control']

    channel = ir.get_channel()
    cmd = ir.get_cmd()

    #Return speed_sp of motor A,B,C,D - 0 if stopped
    return call_channel[int(channel)](client,topic,int(cmd),ir)    
    
