import numpy as np
from time import sleep

# Grid world parameters
rows = 5
cols = 5
discount_factor = 0.95
goal_state = (4, 4) 
lightning_state = (3, 2)
mountain_states = [(3,1), (1,2), (1,3)]
T_min = 149

reward_vals = np.array([0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,-1,0,0, 0,0,0,0,1])

# Define reward function
def reward(state):
    if state == goal_state:
        return 1
    elif state == lightning_state:
        return -1
    else:
        return 0

# Define possible actions (up, down, left, right)
actions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def is_valid_action(state, action):
    new_state = (state[0] + action[0], state[1] + action[1])
    return (0 <= new_state[0] < rows) and (0 <= new_state[1] < cols) and (new_state not in mountain_states)

"""
Need to make it so this function takes in a state and a action and outputs a 1D vector with the transition probability for every state in the grid
"""
def calc_transition_probs(state, curr_action):
    transition_probs = np.zeros(rows * cols)
    # print(f"STATE IS {state}")
    if (tuple(state) == lightning_state) or (tuple(state) == goal_state) or (state in mountain_states):
        transition_probs[(state[0] * 5) + state[1]] = 1
    else:
        for action in actions:
            new_state = (state[0] + action[0], state[1] + action[1])
            if(is_valid_action(state, action)):
                if action == tuple(curr_action):
                    # print(f"New State is {new_state} and index is {(new_state[0] * 5) + new_state[1]}")
                    # sleep(0.1)
                    transition_probs[(new_state[0] * 5) + new_state[1]] += 0.85
                else:
                    transition_probs[(new_state[0] * 5) + new_state[1]] += 0.05
            else:
                if action == tuple(curr_action):
                    transition_probs[(state[0] * 5) + state[1]] += 0.85
                else:
                    transition_probs[(state[0] * 5) + state[1]] += 0.05
    return transition_probs

# Value Iteration
def value_iteration():
    values = np.zeros(rows * cols)
    for i in range(T_min):
        new_values = np.zeros(rows * cols)
        for state in range(rows * cols):
            i, j = divmod(state, cols)
            max_value = -np.inf
            for action in actions:
                transition_probs = calc_transition_probs((i, j), action)
                exp_val_func = sum([values[i] * transition_probs[i] for i in range(len(values))])
                value = reward((i, j)) + discount_factor * exp_val_func
                max_value = max(max_value, value)
            new_values[(i * 5) + j] = max_value
        values = new_values


    # Calculate a policy from the optimal value function list and then return the action list/policy and optimal value funtion!!!
    policy = np.zeros((rows * cols), dtype=('int', 2))
    for state in range(rows * cols):
        i, j = divmod(state, cols)
        max_value = -np.inf
        max_action = (-1,-1)
        for action in actions:
            transition_probs = calc_transition_probs((i, j), action)
            exp_val_func = sum([values[i] * transition_probs[i] for i in range(len(values))])
            value = reward((i, j)) + discount_factor * exp_val_func
            if(max_value < value):
                max_value = value
                max_action = action
    
        policy[(i * 5) + j] = max_action

    #Policy Evaluation
    transition_matrix = np.zeros((rows * cols), dtype=('float', (rows * cols)))
    
    for state in range(rows * cols):
        i, j = divmod(state, cols)
        transition_matrix[state] = calc_transition_probs((i, j), policy[state])

    i_matrix = np.eye(25)
    print(f"DIMENSIONS OF TRANSITION MATRIX ARE {np.linalg.inv((i_matrix - discount_factor * transition_matrix)).shape}")
    analytical_value_func = np.array(np.linalg.inv((i_matrix - discount_factor * transition_matrix)) @ reward_vals)
    values = analytical_value_func

    return policy, values



# Policy Iteration
def policy_iteration():
    values = np.zeros(rows * cols)
    policy = np.zeros((rows * cols), dtype=('int', 2))
    for i in range(T_min):
        new_values = np.zeros(rows * cols)
        for state in range(rows * cols):
            i, j = divmod(state, cols)
            max_value = -np.inf
            max_action = (-1,-1)
            for action in actions:
                transition_probs = calc_transition_probs((i, j), action)
                exp_val_func = sum([values[i] * transition_probs[i] for i in range(len(values))])
                value = reward((i, j)) + discount_factor * exp_val_func
                if(max_value < value):
                    max_value = value
                    max_action = action

            new_values[(i * 5) + j] = max_value
            policy[(i * 5) + j] = max_action

        
        #Policy Evaluation
        transition_matrix = np.zeros((rows * cols), dtype=('float', (rows * cols)))
        
        for state in range(rows * cols):
            i, j = divmod(state, cols)
            transition_matrix[state] = calc_transition_probs((i, j), policy[state])

        i_matrix = np.eye(25)
        analytical_value_func = np.array(np.linalg.inv((i_matrix - discount_factor * transition_matrix)) @ reward_vals)
        values = analytical_value_func

    return policy, values




val_policy, val_values = value_iteration()
pol_policy, pol_values = policy_iteration()

print(f"The value function from the policy from value iteration: {val_values}")
print(f"The policy from value iteration: {val_policy}\n\n\n")
print(f"The value function from the policy from policy iteration: {pol_values}")
print(f"The policy from policy iteration: {pol_policy}")