from __future__ import print_function, division
from builtins import range

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


def random_normalized(d1, d2):
    x = np.random.random((d1, d2))
    return x / x.sum(axis = 1, keepdims = True)


class HMM:
    def __init__(self, M):
        """
        :param M: number of hidden states
        """
        self.M = M

    def fit(self, X, max_iter = 30):

        """
        Train the HMM model using the Baum-Welch algorithm a specific instance of the expectation-maximization algorithm
        determine V, the vocabulary size.

        This algorithm function assumes that the observation are already in integers ranging from 0 - V-1
        :param X: a jagged array of observed sequences
        :param max_iter: maximum number of iterations
        """
        t0 = datetime.now()
        np.random.seed(123)

        V = max(max(x) for x in X) + 1
        N = len(X)

        self.pi = np.ones(self.M) / self.M  # initial state distribution
        self.A = random_normalized(self.M, self.M)  # state transition matrix
        self.B = random_normalized(self.M, V)  # output distribution

        print("initial A:", self.A)
        print("initial B:", self.B)

        costs = []
        for it in range(max_iter):
            if it % 10 == 0:
                print("it:", it)
            alphas = []
            betas = []
            P = np.zeros(N)
            for n in range(N):
                x = X[n]
                T = len(x)
                alpha = np.zeros((T, self.M))
                alpha[0] = self.pi * self.B[:, x[0]]
                for t in range(1, T):
                    tmp1 = alpha[t - 1].dot(self.A) * self.B[:, x[t]]
                    alpha[t] = tmp1
                P[n] = alpha[-1].sum()
                alphas.append(alpha)

                beta = np.zeros((T, self.M))
                beta[-1] = 1
                for t in range(T - 2, -1, -1):
                    beta[t] = self.A.dot(self.B[:, x[t + 1]] * beta[t + 1])
                betas.append(beta)

            assert (np.all(P > 0))
            cost = np.sum(np.log(P))
            costs.append(cost)

            # now re-estimate pi, A, B
            self.pi = np.sum((alphas[n][0] * betas[n][0]) / P[n] for n in range(N)) / N

            den1 = np.zeros((self.M, 1))
            den2 = np.zeros((self.M, 1))
            a_num = 0
            b_num = 0
            for n in range(N):
                x = X[n]
                T = len(x)
                den1 += (alphas[n][:-1] * betas[n][:-1]).sum(axis = 0, keepdims = True).T / P[n]
                den2 += (alphas[n] * betas[n]).sum(axis = 0, keepdims = True).T / P[n]

                a_num_n = np.zeros((self.M, self.M))
                for i in range(self.M):
                    for j in range(self.M):
                        for t in range(T - 1):
                            a_num_n[i, j] += alphas[n][t, i] * self.A[i, j] * self.B[j, x[t + 1]] * betas[n][t + 1, j]
                a_num += a_num_n / P[n]

                b_num_n2 = np.zeros((self.M, V))
                for i in range(self.M):
                    for t in range(T):
                        b_num_n2[i, x[t]] += alphas[n][t, i] * betas[n][t, i]
                b_num += b_num_n2 / P[n]
            self.A = a_num / den1
            self.B = b_num / den2
        print("A:", self.A)
        print("B:", self.B)
        print("pi:", self.pi)

        print("Fit duration:", (datetime.now() - t0))

        plt.plot(costs)
        plt.show()

    def likelihood(self, x):
        """
        :param x: observable sequence
        :return: log P(x | model) using the forward part of the forward-backward algorithm
        """

        T = len(x)
        alpha = np.zeros((T, self.M))
        alpha[0] = self.pi * self.B[:, x[0]]
        for t in range(1, T):
            alpha[t] = alpha[t - 1].dot(self.A) * self.B[:, x[t]]
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
        delta = np.zeros((T, self.M))
        psi = np.zeros((T, self.M))
        delta[0] = self.pi * self.B[:, x[0]]
        for t in range(1, T):
            for j in range(self.M):
                delta[t, j] = np.max(delta[t - 1] * self.A[:, j]) * self.B[j, x[t]]
                psi[t, j] = np.argmax(delta[t - 1] * self.A[:, j])

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