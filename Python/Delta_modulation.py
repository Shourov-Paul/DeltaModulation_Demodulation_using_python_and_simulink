import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

# Parameters
sampling_rate = 100  # Sampling rate (Hz)
duration = 1          # Duration of the signal (seconds)
step_size = 0.3       # Step size for Delta Modulation

# Generate a sine wave signal
time = np.arange(0, duration, 1 / sampling_rate)
frequency = 5  # Frequency of the sine wave (Hz)
input_signal = np.sin(2 * np.pi * frequency * time)

# Delta Modulation
delta_modulated_signal = []
quantized_signal = [0]  # Initialize quantized signal with zero

for sample in input_signal:
    # Determine the step (1 or -1)
    if sample > quantized_signal[-1]:
        delta_modulated_signal.append(1)
        new_value = quantized_signal[-1] + step_size
    else:
        delta_modulated_signal.append(0)
        new_value = quantized_signal[-1] - step_size
    quantized_signal.append(new_value)

# Remove the initial zero from quantized_signal for plotting
quantized_signal = quantized_signal[1:]

# Delta Demodulation
reconstructed_signal = [0]  # Initialize the reconstructed signal
for bit in delta_modulated_signal:
    if bit == 1:
        new_value = reconstructed_signal[-1] + step_size
    else:
        new_value = reconstructed_signal[-1] - step_size
    reconstructed_signal.append(new_value)

# Remove the initial zero from reconstructed_signal for plotting
reconstructed_signal = reconstructed_signal[1:]

# Apply Low-Pass Filter to the Reconstructed Signal
def low_pass_filter(data, cutoff_freq, fs, order=4):
    nyquist = fs / 2.0
    normal_cutoff = cutoff_freq / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    filtered_signal = filtfilt(b, a, data)
    return filtered_signal

cutoff_frequency = 10  # Cutoff frequency for the LPF (Hz)
reconstructed_signal_lpf = low_pass_filter(reconstructed_signal, cutoff_frequency, sampling_rate)

# Plotting
fig, axs = plt.subplots(2, 3, figsize=(16, 10))

# Plot 1: Original Signal
axs[0, 0].plot(time, input_signal, label="Original Signal") 
axs[0, 0].set_title("Original Signal")
axs[0, 0].set_xlabel("Time (s)")
axs[0, 0].set_ylabel("Amplitude")
axs[0, 0].grid()
axs[0, 0].legend(loc="upper right")

# Plot 2: Delta Modulated Signal
axs[0, 1].step(time, quantized_signal, label="Delta Modulated Signal", where="post")
axs[0, 1].set_title("Delta Modulated Signal")
axs[0, 1].set_xlabel("Time (s)")
axs[0, 1].set_ylabel("Amplitude")
axs[0, 1].grid()
axs[0, 1].legend(loc="upper right")

# Plot 3: Original Signal on Top of Delta Modulated Signal
axs[0, 2].plot(time, input_signal, label="Original Signal")
axs[0, 2].step(time, quantized_signal, label="Delta Modulated Signal", where="post", alpha=0.7)
axs[0, 2].set_title("Original Signal and Delta Modulated Signal")
axs[0, 2].set_xlabel("Time (s)")
axs[0, 2].set_ylabel("Amplitude")
axs[0, 2].grid()
axs[0, 2].legend(loc="upper right")

# Plot 4: Reconstructed Signal
axs[1, 0].plot(time, reconstructed_signal, label="Reconstructed Signal")
axs[1, 0].set_title("Reconstructed Signal")
axs[1, 0].set_xlabel("Time (s)")
axs[1, 0].set_ylabel("Amplitude")
axs[1, 0].grid()
axs[1, 0].legend(loc="upper right")

# Plot 5: Reconstructed Signal on Top of Original Signal
axs[1, 1].plot(time, input_signal, label="Original Signal")
axs[1, 1].plot(time, reconstructed_signal, label="Reconstructed Signal", alpha=0.7)
axs[1, 1].set_title("Original Signal and Reconstructed Signal")
axs[1, 1].set_xlabel("Time (s)")
axs[1, 1].set_ylabel("Amplitude")
axs[1, 1].grid()
axs[1, 1].legend(loc="upper right")

# Plot 6: Reconstructed Signal after LPF on Top of Original Signal
axs[1, 2].plot(time, input_signal, label="Original Signal")
axs[1, 2].plot(time, reconstructed_signal_lpf, label="Output", alpha=0.7)
axs[1, 2].set_title("Original Signal and Reconstructed Signal (After LPF)")
axs[1, 2].set_xlabel("Time (s)")
axs[1, 2].set_ylabel("Amplitude")
axs[1, 2].grid()
axs[1, 2].legend(loc="upper right")

# Adjust layout
plt.tight_layout()
plt.show()
