import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

df = pd.read_csv("System usability scale(SUS).csv")
df.drop(["Tidsstempel", "Participant ID"], axis='columns', inplace=True)

participantAmount = 10

susScew = ["positiv",
           "negativ",
           "positiv",
           "negativ",
           "positiv",
           "negativ",
           "positiv",
           "negativ",
           "positiv",
           "negativ"]

def Average(lst):
    return sum(lst) / len(lst)

def calculateStd(data):
    avg = Average(data)
    disSum = 0

    for point in data:
        disSum += math.pow(abs(point - avg), 2)

    return math.sqrt(disSum/len(data))

def mapLikert(row):
    mulNumber = 2.5
    mappedValues = []
    for index1, value1 in enumerate(row):
        if susScew[index1] == "negativ":
            newValue = (int(row[index1]) - 5) * mulNumber
        else:
            newValue = (int(row[index1]) - 1) * mulNumber

        mappedValues.append(abs(newValue))

    return sum(mappedValues)

mappedSUS = []

for index, row in df.iterrows():
    mappedSUS.append(mapLikert(row))

print(mappedSUS)
print(Average(mappedSUS))
print(calculateStd(mappedSUS))
print(max(mappedSUS), min(mappedSUS))

fig = plt.figure()
plt.bar(range(1, participantAmount+1), mappedSUS)

plt.xlabel("Participant")
plt.ylabel("SUS Score")
plt.title("Result from the System usability scale")
plt.show()

