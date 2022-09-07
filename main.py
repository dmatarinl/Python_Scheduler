import jsonschema
import json

from ctrl import Control
from jsonschema import *
from tasks import Task



def main():
    ## The objective of the main function here will be 
    #  1- Creating the main loop 
    #  2- Start using the functions from Control Class
   
    list_tasks_json = Json_Op_Doc()
    
    total_tasks = Task_Generator(list_tasks_json["tasks"])
    
    cntrl = Control.Get_Obj()
    
    cntrl.Starting_Tasks(total_tasks)
    
    cntrl.Results()
    
    cntrl.Terminate_Loop()
    


def Json_Op_Doc():
    ## This function opens json files, 
    #  Reads them  
    #  Keeps the data saved in a list of current tasks
    
    with open('../scheduler_David/input1.json') as Doc_JSON:
        
        Curr_tasks= json.load(Doc_JSON)
        
    with open('../scheduler_David/schema.json') as Doc_JSON:
        
        curr_Schema= json.load(Doc_JSON)
        
        try:
            validate(Curr_tasks, curr_Schema)
            
        except jsonschema.exceptions.ValidationError:
            
            print("Error \n")
    
    return Curr_tasks
 
def Task_Generator(task_INPUTS):
    ## For each task that the input1.json file has
    #  Creates an object from Class Task inside tasks.py
    #  It will return a list of task classes.
    
    List=[]
    
    for INPUTS in task_INPUTS:
        
        if "dependencies" in INPUTS:
            
            curr_tasks= Task(
                INPUTS["name"], 
                INPUTS["type"], 
                INPUTS["arguments"], 
                INPUTS["dependencies"]
                )
        else:
            curr_tasks= Task(
                INPUTS["name"], 
                INPUTS["type"], 
                INPUTS["arguments"], 
                None
                )
        
        List.append(curr_tasks)
    
    return List

# Calling main function
main()


