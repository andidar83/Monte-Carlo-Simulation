# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 22:59:36 2020

@author: Andidar83
"""

import numpy as np
import statistics

import matplotlib.pyplot as plt

data1= []

def simulation(low, most, high, trial):
    mu = (low+most+high)/3
    sigma = (high-low)/6
    r = np.random.normal(mu, sigma, trial)
    if min(r) < 0:
        r = no_zero(r)
    mode = most
    count, bins1, ignored = plt.hist(r, 30, density=True)
    data1.append(r)
    pdf = 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins1 - mu)**2 / (2 * sigma**2) )
    
    return {
        "res": r,
        "val_min": round(min(r), 2),
        "val_max": round(max(r), 2),
        "mean": round(np.mean(r), 2),
        "mode": round(mode, 2),
        "p50": round(np.percentile(r, 50), 2),
        "p1": round(np.percentile(r, 1), 2),
        "p10": round(np.percentile(r, 10), 2),
        "p15": round(np.percentile(r, 15), 2),
        "p85": round(np.percentile(r, 85), 2),
        "p90": round(np.percentile(r, 90), 2),
        "p99": round(np.percentile(r, 99), 2),
        "pdf": [bins1, pdf],
        }


def no_zero(array):
    rbaru = []
    for i in array:
        if i < 0:
            rbaru.append(0)
        else:
            rbaru.append(i)
    return np.array(rbaru)

porosity1 = simulation(5, 25, 45, trial=20000)
oilsat1 = simulation(50, 80, 90, trial=20000)
NtoG1 = simulation(15, 35, 55, trial=20000)
test21 = simulation(0, 0.9, 1, trial=20000)
test31 = simulation(10, 20, 30, trial=20000)

porosity = data1[0]
oilsat = data1[1]
NtoG = data1[2]
test2 = data1[3]
test3 = data1[4]

#KALKULASI RESOURCE
resource = []
resource_round = []


for i in range(len(porosity)):
    mult = porosity[i]*oilsat[i]*NtoG[i]*test2[i]/test3[i]
    resource.append(mult)
    

for i in range(len(resource)):
    w = round(resource[i],1)
    resource_round.append(w)
if min(resource) < 0:
    resource = no_zero(resource)
if min(resource_round) < 0:
    resource_round = no_zero(resource_round)

#########################################################################
mean_resource = round(np.mean(resource_round), 2)
min_resource = round(min(resource_round),2)
max_resource = round(max(resource_round),2)

def find_max_mode(list1):
    list_table = statistics._counts(list1)
    len_table = len(list_table)

    if len_table == 1:
        max_mode = statistics.mode(list1)
    else:
        new_list = []
        for i in range(len_table):
            new_list.append(list_table[i][0])
        max_mode = max(new_list) # use the max value here
    return max_mode

mode_resource = find_max_mode(resource_round)
p50_resource = round(np.percentile(resource_round, 50), 2)
p10_resource =  round(np.percentile(resource_round, 10), 2)
p90_resource =  round(np.percentile(resource_round, 90), 2)
sigma_resource = (min_resource+mode_resource+max_resource)/3
mu_resource = (max_resource-min_resource)/6
print(p10_resource)



fig1= plt.figure()
ax1 = fig1.add_subplot(111)

#ax1.hist(resource, bins= 30, density = True)
count, bins, ignored = ax1.hist(resource_round, 30, density = True)
pdf_resource = 1/(sigma_resource * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu_resource)**2 / (2 * sigma_resource**2) )
print(pdf_resource)
ax1.plot(bins, pdf_resource)
xp10=np.linspace(p10_resource,p10_resource,len(pdf_resource))
xp90=np.linspace(p90_resource,p90_resource,len(pdf_resource))
xp50=np.linspace(p50_resource,p50_resource,len(pdf_resource))
ax1.plot(xp10,pdf_resource,label="P10")
ax1.plot(xp90,pdf_resource,label="P90")
ax1.plot(xp50,pdf_resource,label="P50")
"""
ax1.xlabel("resource")
ax1.ylabel("Probability")
ax1.title("Result and PDF")
ax1.legend()
######################################################################
"""


#resource = resource * 6.2898 / 1000000





###################################################################################
#KALKULASI SENSITIVITAS
def sensitivity_calculation(data):
    val_min = data["p10"]
    val_max = data["p90"]
    mean = data["mean"]
    median = data["p50"]
   
    sen_min = (mean_resource/mean*val_min)-mean_resource
    sen_max = (mean_resource/mean*val_max)-mean_resource
    value = np.absolute(sen_min)+np.absolute(sen_max)
   
    return {
        "sen_min": sen_min,
        "sen_max": sen_max,
        "value": value
        }

sensi_poros = sensitivity_calculation(porosity1)
sensi_oilsat = sensitivity_calculation(oilsat1)
sensi_NtoG = sensitivity_calculation(NtoG1)
sensi_test2 = sensitivity_calculation(test21)
sensi_test3 = sensitivity_calculation(test31)


values = [round(sensi_poros["value"],2),round(sensi_oilsat["value"],2),round(sensi_NtoG["value"],2),
          round(sensi_test2["value"],2),round(sensi_test3["value"],2)]
lows = []
#print(values)
base = 0

for i in range(len(values)):
    lows1 = base - values[i]/2
    lows.append(lows1)

#PLOTTING TORNADO
variables = [
    'Porosity',
    'Oil Saturation',
    'N/G',
    'FVF',
    'EUR',
]
    
# The actual drawing part

# The y position for each variable
plt.figure()
ys = range(len(values))[::-1]  # top to bottom

# Plot the bars, one by one
for y, low, value in zip(ys, lows, values):
    # The width of the 'low' and 'high' pieces
    low_width = base - low
    high_width = low + value - base

    # Each bar is a "broken" horizontal bar chart
    plt.broken_barh(
        [(low, low_width), (base, high_width)],
        (y - 0.4, 0.8),
        facecolors=['white', 'white'],  # Try different colors if you like
        edgecolors=['black', 'black'],
        linewidth=1,
    )

    # Display the value as text. It should be positioned in the center of
    # the 'high' bar, except if there isn't any room there, then it should be
    # next to bar instead.
    x = base + high_width / 2
    if x <= base + 50:
        x = base + high_width + 50
    plt.text(x, y, str(value), va='center', ha='center')

# Draw a vertical line down the middle
plt.axvline(base, color='black')

# Position the x-axis on the top, hide all the other spines (=axis lines)
axes = plt.gca()  # (gca = get current axes)
axes.spines['left'].set_visible(False)
axes.spines['right'].set_visible(False)
axes.spines['bottom'].set_visible(False)
axes.xaxis.set_ticks_position('top')

# Make the y-axis display the variables
plt.yticks(ys, variables)

# Set the portion of the x- and y-axes to show
plt.xlim(base - 1500, base + 1500)
plt.ylim(-1, len(variables))



