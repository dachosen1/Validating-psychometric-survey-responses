# Discrete Hidden Markov Model (HMM) with scaling
from __future__ import print_function, division
from builtins import range

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


def random_normalized(d1, d2):
	x = np.random.random((d1, d2))
	return x / x.sum(axis=1, keepdims=True)


class HMM:
	def __init__(self, hidden_states):

		"""
		:param hidden_states: number of hidden states
		"""
		self.hidden_states = hidden_states

	def fit(self, X, max_iter=30):
		np.random.seed(123)

		"""
		Train the HMM model using the Baum-Welch algorithm a specific instance of the expectation-maximization algorithm
		determine V, the vocabulary size.

		This algorithm function assumes that the observation are already in integers ranging from 0 - V-1
		:param data: a jagged array of observed sequences
		:param max_iter: maximum number of iterations
		"""

		V = max(max(x) for x in X) + 1
		N = len(X)

		self.initial_state_distribution = np.ones(self.hidden_states) / self.hidden_states
		self.state_transition_matrix = random_normalized(self.hidden_states, self.hidden_states)
		self.output_distribution = random_normalized(self.hidden_states, V)

		t0 = datetime.now()

		costs = []
		for it in range(max_iter):
			if it % 10 == 0:
				print("iteration:", it)
			alphas = []
			betas = []
			scales = []
			logP = np.zeros(N)
			for n in range(N):
				x = X[n]
				T = len(x)
				scale = np.zeros(T)
				alpha = np.zeros((T, self.hidden_states))
				alpha[0] = self.initial_state_distribution * self.output_distribution[:, x[0]]
				scale[0] = alpha[0].sum()
				alpha[0] /= scale[0]
				for t in range(1, T):
					alpha_t_prime = alpha[t - 1].dot(self.state_transition_matrix) * self.output_distribution[:, x[t]]
					scale[t] = alpha_t_prime.sum()
					alpha[t] = alpha_t_prime / scale[t]
				logP[n] = np.log(scale).sum()
				alphas.append(alpha)
				scales.append(scale)

				beta = np.zeros((T, self.hidden_states))
				beta[-1] = 1
				for t in range(T - 2, -1, -1):
					beta[t] = self.state_transition_matrix.dot(self.output_distribution[:, x[t + 1]] * beta[t + 1]) / scale[t + 1]
				betas.append(beta)

			cost = np.sum(logP)
			costs.append(cost)

			# now re-estimate the initial state distribution, transition matrix, and output distribution
			self.initial_state_distribution = np.sum((alphas[n][0] * betas[n][0]) for n in range(N)) / N

			den1 = np.zeros((self.hidden_states, 1))
			den2 = np.zeros((self.hidden_states, 1))
			a_num = np.zeros((self.hidden_states, self.hidden_states))
			b_num = np.zeros((self.hidden_states, V))
			for n in range(N):
				x = X[n]
				T = len(x)
				den1 += (alphas[n][:-1] * betas[n][:-1]).sum(axis=0, keepdims=True).T
				den2 += (alphas[n] * betas[n]).sum(axis=0, keepdims=True).T

				# numerator for A
				# a_num_n = np.zeros((self.M, self.M))
				for i in range(self.hidden_states):
					for j in range(self.hidden_states):
						for t in range(T - 1):
							a_num[i, j] += alphas[n][t, i] * betas[n][t + 1, j] * self.state_transition_matrix[i, j] * self.output_distribution[j, x[t + 1]] / \
							               scales[n][t + 1]

				for i in range(self.hidden_states):
					for t in range(T):
						b_num[i, x[t]] += alphas[n][t, i] * betas[n][t, i]
			self.state_transition_matrix = a_num / den1
			self.output_distribution = b_num / den2

		print("Fit duration:", (datetime.now() - t0))
		plt.plot(cost)
		plt.show()

	def log_likelihood(self, x):
		""""
		returns log P(x | model) using the forward part of the forward-backward algorithm
		"""
		T = len(x)
		scale = np.zeros(T)
		alpha = np.zeros((T, self.hidden_states))
		alpha[0] = self.initial_state_distribution * self.output_distribution[:, x[0]]
		scale[0] = alpha[0].sum()
		alpha[0] /= scale[0]
		for t in range(1, T):
			alpha_t_prime = alpha[t - 1].dot(self.state_transition_matrix) * self.output_distribution[:, x[t]]
			scale[t] = alpha_t_prime.sum()
			alpha[t] = alpha_t_prime / scale[t]
		return np.log(scale).sum()

	def get_state_sequence(self, x):
		""""
		Returns the most likely state sequence given observed sequence x using the Viterbi algorithm
		"""
		T = len(x)
		delta = np.zeros((T, self.hidden_states))
		psi = np.zeros((T, self.hidden_states))
		delta[0] = np.log(self.initial_state_distribution) + np.log(self.output_distribution[:, x[0]])
		for t in range(1, T):
			for j in range(self.hidden_states):
				delta[t, j] = np.max(delta[t - 1] + np.log(self.state_transition_matrix[:, j])) + np.log(self.output_distribution[j, x[t]])
				psi[t, j] = np.argmax(delta[t - 1] + np.log(self.state_transition_matrix[:, j]))

		# backtrack
		states = np.zeros(T, dtype=np.int32)
		states[T - 1] = np.argmax(delta[T - 1])
		for t in range(T - 2, -1, -1):
			states[t] = psi[t + 1, states[t + 1]]
		return states

# Source
# https://deeplearningcourses.com/c/unsupervised-machine-learning-hidden-markov-models-in-python
# https://udemy.com/unsupervised-machine-learning-hidden-markov-models-in-python
# http://lazyprogrammer.me

