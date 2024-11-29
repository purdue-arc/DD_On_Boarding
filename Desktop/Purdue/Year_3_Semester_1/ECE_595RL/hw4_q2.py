import numpy as np

discount = 0.95
transitions = np.array([[0.1, 0.8, 0.1],
                        [0.1, 0.1, 0.8],
                        [0.1, 0.1, 0.8]])

reward = np.array([0, 0, 1])
i_matrix = np.eye(3)
analytical_value_func = np.array(np.linalg.inv((i_matrix - discount * transitions)) @ reward)

print(f"The Analytical Value Function is {analytical_value_func}")
