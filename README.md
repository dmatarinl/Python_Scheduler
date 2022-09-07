# Python_Scheduler

### Receiving tasks from a json file, this scheduler will proceed to executing them in the most optimal method

Requirements:

- Written in the **latest version of python, it will work if it's in python 3.6 or higher**
- Created using python/asyncio concurrency mechanism
- Be sure to put the json files **inside jsonfiles folder**
- To run the program just call **python main.py** in the console

After all tasks have proceeded to execute by console.
A perfect completition of the tasks will look like this:

```
task5 Ok
task2 Ok
task1 Ok
task4 Ok
task3 Ok
task8 Ok
task9 Ok
task7 Ok
task6 Ok
```
### IMPORTANT

**Some of the arguments of the inputs.json documents in this test were intended to be performed on a linux console, so if you are a microsoft windows user like me and you don't want to use a virtualbox with ubuntu to compile it, I recommend change some arguments of the jsonfile.**

The ones that will cause conflict are:

- **Sleep** (Change it to "timeout", is the equivalent)
- **ls** (Change it to "dir", is the equivalent).
- **False** (As there is not an equivalent of this command in microsoft windows, I recommend changing it to an existing command)


