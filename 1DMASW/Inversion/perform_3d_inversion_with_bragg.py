import numpy as np
from scipy.signal import ricker
from scipy.fftpack import fftn, ifftn, fftfreq
import os

def perform_3d_inversion_with_bragg(output_dir="processed", grid_shape=(64, 64, 64)):
    nx, ny, nz = grid_shape
    dx = dz = dy = 1.0  # spatial sampling in meters

    # 1. Define background velocity (constant)
    velocity_bg = 2000  # m/s

    # 2. Define Gaussian anomaly (velocity increase)
    x, y, z = np.meshgrid(
        np.linspace(-1, 1, nx),
        np.linspace(-1, 1, ny),
        np.linspace(-1, 1, nz),
        indexing='ij'
    )
    sigma = 0.3
    gaussian = np.exp(-(x**2 + y**2 + z**2) / (2 * sigma**2))

    velocity_model = velocity_bg + 500 * gaussian  # anomaly added to base

    # 3. Compute reflectivity (1D along depth)
    reflectivity = np.diff(velocity_model, axis=2)
    reflectivity = np.pad(reflectivity, ((0, 0), (0, 0), (0, 1)), mode='edge')

    # 4. Forward model: convolve with Ricker wavelet in depth
    wavelet = ricker(points=100, a=10)
    for ix in range(nx):
        for iy in range(ny):
            reflectivity[ix, iy, :] = np.convolve(reflectivity[ix, iy, :], wavelet, mode='same')

    # 5. Apply Bragg scattering enhancement (in frequency domain)
    # Simulate periodic reflectors using FFT enhancement
    freq_x = fftfreq(nx, d=dx)
    freq_y = fftfreq(ny, d=dy)
    freq_z = fftfreq(nz, d=dz)
    FX, FY, FZ = np.meshgrid(freq_x, freq_y, freq_z, indexing='ij')

    bragg_freq = 0.2  # cycles/m
    k = np.sqrt(FX**2 + FY**2 + FZ**2)
    enhancement = np.exp(-((k - bragg_freq)**2) / (2 * (0.05**2)))

    reflectivity_fft = fftn(reflectivity)
    reflectivity_bragg = np.real(ifftn(reflectivity_fft * enhancement))

    # 6. Save results
    os.makedirs(output_dir, exist_ok=True)
    np.save(os.path.join(output_dir, "velocity_model.npy"), velocity_model)
    np.save(os.path.join(output_dir, "reflectivity_3d.npy"), reflectivity_bragg)

    return {
        "status": "done",
        "velocity_model": os.path.join(output_dir, "velocity_model.npy"),
        "reflectivity_bragg": os.path.join(output_dir, "reflectivity_3d.npy")
    }
