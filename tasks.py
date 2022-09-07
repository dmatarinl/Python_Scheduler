import asyncio
import sys

from ctrl import Control

class Task:
    ## Class Task, digital representation of each task from input1.json
    
    def __init__(self, name, task_types, arguments, dependencies):
        ## Created according to the rules of the test 
        #  The name, type, arguments, dependencies and state.
        
        
        self.__name= name
        self.__type= task_types
        
        self.__arguments= arguments
        
        self.__Stat= "Awaiting"
        # In case of dependencies we check if there are or not and how many
        
        if dependencies is not None and len(dependencies) > 0:
            
            self.__dependencies= set()
            
            for tot_dependencies in dependencies:
                
                self.__dependencies.add(tot_dependencies)
        else:
            self.__dependencies = None
                

    def Get_Name(self):
        ## Function Get to return the name of task
        
        return self.__name
    
    def Get_Dependencies(self):
        ## Function Get to return the dependencies of task
        
        return self.__dependencies
    
    def Get_Stat(self):
        ## Function Get to return the state of task
        
        return self.__Stat
    
    async def Perform_Task(self, First_Stage_Depend, Final_Stage_Depend):
        ## Will Perform the Task objective, written in the json file
        #  The task can have a shell command or has a code snippet as argument
        
        #  If the return code from the execution in the shell is diferent from 0
        #  it will be considered a failure
        
        #  In the case of the code snippet, if it raises an Exception
        #  it will be considered a failure
        
        # It ends communicating that the task is terminated and wakes up the controller
        
        print("Started " + self.__name)
        
        if First_Stage_Depend is not None:
            
            await First_Stage_Depend.wait()
            
        if self.__type == "exec":
            
            try:
                # If the task received has shell commands then start it
                subproc= await asyncio.create_subprocess_shell(self.__arguments, stdout=asyncio.subprocess.PIPE)
                await subproc.wait()

                if subproc.returncode != 0:
                    self.__Stat= "fail"
                
                else:
                
                    SPlines= (await subproc.communicate())[0].splitlines()
                    
                    for firstline in SPlines:
                        print(firstline.strip())
                    
                    self.__Stat= "ok"
            
            except Exception as E:
                
                print(E)
                
                self.__Stat= "fail"
        
        else:
            
            try:
                subproc= await asyncio.create_subprocess_exec(sys.executable, '-c', self.__arguments, stdout=asyncio.subprocess.PIPE)
                await subproc.wait()
                
                SPlines= (await subproc.communicate())[0].splitlines()
                
                for firstline in SPlines:
                    print(firstline.strip())
                
                self.__Stat= "ok"
            
            except Exception as E:
                print(E)
                self.__Stat= "fail"
                
        print("Ended " + self.__name)
        
        Control.Get_Obj().Message_Sender([self.__name, self.__Stat])
        Final_Stage_Depend.set()
    
    def Check_Dependencies(self):
        ## There is a possibility that a task doesn't have any dependencies
        #  Checks if there is one then returns True, if not returns False
        
        if self.__dependencies is not None:
            
            return True
        
        return False

