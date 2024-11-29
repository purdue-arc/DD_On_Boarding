from sympy import symbols, expand, diff, solve

# Define symbols
theta_1, theta_2 = symbols('theta_1 theta_2')
y1, y2, y3 = 1.675, -3.35, -1.85

# Define the loss terms
L1 = ((-theta_1 + theta_2) - y1)**2
L2 = (theta_2 - y2)**2
L3 = ((-2*theta_1 - theta_2) - y3)**2

# Total loss function
L_total = expand(L1 + L2 + L3)

# Partial derivatives
grad_theta1 = diff(L_total, theta_1)
grad_theta2 = diff(L_total, theta_2)

# Solve for optimal theta_1 and theta_2
optimal_theta = solve([grad_theta1, grad_theta2], (theta_1, theta_2))
print(optimal_theta, L_total.subs(optimal_theta))