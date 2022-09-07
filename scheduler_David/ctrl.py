import asyncio


## Class that will be the controller of the tasks 
#  Using unique instance pattern

class Control:
    
    ## Creation of the instance object
    __obj = None
    
    @staticmethod
    def Get_Obj():
        
        if Control.__obj is None:
            Control()
        
        return Control.__obj
    
    ## Creation of the private constructor from Class Control
    def __init__(self):
        
        if Control.__obj is not None:
            
            raise Exception("Get the object using Get_Obj() Function")
        
        else:
            
            # Singleton pattern
            Control.__obj= self 
            
            # List that will be saving the tasks
            self.__List_of_Tasks= None 
            
            # List that will be saving messages from the tasks
            self.__All_Messages= []
            
            # Different Set for Skipped, Finished and Failed tasks
            self.__Skipped_Tasks= set()
            self.__Finished_Tasks= set()
            self.__Failed_Tasks= set()
            
            
            
            # Creating the wake up call
            self.__Final_Event= asyncio.Event()
            # List that will save events for each task
            self.__First_Event= []
            
            # Creating the loop of the events
            self.__Event_Loop= asyncio.get_event_loop()
    
    def Results(self):
        ## Will print at the end of the loop
        #  the total results of finished, failed and skipped tasks
        print()
        for solution in self.__Finished_Tasks:
            
            print(solution + " Ok")
        
        for solution in self.__Failed_Tasks:
            print(solution + " Failed")
            
        for solution in self.__Skipped_Tasks:
            print(solution + " Skipped")
    
    def Message_Sender(self, mess):
        ## This function will add the message to a list
        
        self.__All_Messages.append(mess)
            
    def Starting_Tasks(self, tasks):
        ## This will add the tasks to the main loop
        #  Using the synchronizing function for the rest of the tasks
        #  Creates a single task at a time
        
        self.__List_of_Tasks = tasks
        
        self.__Event_Loop.create_task(self.Sync_Tasks())
        
        for task in self.__List_of_Tasks:
            
            if task.Check_Dependencies():
                awaiting = asyncio.Event()     
                
                self.__First_Event.append([awaiting, 
                                           task])
                
                self.__Event_Loop.create_task(task.Perform_Task(awaiting, 
                                                                self.__Final_Event)) 
                
            else:
                self.__Event_Loop.create_task(task.Perform_Task(None, 
                                                                self.__Final_Event))
                
        self.__Event_Loop.run_forever()
             
    async def Sync_Tasks(self):
        ## This function will signal the tasks created if they can start running
        #  We will keep the number of tasks ended
        #  It will be awaiting until a task has finished
        #  It will check if a task can run
        #  If not it will be considered skipped
        #  It will cancel every skipped task
        
        
        tot_end_tasks= 0
        
        while tot_end_tasks < len(self.__List_of_Tasks):
            
            await self.__Final_Event.wait()
            
            for mess in self.__All_Messages:
                if mess[1] == "ok":
                    self.__Finished_Tasks.add(mess[0])
                
                elif mess[1] == "skip":
                    self.__Skipped_Tasks.add(mess[0])
                
                elif mess[1] == "fail":
                    self.__Failed_Tasks.add(mess[0])
                
                self.__All_Messages.remove(mess)
                
                tot_end_tasks +=1
            
            for First_Event in self.__First_Event:
                
                if First_Event[1].Get_Dependencies().issubset(self.__Finished_Tasks):
                    
                    First_Event[0].set()
                    self.__First_Event.remove(First_Event)
                
                elif len(First_Event[1].Get_Dependencies().intersection(self.__Failed_Tasks)) > 0 \
                    or len(First_Event[1].Get_Dependencies().intersection(self.__Skipped_Tasks)) > 0:
                        
                        self.__Skipped_Tasks.add(First_Event[1].Get_Name())
                        self.__First_Event.remove(First_Event)
                        
                        tot_end_tasks +=1
                        
            # Refresh signal          
            self.__Final_Event.clear()
            
        for alltasks in asyncio.all_tasks():
            
            # Shutting down the skipped tasks
            alltasks.cancel()
            
            try:
                await alltasks
            
            except asyncio.CancelledError:
                print("The Failed or Skipped Tasks will be cancelled unfinished")
        
        self.__Event_Loop.stop()
          
    def Terminate_Loop(self):
        ## before the app closure, finish the loop created
        
        self.__Event_Loop.close()
        
         

    
    
        
   