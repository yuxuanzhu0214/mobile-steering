class Kalman:
    def __init__(self, initial_state, initial_uncertainty, process_noise, measurement_noise):
        self.state = initial_state
        self.uncertainty = initial_uncertainty
        self.process_noise = process_noise
        self.measurement_noise = measurement_noise

    def predict(self):
        self.uncertainty += self.process_noise

    def update(self, measurement, uncertainty):
        self.uncertainty = uncertainty
        kalman_gain = self.uncertainty / (self.uncertainty + self.measurement_noise)
        self.state = self.state + kalman_gain * (measurement - self.state)
        self.uncertainty = (1 - kalman_gain) * self.uncertainty

# # Example usage:
# initial_state = 0
# initial_uncertainty = 1
# process_noise = 0.1
# measurement_noise = 1
# kf = Kalman(initial_state, initial_uncertainty, process_noise, measurement_noise)

# # Simulate measurements
# true_state = np.linspace(0, 10, 100)
# measurements = true_state + np.random.normal(0, 1, len(true_state))  # Add noise to the true state

# # Apply Kalman Filter
# estimated_states = []
# for measurement in measurements:
#     kf.predict()
#     kf.update(measurement)
#     estimated_states.append(kf.state)

# # Compare true state, measurements, and estimated states
# plt.plot(true_state, label='True State')
# plt.plot(measurements, label='Measurements', linestyle=':', marker='o', alpha=0.5)
# plt.plot(estimated_states, label='Estimated State', linestyle='--', marker='x')
# plt.legend()
# plt.show()