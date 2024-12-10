import random
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

class Genetic_Circuit:
    def __init__(self, circuit_dict, Initial_Concentrations, inducer_dict, inducer_times):
        self.circuit_dict = circuit_dict
        self.Initial_Concentrations = Initial_Concentrations
        self.inducer_dict = inducer_dict
        self.inducer_times = inducer_times  # Dictionary with start times for each inducer
        self.simulate_data = []
        self.time_data = []

    def reset(self):
        self.circuit_dict = []
        self.Initial_Concentrations = []
        self.simulate_data = []
        self.time_data = []

    def simulate(self, time, dt, mode):

        # has no entry
        if self.Initial_Concentrations == []:

            self.simulate_data = [0]

            return self.simulate_data


        t = 0
        mRNA = self.Initial_Concentrations[:]
        self.simulate_data = [[] for _ in range(len(self.Initial_Concentrations))]
        self.time_data = [t]

        while t < time:
            rates = []  # List of reaction rates for stochastic simulation

            for gene in range(1, len(self.circuit_dict) + 1):
                change_coef = 1

                # Calculate effect of activators and repressors on each gene
                for influencer_gene in range(1, len(self.circuit_dict) + 1):
                    if gene in self.circuit_dict[str(influencer_gene)][0]:  # Activator
                        change_coef *= self.activator_function(gene, mRNA[influencer_gene - 1], influencer_gene)
                    if gene in self.circuit_dict[str(influencer_gene)][1]:  # Repressor
                        change_coef *= self.repressor_function(gene, mRNA[influencer_gene - 1], influencer_gene)

                # Apply effects of inducers if current time >= inducer start time
                for inducer, (activates, act_coefs, ton) in self.inducer_dict.items():

                    if t >= ton: #self.inducer_times.get(inducer, 1):  # Check inducer start time
                        if gene in activates:
                            change_coef *= self.inducer_effect(gene, act_coefs)
                    else:
                        if gene in activates:
                            change_coef = 0

                prod_const = self.circuit_dict[str(gene)][4]
                decay_const = self.circuit_dict[str(gene)][5]

                if mode == "deterministic":

                    dmRNA = change_coef * prod_const - decay_const * mRNA[gene - 1]
                    mRNA[gene - 1] += dmRNA * dt

                elif mode == "stochastic":
                    prod_rate = change_coef * prod_const
                    decay_rate = decay_const * mRNA[gene - 1]
                    print(prod_rate)
                    rates.append((prod_rate, gene, "production"))
                    rates.append((decay_rate, gene, "decay"))

            if mode == "stochastic":
                total_rate = sum(abs(rate[0]) for rate in rates)
                if total_rate == 0:
                    break

                dt = np.random.exponential(1 / total_rate)
                chosen_reaction = random.choices(rates, weights=[abs(rate[0]) for rate in rates])[0]

                if chosen_reaction[2] == "production":
                    mRNA[chosen_reaction[1] - 1] += 1
                elif chosen_reaction[2] == "decay" and mRNA[chosen_reaction[1] - 1] > 0:
                    mRNA[chosen_reaction[1] - 1] -= 1

            t += dt
            for i in range(len(self.simulate_data)):
                self.simulate_data[i].append(mRNA[i])

            self.time_data.append(t)

        if len(self.time_data) > len(self.simulate_data[0]):
            self.time_data.pop()

        return self.simulate_data

    def repressor_function(self, gene, concentration, influencer_gene):
        try:
            repress_coefficiant_position = self.circuit_dict.get(str(influencer_gene))[1].index(gene)
            repress_coefficiant = self.circuit_dict.get(str(gene))[3][repress_coefficiant_position]
            return repress_coefficiant**5 / (repress_coefficiant**5 + concentration**5)
        except IndexError:
            return 1

    def activator_function(self, gene, concentration, influencer_gene):
        try:
            activate_coefficiant_position = self.circuit_dict.get(str(influencer_gene))[0].index(gene)
            activate_coefficiant = self.circuit_dict.get(str(gene))[2][activate_coefficiant_position]
            return concentration ** 5 / (activate_coefficiant ** 5 + concentration ** 5)
        except IndexError:
            return 1

    def inducer_effect(self, gene, act_coefs):
        try:
            activate_coefficiant_position = act_coefs.index(gene)
            activate_coefficiant = act_coefs[activate_coefficiant_position]
            return activate_coefficiant ** 5 / (activate_coefficiant ** 5 + 1)  # Inducer is constant
        except (IndexError, ValueError):
            return 1

    def plot_circuit(self):
        if not self.simulate_data or not self.time_data:
            plt.plot([0], [0])

            plt.title("Genetic Network Simulation Results")
            plt.ylabel("Fluorescence (Arbitrary Units)")
            plt.xlabel("Time (Arbitrary Units)")
            plt.legend()
            plt.grid(True)

            plt.savefig("plot.png")

            self.reset()
            plt.clf()
            return

        rfp_data = []
        gfp_data = []
        bfp_data = []

        for gene in range(0, len(self.simulate_data)):
            if self.circuit_dict.get(str(gene + 1))[6] == 1:
                rfp_data.append(self.simulate_data[gene])
            elif self.circuit_dict.get(str(gene + 1))[6] == 2:
                gfp_data.append(self.simulate_data[gene])
            elif self.circuit_dict.get(str(gene + 1))[6] == 3:
                bfp_data.append(self.simulate_data[gene])

        # Sum the lists element-wise
        rfp_added = [sum(values) for values in zip(*rfp_data)] if rfp_data else []
        gfp_added = [sum(values) for values in zip(*gfp_data)] if gfp_data else []
        bfp_added = [sum(values) for values in zip(*bfp_data)] if bfp_data else []

        # Plot only if the data is not empty
        if rfp_added:
            plt.plot(self.time_data, rfp_added, label="RFP", color="red")

        if gfp_added:
            plt.plot(self.time_data, gfp_added, label="GFP", color='green')

        if bfp_added:
            plt.plot(self.time_data, bfp_added, label="BFP", color='blue')

        plt.title("Genetic Network Simulation Results")
        plt.ylabel("Fluorescence (Arbitrary Units)")
        plt.xlabel("Time (Arbitrary Units)")
        plt.legend()
        plt.grid(True)

        plt.savefig("plot.png")

        self.reset()
        plt.clf()



