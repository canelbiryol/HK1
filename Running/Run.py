'''
Created on Mar 7, 2018

@author: Michael
'''
'''Trying to get cvxopt/cvxpy to work.'''
import numpy as np
import math

np.random.seed(1)
n = 10
mu = np.abs(np.random.randn(n, 1))
Sigma = np.random.randn(n, n)
Sigma = Sigma.T.dot(Sigma)

from cvxpy import Variable
from cvxpy import Parameter
from cvxpy import quad_form
from cvxpy import Problem
from cvxpy import Maximize
from cvxpy import sum_entries

w = Variable(n)
gamma = Parameter(sign='positive')
ret = mu.T*w 
risk = quad_form(w, Sigma)
prob = Problem(Maximize(ret - gamma*risk), 
               [sum_entries(w) == 1, 
                w >= 0])

# Compute trade-off curve.
SAMPLES = 100
risk_data = np.zeros(SAMPLES)
ret_data = np.zeros(SAMPLES)
gamma_vals = np.logspace(-2, 3, num=SAMPLES)
for i in range(SAMPLES):
    gamma.value = gamma_vals[i]
    prob.solve()
    risk_data[i] = math.sqrt(risk)
    ret_data[i] = ret.value
    
    
# Plot long only trade-off curve.
import matplotlib.pyplot as plt

markers_on = [29, 40]
fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(risk_data, ret_data, 'g-')
for marker in markers_on:
    plt.plot(risk_data[marker], ret_data[marker], 'bs')
    ax.annotate(r"$\gamma = %.2f$" % gamma_vals[marker], xy=(risk_data[marker]+.08, ret_data[marker]-.03))
for i in range(n):
    plt.plot(math.sqrt(Sigma[i,i]), mu[i], 'ro')
plt.xlabel('Standard deviation')
plt.ylabel('Return')
plt.show()