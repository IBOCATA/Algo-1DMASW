import numpy as np
from obspy.io.segy.segy import _read_segy
from scipy.signal import ricker
from scipy.linalg import toeplitz
import os

def perform_inversion_1D(file_path):
    # Load seismic data
    st = _read_segy(file_path)
    tr = st.traces[0]
    data = tr.data.astype(np.float32)

    # Create a Ricker wavelet (25 Hz)
    dt = tr.header.sample_interval_in_ms_for_this_trace / 1000.0
    wavelet = ricker(points=100, a=25)
    wavelet = wavelet / np.max(np.abs(wavelet))

    # Convolve data with wavelet matrix (Toeplitz model)
    n = len(data)
    W = toeplitz(np.r_[wavelet[0], np.zeros(n - 1)], wavelet)
    d = data[:len(W)]  # truncate data to match model

    # Least-squares inversion (Tikhonov regularization)
    lam = 0.01  # regularization strength
    I = np.eye(W.shape[1])
    m = np.linalg.inv(W.T @ W + lam * I) @ W.T @ d

    # Save inversion result
    output_path = file_path.replace(".segy", "_inversion.npy")
    np.save(output_path, m)

    return {
        "status": "done",
        "output": output_path
    }