'''
v1.0
gene_circuit_dict = {
   # gene : [activates], [represses], [activator coefs], [repressor coefs], prod_const, decay_const]
   "1": [[0], [2], [1], [1], 0.204, 0.01],
   "2": [[0], [3], [1], [1], 0.21, 0.009],
   "3": [[0], [4], [1], [1], 0.205, 0.01],
   "4": [[0], [5], [1], [1], 0.19, 0.01],
   "5": [[0], [1], [1], [1], 0.201, 0.0095],
}

Initial_concentrations = [0.1, 0.1, 0.1, 0.1, 0.1]
time = 2000
dt = 1

circuit = Genetic_Circuit(gene_circuit_dict, Initial_concentrations)
circuit.simulate(time, dt, "deterministic")
circuit.plot_circuit()
'''

'''
v1.1
added const expression term for expressed genes (need no activator, expressed as constant rate)

gene_circuit_dict = {
   # gene : [activates], [represses], [activator coefs], [repressor coefs], prod_const, decay_const, auto_expression level]
   "1": [[0], [2], [1], [1], 0.204, 0.01, 0],
   "2": [[0], [3], [1], [1], 0.21, 0.009, 0],
   "3": [[0], [4], [1], [1], 0.205, 0.01, 0],
   "4": [[0], [5], [1], [1], 0.19, 0.01, 0],
   "5": [[0], [1], [1], [1], 0.201, 0.0095, 0],
}

Initial_concentrations = [0.1, 0.1, 0.1, 0.1, 0.1]
time = 2000
dt = 1

circuit = Genetic_Circuit(gene_circuit_dict, Initial_concentrations)
circuit.simulate(time, dt, "deterministic")
circuit.plot_circuit()
'''


'''
v1.2
const expression not neccesary, added reporter marking

0 = none
1 = rfp
2 = gfp
3 = bfp

gene_circuit_dict = {
   # gene : [activates], [represses], [activator coefs], [repressor coefs], prod_const, decay_const, reporter marking]
   "1": [[0], [2], [1], [1], 0.204, 0.01, 0],
   "2": [[0], [3], [1], [1], 0.21, 0.009, 0],
   "3": [[0], [4], [1], [1], 0.205, 0.01, 0],
   "4": [[0], [5], [1], [1], 0.19, 0.01, 0],
   "5": [[0], [1], [1], [1], 0.201, 0.0095, 0],
}

Initial_concentrations = [0.1, 0.1, 0.1, 0.1, 0.1]
time = 2000
dt = 1

circuit = Genetic_Circuit(gene_circuit_dict, Initial_concentrations)
circuit.simulate(time, dt, "deterministic")
circuit.plot_circuit()
'''
