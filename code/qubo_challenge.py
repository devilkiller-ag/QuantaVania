import pygame,sys
from pygame.image import load as loadImage

from settings import *
from support import *
from dwave.system import DWaveCliqueSampler
import dimod
import pyqubo
import numpy as np
from pyqubo import Array, Placeholder, Constraint
import matplotlib.pyplot as plt
import networkx as nx
import neal
import csv
import os
import math

class SolveQubo:
    def __init__(self, file_name, token_given=False, Token = None):
        self.file_name = file_name
        self.Token=Token
        self.token_given=token_given


    def run(self, relaxation_parameter, num_cities=10):
        node_matrix, distance_matrix = parse_tsp_file(self.file_name)
        best_sample, num_broken,  P_f, E_avg, E_std, E_min, cities = solve_for_instances(node_matrix, relaxation_parameter,num_cities_in_a_instance=10)

        plot_city(cities)
        if num_broken == 0:
            plot_city(cities, best_sample)
        return P_f, E_avg

        
def parse_tsp_file(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    node_coord_section = False
    node_matrix = []
    distance_matrix = None

    for line in lines:
        if line.startswith("NODE_COORD_SECTION"):
            node_coord_section = True
            continue
        elif line.startswith("EOF"):
            break

        if node_coord_section:
            node_info = line.split()
            node_id = int(node_info[0])
            # x_coord = int(float(node_info[1]))  # Convert to int
            # y_coord = int(float(node_info[2]))  # Convert to int
            x_coord = float(node_info[1])  # Convert to int
            y_coord = float(node_info[2])  # Convert to int

            node_matrix.append([node_id, x_coord, y_coord])

    node_matrix = np.array(node_matrix)

    # Calculate distance matrix (as in the previous version)
    num_nodes = node_matrix.shape[0]
    distance_matrix = np.zeros((num_nodes, num_nodes))
    for i in range(num_nodes):
        for j in range(num_nodes):
            x1, y1 = node_matrix[i, 1], node_matrix[i, 2]
            x2, y2 = node_matrix[j, 1], node_matrix[j, 2]
            distance_matrix[i, j] = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    return node_matrix, distance_matrix

def plot_city(cities, sol=None):
    n_city = len(cities)
    cities_dict = dict(cities)
    G = nx.Graph()
    for city in cities_dict:
        G.add_node(city)
        
    # draw path
    if sol:
        city_order = []
        for i in range(n_city):
            for j in range(n_city):
                if sol.array('c', (i, j)) == 1:
                    city_order.append(j)
        for i in range(n_city):
            city_index1 = city_order[i]
            city_index2 = city_order[(i+1) % n_city]
            G.add_edge(cities[city_index1][0], cities[city_index2][0])

    plt.figure(figsize=(3,3))
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, cities_dict)
    plt.axis("off")
    if sol:
        plt.savefig("solution.png")
    else:
        plt.savefig("problem.png")

def dist(i, j, cities):
    pos_i = cities[i][1]
    pos_j = cities[j][1]
    return np.sqrt((pos_i[0] - pos_j[0])**2 + (pos_i[1] - pos_j[1])**2)

def solve_for_instances(nodes_matrix, relaxation_parameter, Token=None, token_given=False, num_cities_in_a_instance=10):
    cities = [(i,(0,0)) for i in range(num_cities_in_a_instance)]
    n_mat = nodes_matrix.copy()
    for i in range(num_cities_in_a_instance):
        cities[i] = (str(n_mat[i][0]), (n_mat[i][1], n_mat[i][2]))
    ## Prepare binary vector with bit (𝑖,𝑗) representing to visit 𝑗 city at time 𝑖
    n_city = len(cities)
    x = Array.create('c', (n_city, n_city), 'BINARY')
    # print(x)

    ## Constraint not to visit more than two cities at the same time.
    ## equation (6) implemented here
    ## time_const + city_const = H_a
    time_const = 0.0
    for i in range(n_city):
        # If you wrap the hamiltonian by Const(...), this part is recognized as constraint
        time_const += Constraint((sum(x[i, j] for j in range(n_city)) - 1)**2, label="time{}".format(i))

    ## Constraint not to visit the same city more than twice.
    city_const = 0.0
    for j in range(n_city):
        city_const += Constraint((sum(x[i, j] for i in range(n_city)) - 1)**2, label="city{}".format(j))

    distance = 0.0
    for i in range(n_city):
        for j in range(n_city):
            for k in range(n_city):
                d_ij = dist(i, j, cities)
                distance += d_ij * x[k, i] * x[(k+1)%n_city, j]

    A = Placeholder("A")  
    H = distance + A * (time_const + city_const) 
    ## Compile model
    model = H.compile()
    ## Generate QUBO
    feed_dict = {'A': relaxation_parameter} 
    bqm = model.to_bqm(feed_dict=feed_dict)

    if token_given:
        sampler = DWaveCliqueSampler()
    else:
        sampler = neal.SimulatedAnnealingSampler()

    
    bqm = model.to_bqm(feed_dict=feed_dict)
    sampleset = sampler.sample(bqm, num_reads=128, num_sweeps=128)
    decoded_samples = model.decode_sampleset(sampleset, feed_dict=feed_dict)
    best_sample = min(decoded_samples, key=lambda x: x.energy)
    E_min = best_sample.energy
    num_broken = len(best_sample.constraints(only_broken=True))
    infeasible_ctr = 0
    for i in range(128):
        if len(decoded_samples[i].constraints(only_broken=True)) > 0:
            infeasible_ctr += 1
    P_f = (128-infeasible_ctr)/128
        #print(f"P_f for {feed_dict} is {P_f}")


    energies = [0 for i in range(128)]
    for i in range(128):
        energies[i] = decoded_samples[i].energy
    E_avg = sum(energies)/128
    s = 0
    for i in range(128):
        s = s + (E_avg-energies[i])**2
    E_std = math.sqrt((s/128))
    return best_sample, num_broken, P_f, E_avg, E_std, E_min, cities  #returns bestsample, relaxation parameter, Pf, min, mean and std of energies

'''
QuboInstance = SolveQubo(f"challenges/rat195.tsp")
QuboInstance.run(PARAMETER_RANGE["rat195.tsp"][0])
'''