# Task-Manager

A small program developed for my Hall Advisor that assigns people to tasks based on the tasks' duration and difficulty. A dictionary is stored in a text file between runs to save the program's internal state and is used to assign people to more or less tasks based on how difficult and long each task is.

## How To Run

Simply run the `generateSchedule.py` file and the tasks given in the "Task" folder and the people in `People.csv` will be used to populate the schedule, `Schedule.csv`.

<pre>
python generateSchedule.py
</pre>

## Input

The `People.csv` file holds the names of all possible people that can be assigned to a task.

Inside of the "Task" folder are .csv files that contain all of the information of the tasks for each day. Each task is listed in the following format:

Name of Task (without commas), Time (in minutes), Difficulty (as an integer), Time of Day (in military time and with a ":"), Number of People Required (as an integer)

## Mechanics

Each person is assigned an integer that is related to how hard their last task that they completed was. When a new task needs to be assigned people, the persons with the lowest integers are assigned to the task. After assignment, each person assigned to the new task receives a new integer based upon the equation below:

<pre>
new integer = (duration minutes // 10) * difficulty of the task + random integer
</pre>

The duration minutes is integer divided by 10 to reduce the influence of the duration on the new integer. The random integer provides some randomization when groups of people (Number of People Required > 1) are assigned to the same task. The randomization prevents the same people being assigned to tasks together over and over again because their integer is always randomly slightly different.

When integers are updated for an assigned task, every single person in the dictionary's integer is also subtracted by 1. This gradually decreases integers and prepares people to be selected for future tasks. NOTE: The subtration value of 1 could need to be changed/fine-tuned for different use cases or for when task difficulties are very high.

## Output

The final schedule will be output to the `Schedule.csv` file.
