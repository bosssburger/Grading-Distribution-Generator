# Creating grading distribution for quizzes and exams

#import sys, math, random, numpy as np
import random

tas = open("tas.csv")

taDict = {}
num_tas = 0

# Get all the TA info from csv and ignore pedram
for ta in tas:
	info = ta.split(",")
	if "Pedram" not in info[0]:
		# Mark undergrads with 1 and grads with 2 since they do twice the work
		if "10" in info[3]:
			taDict[info[0]] = 1
		else:
			taDict[info[0]] = 2
			num_tas += 1
		num_tas += 1

# Calculate how many problems each ta needs to do
# info.txt format:
# [# of total submissions],[# of coding questions],[comma separated list of # of rubric items for each question]
args = open("info.txt")
info = args.readline().split(",")

submissions = int(info[0])
num_questions = int(info[1])
rubric_items = list(map(int, info[2:]))

# Calculate the total point value for each TA
'''
This distribution style uses a stride based method

The "total value" of the quiz/exam is a weighted total where each question is given a weight based on the # of rubric items it has
Then each ta is allotted an even amount of the total value and assigned questions until their allotment is filled
In order to account for remainder of the total value, every other TA takes an extra question which puts their allotment below 0
'''

total_allotment = 0
for q in range(num_questions):
	total_allotment += submissions * rubric_items[q]

q_per_ta = total_allotment / num_tas

# Account for grads vs undergrads
for ta in taDict.keys():
	taDict[ta] = taDict[ta] * q_per_ta

# shuffle list so that everybody gets a chance to be doing the "easy" questions. 
# Mentally it feels better even though theoretically the time taken should be equal
tas_shuffled = list(taDict.keys())
random.shuffle(tas_shuffled)

start = 1
curr_q = 1
curr_problem = 0
took_extra = 0
for ta in tas_shuffled:
	assignment = ta + ": Q" + str(curr_problem + 1) + ": "
	start = curr_q

	while taDict[ta] > (0 if took_extra == 0 else rubric_items[curr_problem]):
		if curr_q >= submissions + 1:
			curr_problem += 1
			assignment += str(start) + "-End, Q" + str(curr_problem + 1) + ": "
			curr_q = 1
			start = 1
		taDict[ta] -= rubric_items[curr_problem]
		curr_q += 1
		if curr_q >= submissions + 1 and curr_problem == num_questions - 1:
			break

	if taDict[ta] < 0:
		took_extra = 1
	else:
		took_extra = 0
		
	assignment += str(start) + "-" + (str(curr_q - 1) if curr_q - 1 < submissions else "End")
	print(assignment)

'''
THIS CODE ASSIGNS GRADING BY EQUAL SUBMISSIONS
===============================================================================================
total_grading = submissions * num_questions
problems_each = math.floor(total_grading / num_tas)

# Some TAs will have to do one more for remainder
remainder = total_grading % num_tas

# Randomize TA order 
tas_shuffled = list(taDict.keys())
random.shuffle(tas_shuffled)

# Assign the first [remainder] TAs to do one extra and assign number of problems to each TA
for ta in tas_shuffled:
	taDict[ta] = taDict[ta] * problems_each + (1 if remainder > 0 else 0)
	remainder -= 1

i = 0
while remainder > 0:
	taDict[tas_shuffled[i]] += 1
	remainder -= 1
	i = (i + 1) % len(tas_shuffled)

# Sort the dict by values
# This puts the grad students at the bottom of the dict along with those doing one extra
keys = list(taDict.keys())
values = list(taDict.values())
sorted_value_index = np.argsort(values)
sorted_dict = {keys[i]: values[i] for i in sorted_value_index}

next_start = 1
curr_problem = 1
for ta in sorted_dict.keys():
	# Find the last submission they should grade
	end = next_start + sorted_dict[ta] - 1

	# Give them those submissions
	assignment = "Q" + str(curr_problem) + ": " + str(next_start) + "-" + (str(end) if end < submissions else "End")

	# If there is overflow, give them submissions from the next problem
	if end > submissions:
		curr_problem += 1
		assignment += ", Q" + str(curr_problem) + ": 1-" + str(end - submissions)
	elif end == submissions:
		curr_problem += 1

	next_start = (end + 1) % submissions
	print(ta + ": " + assignment)
'''