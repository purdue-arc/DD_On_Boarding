import numpy as np

discount = 0.95
transitions = np.array([[0.1, 0.8, 0.1],
                        [0.1, 0.1, 0.8],
                        [0.1, 0.1, 0.8]])

reward = np.array([0, 0, 1])
i_matrix = np.eye(3)
analytical_value_func = np.array(np.linalg.inv((i_matrix - discount * transitions)) @ reward)

print(f"The Analytical Value Function is {analytical_value_func}")


true_P = np.array([[0.1, 0.8, 0.1],
                   [0.1, 0.1, 0.8],
                   [0.1, 0.1, 0.8]])


State_Act_Samples = {
    "1": [],
    "2": [],
    "3": []
}
state = 0
discount = 0.95

def action(state):
    if state == 1:
        return 0
    elif state == 2:
        return 0
    elif state == 3:
        return 1


def reward(state):
    if state == 3:
        return 1
    else:
        return 0
    
min_samples = 99
while min_samples < 100:
    min_samples = 100
    #print(f"Min Num of Samples: {min_samples}")
    #print(State_Act_Samples)
    next_state_dist = true_P[state]
    indices = list(range(len(next_state_dist)))
    next_action = action(state + 1)
    next_state = np.random.choice(indices, p=next_state_dist, size=1)
    reward_val = reward(state)
    State_Act_Samples[str(state + 1)].append(int(next_state) + 1)
    state = int(next_state)
    for i in State_Act_Samples.values():
        # print(i)
        if len(i) < min_samples:
            min_samples = len(i)




estimated_P = []

for values in State_Act_Samples.values():
    state_1_cnt = 0
    state_2_cnt = 0
    state_3_cnt = 0

    for val in values:
        if val == 1:
            state_1_cnt += 1
        elif val == 2:
            state_2_cnt += 1
        else:
            state_3_cnt += 1

    cnts = [state_1_cnt, state_2_cnt, state_3_cnt]
    #print(state_1_cnt + state_2_cnt + state_3_cnt)
    cnts = [cnt / len(values) for cnt in cnts]
    estimated_P.append(cnts)

estimated_P = np.array(estimated_P)
difference = estimated_P - true_P
l1_norm = [sum(norm) for norm in np.abs(difference)]

i_matrix = np.eye(3)
mu_0 = [1, 0, 0]
norm_state_occ = np.linalg.inv((i_matrix - discount * estimated_P.T)) @ mu_0

val_func_diff_bound =  (discount / (1 - discount) ** 2) * sum([norm_state_occ[i] * l1_norm[i] for i in range(len(l1_norm))])

reward_vals = np.array([0, 0, 1])
i_matrix = np.eye(3)
estimated_val_func = np.array(np.linalg.inv((i_matrix - discount * estimated_P)) @ reward_vals)

val_diff = abs(analytical_value_func - estimated_val_func)

print(f"Estimated P; {estimated_P}")
print(f"L1 Norm: {l1_norm}")
print(f"Norm State Occ: {norm_state_occ}")
print(f"Upper Bound of Val Func Diff: {val_func_diff_bound}")
print(f"Estimated Val Func: {estimated_val_func}")
print(f"Absolute Difference in Val Funcs: {val_diff}")








        