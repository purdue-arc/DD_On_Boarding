import numpy as np
import matplotlib.pyplot as plt

P = [[0.2, 0.4, 0.4],
     [0.375, 0.25, 0.375],
     [0.45, 0.45, 0.1]]

t = 1000000
P_t = [[0.2, 0.4, 0.4],
     [0.375, 0.25, 0.375],
     [0.45, 0.45, 0.1]]
for i in range(t):
    P_t = np.matmul(P_t, P)

print(P_t)




u_bar = P_t[0, :]
u_t = [0, 1, 0]
l1_norms_mu_t = []

for i in range(100):
    norm_u_t = np.linalg.norm(u_t, ord=1)
    l1_norms_mu_t.append(norm_u_t)
    u_t = np.matmul(u_t, P)

l1_norms_mu_t.append(norm_u_t)


l1_norm_stationary = np.linalg.norm(u_bar, ord=1)  

l1_diff = np.abs(l1_norms_mu_t - l1_norm_stationary)

time_steps = np.arange(101)

plt.figure(figsize=(8, 6))
plt.plot(time_steps, l1_diff, marker='o', linestyle='-', color='b')

plt.title('Difference between µ_t and ¯µ in L1 norm over time')
plt.xlabel('Time steps (t)')
plt.ylabel('L1 norm difference |µ_t - ¯µ|')
plt.grid(True)
plt.show()

    