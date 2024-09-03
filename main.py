from flask import Flask, render_template, g
from datetime import datetime, timedelta
import sqlite3
import math
import numpy as np
import matplotlib.pyplot as plt
import random
import cpp_function


# Helper function that creates date_range so we can iterate
# Through all days we have collected data from
def date_range(start_date_str, end_date_str):
    # Convert start and end date strings to datetime objects
    start_date = datetime.strptime(start_date_str, "%Y.%m.%d")
    end_date = datetime.strptime(end_date_str, "%Y.%m.%d")

    # Iterate over the date range
    current_date = start_date
    while current_date <= end_date:
        # Format current date in "YYYY.MM.DD" format
        yield current_date.strftime("%Y.%m.%d")
        # Move to the next date
        current_date += timedelta(days=1)

# Finds optimal size of universum (how many horoscopes are there on diva.sk webpage)
# given: m - number of distinct horoscopes we have seen
#        n - number of fetches from their webpage
#
# this function is now outdated
# we rewrote it in c++ code in cpp_class.cc file
def find_optimal_universum_size(m, n):
    best_k = -1
    best = float("-inf")
    for k in range(m, 10000):

        # use this if you want improved numerical stability at cost of speed
        """
        log_comb = 0
        for i in range(m):
            log_comb += math.log(k - i) - math.log(max(i, 1))
        curr = log_comb - n * math.log(k)
        """

        # use this if you want faster but less stable calculation
        curr = math.log(math.comb(k, m)) - n * math.log(k)

        # do update if better k was found
        if best < curr:
            best_k = k
            best = curr
    return best_k

# connect to a database
connection = sqlite3.connect("horoscopes.db")
# create a "cursor" for working with the database
cursor = connection.cursor()

cursor.execute("""
        SELECT MIN(h_date) AS min_date, MAX(h_date) AS max_date
        FROM horoscopes;
        """
        )
min_date, max_date = cursor.fetchone()
original_y_axis = []
optimal_universum_size_finder = cpp_function.Find_optimal_universum_size()

print("Computing results... for collected data from https://diva.aktuality.sk/horoskopy/")

for date_str in date_range(min_date, max_date):
    cursor.execute("""
        SELECT COUNT(DISTINCT h_text) AS m, COUNT(h_id) AS n
        FROM horoscopes
        WHERE h_date <= ?;
        """, [date_str])
    m, n = cursor.fetchone()

    # Finds optimal k - amount of horoscopes in diva.sk webpage for m, n
    best_k = optimal_universum_size_finder.compute(m,n)


    # We want to add it into graph only if the optimum is not in infinity
    # (this happens if we do not have any horoscope text collisions yet)

    # From previous tests we concluded, that if the predicted size of
    # the horoscopes is greather than 3000, then most likely
    # the current prediction is infinite size
    # (this happens when we have no collisions yet)

    # When it comes to a drawing of a graph,
    # it looks better if we just draw there 0 instead of infinity
    if best_k < 3000:
        original_y_axis.append(best_k)
    else:
        # we know it is infinity but graph is nicer if it is zero
        original_y_axis.append(0)

original_x_axis = [i for i in range(len(original_y_axis))]

plt.xlabel("Days")
plt.ylabel("Horoscope amount prediction")
plt.title("Prediction of horoscopes amount based on collected data (timeline)")
plt.plot(original_x_axis, original_y_axis)

plt.savefig("/home/z/zubcak2/project/collected_data_universum_size_prediction.png", dpi=500)

plt.grid(True)
#plt.show()
plt.figure()


# Monte-Carlo simulation comparison:
# now we add some different functions,
# each representing how the graph should "look like"
# if we have N horoscopes in diva.sk horoscopes database, assuming no were added
# (N is the universum size)
#
# for each of them we do 30 repeats and mean of them,
# to get more reperesentative data


N_vals = [1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100]
print("Running Monte-Carlo simulations...")
plt.xlabel("Days")
plt.ylabel("Horoscope amount prediction")
plt.title("Comparison of our data vs random samples from universum of given size")
plt.plot(original_x_axis, original_y_axis, label="collected data")

for N in N_vals:
    print("... for N = " + str(N))
    y_axis_matrix = []
    rand_seed = [random.randint(0, N) for _ in range(1000000)]
    for j in range(30):
        y_axis_j = []
        for i in range(len(original_x_axis)):
            n = (i+1) * 12
            m = len(set(rand_seed[:(i+1)*12]))

            # Finds optimal k - amount of horoscopes in diva.sk webpage for m, n
            best_k = optimal_universum_size_finder.compute(m, n)
            if best_k < 3000:
                y_axis_j.append(best_k)
            else:
                y_axis_j.append(0)
        y_axis_matrix.append(y_axis_j)
        rand_seed = rand_seed[12*(len(original_x_axis) + 1):]
    y_axis_mean = np.mean(np.array(y_axis_matrix), axis=0)
    tmp_x_axis = [i for i in range(len(y_axis_mean))]
    label = "N: " + str(N)
    plt.plot(tmp_x_axis, y_axis_mean, label=label)


plt.legend()
plt.savefig("/home/z/zubcak2/project/monte-carlo_predictions.png", dpi=500)

plt.grid(True)
#plt.show()
plt.figure()


# In the end we will compute dispersion for vales N= 1500, 1750, 2000
# in our Monte-Carlo simulation
# (10 random runs for each value N)

N_vals = [1500, 1750, 2000]
for N in N_vals:
    rand_seed = [random.randint(0, N) for _ in range(1000000)]
    print("Computing dispersion graph... for N = " + str(N))
    for j in range(10):
        y_axis = []
        for i in range(len(original_x_axis)):
            n = (i+1) * 12
            m = len(set(rand_seed[:(i+1)*12]))

            # Finds optimal k - amount of horoscopes in diva.sk webpage for m, n
            best_k = optimal_universum_size_finder.compute(m, n)
            if best_k < 3000:
                y_axis.append(best_k)
            else:
                y_axis.append(0)
        x_axis = [i for i in range(len(y_axis))]
        rand_seed = rand_seed[12*(len(x_axis) + 1):]
        if j ==0:
            label = "simulation data"
            plt.plot(x_axis, y_axis, label=label, color="grey")
        else:
            plt.plot(x_axis, y_axis, color="grey")


    plt.plot(original_x_axis, original_y_axis, label="collected data", color="red")
    plt.xlabel("Days")
    plt.ylabel("Horoscope amount prediction")
    plt.title("Dispersion graph for N =" + str(N))
    plt.legend()

    plt.savefig("/home/z/zubcak2/project/monte-carlo_dispersion" + str(N) + ".png", dpi=500)

    plt.grid(True)
    #plt.show()
    plt.figure()
