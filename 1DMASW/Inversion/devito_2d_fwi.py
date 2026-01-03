from devito import Grid, TimeFunction, Function, Eq, Operator
import numpy as np
import os

def devito_2d_fwi(shape=(101, 101), spacing=(10., 10.), nbl=20, tn=1000, f0=0.01, output_dir="devito_fwi"):
    from examples.seismic import RickerSource, Receiver, setup_geometry, plot_image
    from examples.seismic.acoustic import AcousticWaveSolver

    # 1. Velocity model with anomaly
    model_true = np.ones(shape) * 1500.
    model_true[40:60, 40:60] += 400.  # velocity anomaly

    # 2. Setup Devito objects
    grid = Grid(shape=shape, extent=(spacing[0]*shape[0], spacing[1]*shape[1]))
    model = Function(name="m", grid=grid)
    model.data[:] = 1 / (model_true**2)

    # 3. Source and receivers
    geometry = setup_geometry(model.shape, spacing, nbl, tn, f0)
    src = RickerSource(name='src', grid=grid, f0=f0, time_range=geometry.time_axis)
    src.coordinates.data[0, :] = geometry.src_positions[0]

    rec = Receiver(name='rec', grid=grid, npoint=geometry.nrec, time_range=geometry.time_axis)
    rec.coordinates.data[:, :] = geometry.rec_positions

    # 4. Forward modeling (true data)
    solver = AcousticWaveSolver(model, geometry, space_order=2)
    rec_data = solver.forward(src=src, rec=rec, save=True)

    # 5. Inversion loop (very simplified gradient descent)
    m0 = Function(name="m0", grid=grid)
    m0.data[:] = 1 / (1500.**2)

    for i in range(5):  # number of FWI iterations
        solver = AcousticWaveSolver(m0, geometry, space_order=2)
        rec0, u0, _ = solver.forward(src=src, rec=rec, save=True)
        residual = rec_data.data - rec0.data

        # Compute gradient via adjoint
        gradient = solver.gradient(rec0, u0)

        # Update model with gradient descent
        alpha = 1e-4
        m0.data[:] -= alpha * gradient.data

    os.makedirs(output_dir, exist_ok=True)
    np.save(os.path.join(output_dir, "velocity_inverted.npy"), 1 / np.sqrt(m0.data))

    return {"status": "done", "velocity_inverted": os.path.join(output_dir, "velocity_inverted.npy")}
