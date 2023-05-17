from scipy import stats
import numpy as np
import pandas as pd
import math
import statsmodels
import matplotlib.pyplot as plt
import glob
import os
import pathlib

df = pd.read_csv("System usability scale(SUS).csv")
df.drop(["Tidsstempel","Participant ID"], axis='columns', inplace=True)

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

def calculateMean(data):
    averageData = []
    tData = np.asarray(data).T.tolist()
    for list in tData:
        avg = Average(list)
        averageData.append(round(avg, 2))
    return averageData

def calculateStd(data):
    tempList = []
    tData = np.asarray(data).T.tolist()
    for list in tData:
        tempList.append(round(math.sqrt(Average(list)), 2))
    return tempList

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
print(sum(mappedSUS)/10)

fig = plt.figure()
plt.bar(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], mappedSUS)

plt.xlabel("Participant")
plt.ylabel("SUS Score")
plt.title("Result from the System usability scale")
plt.show()

