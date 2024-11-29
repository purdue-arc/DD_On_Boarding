import numpy as np

effective_horizon = 104
discount_factor = 0.95

transitions_h = np.array([[0.1, 0.8, 0.1],
                         [0.1, 0.1, 0.8],
                         [0.8, 0.1, 0.1]])

transitions_g = np.array([[0.8, 0.1, 0.1],
                         [0.1, 0.8, 0.1],
                         [0.1, 0.1, 0.8]])


def action(state):
    if state == 1:
        return [0.85, 0.15]
    elif state == 2:
        return [0.88, 0.12]
    elif state == 3:
        return [0.1, 0.9]
    

def reward(state, action):
    if state == 2 and action == 0:
        return 1
    else:
        return 0
    

def target_policy(state, action):
    if state == 0:
        if action == 0:
            return 0.9
        else:
            return 0.1
    elif state == 1:
        if action == 0:
            return 0.9
        else:
            return 0.1
    else:
        if action == 0:
            return 0.1
        else:
            return 0.9


def behavior_policy(state, action):
    if state == 0:
        if action == 0:
            return 0.85
        else:
            return 0.15
    elif state == 1:
        if action == 0:
            return 0.88
        else:
            return 0.12
    else:
        if action == 0:
            return 0.1
        else:
            return 0.9

    
def gen_episode(start_state):
    """Simulate an episode following the given policy."""
    episode = []
    state = start_state
    for _ in range(effective_horizon):
        # print(f"State is {state}")
        next_state_dist_h = transitions_h[state]
        next_state_dist_g = transitions_g[state]
        indices_h = list(range(len(next_state_dist_h)))
        indices_g = list(range(len(next_state_dist_g)))
        #sleep(0.2)
        next_action_dist = action(state + 1)
        next_action = np.random.choice([0, 1], p=next_action_dist, size=1)
        if next_action == 0:
            # print(f"P in h is {next_state_dist_h} with indices: {indices_h}")    
            next_state = np.random.choice(indices_g, p=next_state_dist_g, size=1)
        else:
            # print(f"P in g is {next_state_dist_g} with indices: {indices_g}")
            next_state = np.random.choice(indices_h, p=next_state_dist_h, size=1)
        # print(f"Next State is {int(next_state)}")
        reward_val = reward(state, next_action)
        episode.append((state, next_action, reward_val))
        state = int(next_state)
    return episode


def fv_monte_carlo(episodes=104):
    returns_sum = np.zeros(3)
    returns_cnt = np.zeros(3)
    value_function_mc = np.zeros(3)
    num_of_episodes = 0
    for _ in range(episodes):
        # Start from random non-terminal state
        start_state = 0
        # while is_terminal(start_state):
        #     start_state = (np.random.randint(cols), np.random.randint(rows))

        episode = gen_episode(start_state)
        num_of_episodes += 1
        G = 0
        visited_states = set()
        for t in range(len(episode)):
            state, next_action, reward_got = episode[t]
            #states = [t[0] for t in episode]
            #print(f"The States are: {states}")
            if state not in visited_states:
                rewards = [val[2] for val in episode[t:len(episode)]]
                states = [val[0] for val in episode[t:len(episode)]]
                actions = [val[1] for val in episode[t:len(episode)]]
                #print(f"Rewards are: {rewards}")
                G = 0
                W = 1
                for i in range(t, len(episode)):
                    G += (discount_factor ** (i - t)) * rewards[i - t]

                for i in range(t, len(episode)):
                    W *= target_policy(states[i - t], actions[i - t]) / behavior_policy(states[i - t], actions[i - t])

                #print(f"G is {G} and W is {W}")
                returns_sum[state] += G * W
                returns_cnt[state] += 1
                value_function_mc[state] = returns_sum[state] / returns_cnt[state]
                visited_states.add(state)
    
    return value_function_mc


value_function = fv_monte_carlo()
print(f"The value function is: {value_function}")