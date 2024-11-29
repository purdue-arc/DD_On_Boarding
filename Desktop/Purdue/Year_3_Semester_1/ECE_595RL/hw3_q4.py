import numpy as np
import matplotlib.pyplot as plt
from time import sleep

# Grid world parameters
rows = 5
cols = 5
discount_factor = 0.95
goal_state = (4, 0) 
lightning_state = (2, 1)
mountain_states = [(1,1), (2,3), (3,3)]
T_min = 149
value_function_mc = np.zeros(rows * cols)
value_function_td = np.zeros(rows * cols) 
num_of_episodes_mc = 0
num_of_episodes_td = 0


transitions = np.array([[0.10,0.85,0,0,0,0.05,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0.05,0.10,0.85,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0.0,0.05,0.05,0.85,0,0,0,0.05,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0.0,0.0,0.05,0.05,0.85,0,0,0,0.05,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0.0,0.0,0,0,1, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
                        [0.05,0.0,0,0,0, 0.9,0,0,0,0, 0.05,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
                        [0.0,0.0,0,0,0, 0,1,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
                        [0.0,0.0,0,0,0, 0,0,1,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
                        [0.0,0.0,0,0.05,0, 0,0,0.85,0.0,0.05, 0,0,0,0.05,0, 0,0,0,0,0, 0,0,0,0,0],
                        [0.0,0.0,0,0,0.85, 0,0,0,0.05,0.05, 0,0,0,0,0.05, 0,0,0,0,0, 0,0,0,0,0],
                        [0.0,0.0,0,0,0, 0.85,0,0,0,0, 0.05,0.05,0,0,0, 0.05,0,0,0,0, 0,0,0,0,0],
                        [0.0,0.0,0,0,0, 0,0,0,0,0, 0.05,0.85,0.05,0,0, 0,0.05,0,0,0, 0,0,0,0,0],
                        [0.0,0.0,0,0,0, 0,0,0.05,0,0, 0,0.05,0.05,0.85,0, 0,0,0,0,0, 0,0,0,0,0],
                        [0.0,0.0,0,0,0, 0,0,0,0.05,0, 0,0,0.05,0.05,0.85, 0,0,0,0,0, 0,0,0,0,0],
                        [0.0,0.0,0,0,0, 0,0,0,0,0.05, 0,0,0,0.05,0.85, 0,0,0,0,0.05, 0,0,0,0,0],
                        [0.0,0.0,0,0,0, 0,0,0,0,0, 0.85,0,0,0,0, 0.05,0.05,0,0,0, 0.05,0,0,0,0],
                        [0.0,0.0,0,0,0, 0,0,0,0,0, 0,0.05,0,0,0, 0.05,0,0,0,0, 0,0.9,0,0,0],
                        [0.0,0.0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,1,0,0, 0,0,0,0,0],
                        [0.0,0.0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,1,0, 0,0,0,0,0],
                        [0.0,0.0,0,0,0, 0,0,0,0,0, 0,0,0,0,0.85, 0,0,0,0,0.1, 0,0,0,0,0.05],
                        [0.0,0.0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0.85,0,0,0,0, 0.1,0.05,0,0,0],
                        [0.0,0.0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0.05,0,0,0, 0.05,0.05,0.85,0,0],
                        [0.0,0.0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0.05,0.1,0.85,0],
                        [0.0,0.0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0.05,0.9,0.05],
                        [0.0,0.0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0.85, 0,0,0,0.05,0.1]])

# Define reward function
def reward(state):
    if state == goal_state:
        return 1
    elif state == lightning_state:
        return -1
    else:
        return 0
    

def is_terminal(state):
    if state == goal_state or state == lightning_state or state in mountain_states:
        return 1
    else:
        return 0


def gen_episode(start_state):
    """Simulate an episode following the given policy."""
    episode = []
    state = start_state
    while not is_terminal(state): # MIGHT HAVE TO HAVE SPECIAL CASE IF START IN LIGHTNING OR GOAL OR MOUNTAINS!!!
        #print(f"State is {state}")
        next_state_dist = transitions[(state[1] * 5) + state[0]]
        indices = list(range(len(next_state_dist)))
        #print(f"P is {next_state_dist} with indices: {indices}")
        #sleep(0.2)
        next_state_idx = np.random.choice(indices, p=next_state_dist, size=1)
        #print(f"Next State Idx is {next_state_idx}")
        i, j = divmod(next_state_idx, cols)
        next_state = (int(j), int(i))
        reward_val = reward(state)
        episode.append((state, reward_val))
        state = next_state
    #print(f"Terminal State is {state}")
    reward_val = reward(state)
    episode.append((state, reward_val))
    return episode


def fv_monte_carlo(episodes=0):
    returns_sum = np.zeros(rows * cols)
    returns_cnt = np.zeros(rows * cols)
    num_of_episodes = 0
    # for _ in range(episodes):
    while min(returns_cnt) < 1000:
        # Start from random non-terminal state
        start_state = (np.random.randint(cols), np.random.randint(rows))
        # while is_terminal(start_state):
        #     start_state = (np.random.randint(cols), np.random.randint(rows))

        episode = gen_episode(start_state)
        num_of_episodes += 1
        G = 0
        visited_states = set()
        for t in range(len(episode)):
            state, reward = episode[t]
            if state not in visited_states:
                rewards = [val[1] for val in episode[t:len(episode)]]
                G = 0
                for i in range(t, len(episode)):
                    G += (discount_factor ** (i - t)) * rewards[i - t]
                returns_sum[(state[1] * 5) + state[0]] += G
                returns_cnt[(state[1] * 5) + state[0]] += 1
                value_function_mc[(state[1] * 5) + state[0]] = returns_sum[(state[1] * 5) + state[0]] / returns_cnt[(state[1] * 5) + state[0]]
                visited_states.add(state)
    
    return num_of_episodes
    # print(f"The Min Ns = N is: {min(returns_cnt)}")
    # print(f"Number of Episodes is: {num_of_episodes_mc}")


def temporal_difference(episodes=0, alpha=0.009):
    returns_cnt = np.zeros(rows * cols)
    # for _ in range(episodes):
    num_of_episodes = 0
    while min(returns_cnt) < 1000:
        # Start from random non-terminal state
        start_state = (np.random.randint(cols), np.random.randint(rows))
        num_of_episodes += 1
        # while is_terminal(start_state):
        #     start_state = (np.random.randint(cols), np.random.randint(rows))
        
        state = start_state
        while not is_terminal(state):
            next_state_dist = transitions[(state[1] * 5) + state[0]]
            indices = list(range(len(next_state_dist)))
            next_state_idx = np.random.choice(indices, p=next_state_dist, size=1)
            i, j = divmod(next_state_idx, cols)
            next_state = (int(j), int(i))
            reward_val = reward(state)

            # Update TD(0)
            real_alpha = np.log(1 + returns_cnt[(state[1] * 5) + state[0]]) / (1 + returns_cnt[(state[1] * 5) + state[0]])
            value_function_td[(state[1] * 5) + state[0]] += real_alpha * (reward_val + discount_factor * value_function_td[(next_state[1] * 5) + next_state[0]] - value_function_td[(state[1] * 5) + state[0]])
            returns_cnt[(state[1] * 5) + state[0]] += 1
            state = next_state
            #1 / (1 + returns_cnt[(state[1] * 5) + state[0]])

        reward_val = reward(state)
        value_function_td[(state[1] * 5) + state[0]] = reward_val
        returns_cnt[(state[1] * 5) + state[0]] += 1
        # alpha * (reward_val + discount_factor * 0 - value_function_td[(state[1] * 5) + state[0]])
    return num_of_episodes


def fv_monte_carlo_ep(episodes=0):
    returns_sum = np.zeros(rows * cols)
    returns_cnt = np.zeros(rows * cols)
    for _ in range(episodes):
        # Start from random non-terminal state
        start_state = (np.random.randint(cols), np.random.randint(rows))
        # while is_terminal(start_state):
        #     start_state = (np.random.randint(cols), np.random.randint(rows))

        episode = gen_episode(start_state)
        G = 0
        visited_states = set()
        for t in range(len(episode)):
            state, reward = episode[t]
            if state not in visited_states:
                rewards = [val[1] for val in episode[t:len(episode)]]
                G = 0
                for i in range(t, len(episode)):
                    G += (discount_factor ** (i - t)) * rewards[i - t]
                returns_sum[(state[1] * 5) + state[0]] += G
                returns_cnt[(state[1] * 5) + state[0]] += 1
                value_function_mc[(state[1] * 5) + state[0]] = returns_sum[(state[1] * 5) + state[0]] / returns_cnt[(state[1] * 5) + state[0]]
                visited_states.add(state)

    # print(f"The Min Ns = N is: {min(returns_cnt)}")
    # print(f"Number of Episodes is: {num_of_episodes_mc}")


def temporal_difference_ep(episodes=0, alpha=0.009):
    returns_cnt = np.zeros(rows * cols)
    for _ in range(episodes):
        # Start from random non-terminal state
        start_state = (np.random.randint(cols), np.random.randint(rows))
        # while is_terminal(start_state):
        #     start_state = (np.random.randint(cols), np.random.randint(rows))
        
        state = start_state
        while not is_terminal(state):
            next_state_dist = transitions[(state[1] * 5) + state[0]]
            indices = list(range(len(next_state_dist)))
            next_state_idx = np.random.choice(indices, p=next_state_dist, size=1)
            i, j = divmod(next_state_idx, cols)
            next_state = (int(j), int(i))
            reward_val = reward(state)

            # Update TD(0)
            real_alpha = np.log(1 + returns_cnt[(state[1] * 5) + state[0]]) / (1 + returns_cnt[(state[1] * 5) + state[0]])
            value_function_td[(state[1] * 5) + state[0]] += real_alpha * (reward_val + discount_factor * value_function_td[(next_state[1] * 5) + next_state[0]] - value_function_td[(state[1] * 5) + state[0]])
            returns_cnt[(state[1] * 5) + state[0]] += 1
            state = next_state
            #1 / (1 + returns_cnt[(state[1] * 5) + state[0]])

        reward_val = reward(state)
        value_function_td[(state[1] * 5) + state[0]] = reward_val
        # alpha * (reward_val + discount_factor * 0 - value_function_td[(state[1] * 5) + state[0]])

reward_true = np.array([0,0,0,0,1,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0])

transitions_true = np.array([[0.10,0.85,0,0,0,0.05,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
                        [0.05,0.10,0.85,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
                        [0.0,0.05,0.05,0.85,0,0,0,0.05,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
                        [0.0,0.0,0.05,0.05,0.85,0,0,0,0.05,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0],
                        [0.0,0.0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 1],
                        [0.05,0.0,0,0,0, 0.9,0,0,0,0, 0.05,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0],
                        [0.0,0.0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 1],
                        [0.0,0.0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 1],
                        [0.0,0.0,0,0.05,0, 0,0,0.85,0.0,0.05, 0,0,0,0.05,0, 0,0,0,0,0, 0,0,0,0,0, 0],
                        [0.0,0.0,0,0,0.85, 0,0,0,0.05,0.05, 0,0,0,0,0.05, 0,0,0,0,0, 0,0,0,0,0, 0],
                        [0.0,0.0,0,0,0, 0.85,0,0,0,0, 0.05,0.05,0,0,0, 0.05,0,0,0,0, 0,0,0,0,0, 0],
                        [0.0,0.0,0,0,0, 0,0,0,0,0, 0.05,0.85,0.05,0,0, 0,0.05,0,0,0, 0,0,0,0,0, 0],
                        [0.0,0.0,0,0,0, 0,0,0.05,0,0, 0,0.05,0.05,0.85,0, 0,0,0,0,0, 0,0,0,0,0, 0],
                        [0.0,0.0,0,0,0, 0,0,0,0.05,0, 0,0,0.05,0.05,0.85, 0,0,0,0,0, 0,0,0,0,0, 0],
                        [0.0,0.0,0,0,0, 0,0,0,0,0.05, 0,0,0,0.05,0.85, 0,0,0,0,0.05, 0,0,0,0,0, 0],
                        [0.0,0.0,0,0,0, 0,0,0,0,0, 0.85,0,0,0,0, 0.05,0.05,0,0,0, 0.05,0,0,0,0, 0],
                        [0.0,0.0,0,0,0, 0,0,0,0,0, 0,0.05,0,0,0, 0.05,0,0,0,0, 0,0.9,0,0,0, 0],
                        [0.0,0.0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 1],
                        [0.0,0.0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 1],
                        [0.0,0.0,0,0,0, 0,0,0,0,0, 0,0,0,0,0.85, 0,0,0,0,0.1, 0,0,0,0,0.05, 0],
                        [0.0,0.0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0.85,0,0,0,0, 0.1,0.05,0,0,0, 0],
                        [0.0,0.0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0.05,0,0,0, 0.05,0.05,0.85,0,0, 0],
                        [0.0,0.0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0.05,0.1,0.85,0, 0],
                        [0.0,0.0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0.05,0.9,0.05, 0],
                        [0.0,0.0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0.85, 0,0,0,0.05,0.1, 0],
                        [0.0,0.0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 1]])

i_matrix = np.eye(26)

true_value_func = np.array(np.linalg.inv((i_matrix - discount_factor * transitions_true)) @ reward_true)

# Run the Monte Carlo method
num_of_episodes_mc = fv_monte_carlo()

# Display value function after MC evaluation
print("Value function after First-Visit Monte Carlo evaluation:")
print(value_function_mc)

# Run the TD learning method
num_of_episodes_td = temporal_difference()

# Display value function after TD evaluation
print("Value function after Temporal Difference (TD) evaluation:")
print(value_function_td)


print("True Value function is:")
print(true_value_func)

true_value_func = true_value_func[0:len(true_value_func) - 1]


# Calculate and plot the errors between Vn (Monte Carlo/TD) and Vπ (true value function)

def plot_errors():
    errors_mc = []
    errors_td = []
    
    for n in range(1, max([num_of_episodes_mc, num_of_episodes_td]), 100):
        print(f"In Episode {n}")
        fv_monte_carlo_ep(episodes=n)
        temporal_difference_ep(episodes=n)
        error_mc = np.linalg.norm(value_function_mc - true_value_func)
        error_td = np.linalg.norm(value_function_td - true_value_func)
        errors_mc.append(error_mc)
        errors_td.append(error_td)
    
    plt.plot(list(range(1, max([num_of_episodes_mc, num_of_episodes_td]), 100)), errors_mc, label="Monte Carlo")
    plt.plot(list(range(1, max([num_of_episodes_mc, num_of_episodes_td]), 100)), errors_td, label="TD Learning")
    plt.xlabel("Episodes")
    plt.ylabel("Error")
    plt.legend()
    plt.show()

# Run and plot the error sequence
plot_errors()