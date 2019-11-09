from __future__ import print_function, division

from builtins import range
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np


def random_normalized(d1, d2):
    x = np.random.random((d1, d2))
    return x / x.sum(axis = 1, keepdims = True)


class HMM:
    def __init__(self, hidden_states):
        """
        :param hidden_states: number of hidden states
        """
        self.hidden_states = hidden_states

    def fit(self, data, max_iter = 30):

        """
        Train the HMM model using the Baum-Welch algorithm a specific instance of the expectation-maximization algorithm
        determine V, the vocabulary size.

        This algorithm function assumes that the observation are already in integers ranging from 0 - V-1
        :param data: a jagged array of observed sequences
        :param max_iter: maximum number of iterations
        """
        t0 = datetime.now()
        np.random.seed(987)

        V = max(max(x) for x in data) + 1
        n_row_data = len(data)

        self.states_distribution = np.ones(self.hidden_states) / self.hidden_states
        self.transition_matrix = random_normalized(self.hidden_states, self.hidden_states)
        self.output_distribution = random_normalized(self.hidden_states, V)  

        costs = []
        for it in range(max_iter):
            if it % 10 == 0:
                print("it:", it)
            alphas = []
            betas = []
            P = np.zeros(n_row_data)
            for n in range(n_row_data):
                x = data[n]
                T = len(x)
                alpha = np.zeros((T, self.hidden_states))
                alpha[0] = self.states_distribution * self.output_distribution[:, x[0]]
                for t in range(1, T):
                    tmp1 = alpha[t - 1].dot(self.transition_matrix) * self.output_distribution[:, x[t]]
                    alpha[t] = tmp1
                P[n] = alpha[-1].sum()
                alphas.append(alpha)

                beta = np.zeros((T, self.hidden_states))
                beta[-1] = 1
                for t in range(T - 2, -1, -1):
                    beta[t] = self.transition_matrix.dot(self.output_distribution[:, x[t + 1]] * beta[t + 1])
                betas.append(beta)

            assert (np.all(P > 0))
            cost = np.sum(np.log(P))
            costs.append(cost)

            # now re-estimate pi, A, B
            self.states_distribution = np.sum(
                (alphas[n][0] * betas[n][0]) / P[n] for n in range(n_row_data)) / n_row_data

            den1 = np.zeros((self.hidden_states, 1))
            den2 = np.zeros((self.hidden_states, 1))
            a_num = 0
            b_num = 0
            for n in range(n_row_data):
                x = data[n]
                T = len(x)
                den1 += (alphas[n][:-1] * betas[n][:-1]).sum(axis = 0, keepdims = True).T / P[n]
                den2 += (alphas[n] * betas[n]).sum(axis = 0, keepdims = True).T / P[n]

                a_num_n = np.zeros((self.hidden_states, self.hidden_states))
                for i in range(self.hidden_states):
                    for j in range(self.hidden_states):
                        for t in range(T - 1):
                            a_num_n[i, j] += alphas[n][t, i] * self.transition_matrix[i, j] * self.output_distribution[
                                j, x[t + 1]] * betas[n][t + 1, j]
                a_num += a_num_n / P[n]

                b_num_n2 = np.zeros((self.hidden_states, V))
                for i in range(self.hidden_states):
                    for t in range(T):
                        b_num_n2[i, x[t]] += alphas[n][t, i] * betas[n][t, i]
                b_num += b_num_n2 / P[n]
            self.transition_matrix = a_num / den1
            self.output_distribution = b_num / den2
        # print("A:", self.A)
        # print("B:", self.B)
        # print("pi:", self.pi)

        print("Fit duration:", (datetime.now() - t0))

        plt.plot(costs)
        plt.show()

    def likelihood(self, x):
        """
        :param x: observable sequence
        :return: log P(x | model) using the forward part of the forward-backward algorithm
        """

        T = len(x)
        alpha = np.zeros((T, self.hidden_states))
        alpha[0] = self.states_distribution * self.output_distribution[:, x[0]]
        for t in range(1, T):
            alpha[t] = alpha[t - 1].dot(self.transition_matrix) * self.output_distribution[:, x[t]]
        return alpha[-1].sum()

    def likelihood_multi(self, X):
        return np.array([self.likelihood(x) for x in X])

    def log_likelihood_multi(self, X):
        return np.log(self.likelihood_multi(X))

    def get_state_sequence(self, x):
        """
        returns the most likely state sequence given observed sequence x using the Viterbi algorithm
        """

        T = len(x)
        delta = np.zeros((T, self.hidden_states))
        psi = np.zeros((T, self.hidden_states))
        delta[0] = self.states_distribution * self.output_distribution[:, x[0]]
        for t in range(1, T):
            for j in range(self.hidden_states):
                delta[t, j] = np.max(delta[t - 1] * self.transition_matrix[:, j]) * self.output_distribution[j, x[t]]
                psi[t, j] = np.argmax(delta[t - 1] * self.transition_matrix[:, j])

        # backtrack
        states = np.zeros(T, dtype = np.int32)
        states[T - 1] = np.argmax(delta[T - 1])
        for t in range(T - 2, -1, -1):
            states[t] = psi[t + 1, states[t + 1]]
        return states

# source:
# Modified for the purpose of dotin
# https://deeplearningcourses.com/c/unsupervised-machine-learning-hidden-markov-models-in-python
# https://udemy.com/unsupervised-machine-learning-hidden-markov-models-in-python
# http://lazyprogrammer.me
# Discrete Hidden Markov Model (HMM)