import os
import random

DICT_DATA = "currentState.txt"
PERSON_DATA = "People.csv"
OUTPUT_FILE = "Schedule.csv"
TASK_DAYS = ["Sunday","Monday","Wednesday","Thursday","Friday","Saturday"]

#Helper function for starting priorityDict fresh
def initPDict(peopleList):
	random.shuffle(peopleList)
	return {people[personIdx]:personIdx for personIdx in range(len(people))}

#Helper function to get next person from priorityDict
def nextPerson(pDict, numPeople = 1):
	prioritySortedPeople = [k for k,v in sorted(pDict.items(), key=lambda item: item[1])]
	return prioritySortedPeople[:numPeople]

#Helper function to update priorityDict when someone has been assigned a task. NOTE: 'person' could be a string or a list of strings
def updateDict(person, diff, dur, pDict):
	#Make sure that person is a list
	if isinstance(person, str):
		person = [person]
	for p in person:
		#Logic for finding out how hard a task is: (duration/10 minutes) * difficulty + random integer if the task requires more than one person
		pDict[p] = (dur//10) * diff + random.randint(-(len(person)-1),len(person)-1)
	#Subtract from each value in the priorityDict. Have to update this way due to pDict being passed by value
	subtractionUpdate = 1
	for key in pDict.keys():
		pDict[key] -= subtractionUpdate

#Helper function to assign people to a list of tasks and update priorityDict
def assignPeople(tasks, pDict, peopleList):
	assignedTasks = []
	for task in tasks:
		#Assertion
		if task[3].count(":") != 1 or not task[3].replace(":","").isdigit():
			print("ERROR: The time '" + task[3] + "' for task '" + task[0] + "' isn't valid.")
			quit()
		#Make sure that the duration is in the right format
		try:
			duration = int(task[1])
		except:
			print("ERROR: The duration for the '" + task[0] + "' task can't be converted to an integer.")
			quit()
		#Make sure that the difficulty is in the right format
		try:
			difficulty = int(task[2])
		except:
			print("ERROR: The difficulty for the '" + task[0] + "' task can't be converted to an integer.")
			quit()
		#Make sure that numPeople is in the right format
		try:
			numPeople = int(task[4])
			#Assertion
			if numPeople > len(peopleList):
				print("ERROR: The task '" + task[0] + "' has more people assigned to it than are present in the '" + PERSON_DATA + "' file.")
				quit()
		except:
			print("ERROR: The number of people for the '" + task[0] + "' task can't be converted to an integer.")
			quit()
		peopleAssigned = nextPerson(pDict,numPeople)
		assignedTasks.append([peopleAssigned,task])
		updateDict(peopleAssigned,difficulty,duration,pDict)
	return assignedTasks

#Initialize people
with open(PERSON_DATA, "r") as peopleFile:
	people = [person.strip() for person in peopleFile.readlines()]
	#Get rid of empty/blank lines
	while "" in people:
		people.remove("")

#Initialize priorityDict
if os.path.exists(DICT_DATA):
        #Read in the last dictionary state from DICT_DATA
	with open(DICT_DATA, "r") as dictFile:
		priorityDict = eval(dictFile.readline())
	#Assertion that the same people are still here
	if sorted(priorityDict.keys()) != sorted(people):
		print("Hmmm... It looks like the '" + PERSON_DATA + "' file has been edited since the last run. We'll recreate everyone's priorities real quick with the new people.")
		priorityDict = initPDict(people)
else:
	priorityDict = initPDict(people)

#Initialize taskDict
taskDict = {}
for day in TASK_DAYS:
	#Assertion that the day's file exists
	if not os.path.exists(day + ".csv"):
		print("ERROR: It looks like the task file '" + day + ".csv' doesn't exists. Please either create the file with tasks or remove the day from the 'TASK_DAYS' variable in the Python program.")
		quit()
	with open(day + ".csv", "r") as taskFile:
		lines = [line.strip() for line in taskFile.readlines()]
		#Remove blank/empty lines
		while "" in lines:
			lines.remove("")
		tasks = []
		for line in lines:
			#Assertion that there are 4 commas
			if line.count(",") != 4:
				print("ERROR: Line '" + line + "' in file '" + day + ".csv' probably isn't in the right format due to more or less than 4 commas present.")
				quit()
			tasks.append(line.split(","))
		taskDict[day] = tasks
		
#Generate schedule and write it to a file
with open(OUTPUT_FILE, "w") as outputFile:
	outputFile.write("DAY,TIME,TASK NAME,PEOPLE ASSIGNED,EXPECTED DURATION,DIFFICULTY\n")
	for day in TASK_DAYS:
		outputFile.write(day.upper()+",,,\n")
		dayTasks = assignPeople(taskDict[day],priorityDict,people)
		#Sort the tasks by the timestamp
		dayTasks = sorted(dayTasks, key=lambda item: int(item[1][3].replace(":","")))
		for task in dayTasks:
			outputFile.write(day + "," + task[1][3] + "," + task[1][0] + "," + ";".join(task[0]) + "," + task[1][1] + " mins," + task[1][2] + "\n")

#Write the current state of the priorityDict to a file
with open(DICT_DATA, "w") as dataFile:
	dataFile.write(str(priorityDict))

print("The schedule has been created and saved as '" + OUTPUT_FILE + "'. The state of the Priority Dictionary has been saved in '" + DICT_DATA + "'.")
