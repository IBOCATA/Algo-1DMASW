import subprocess
import os

def run_madagascar_fwi(segy_file, output_dir="madagascar_output"):
    os.makedirs(output_dir, exist_ok=True)
    
    rsf_file = os.path.join(output_dir, "data.rsf")
    vel_file = os.path.join(output_dir, "velocity.rsf")
    model_file = os.path.join(output_dir, "model.rsf")

    # 1. Convert SEG-Y to RSF
    subprocess.run(["segyread", f"tape={segy_file}", f"read={rsf_file}"], check=True)

    # 2. Generate starting velocity model
    subprocess.run(["sfspike", "n1=100", "d1=0.01", f"output={vel_file}", "mag=1500"], check=True)

    # 3. Run basic FWI
    subprocess.run([
        "sfwi",
        f<data={rsf_file}",
        f<vel0={vel_file}",
        f>vel1={model_file}",
        "niter=5"
    ], check=True)

    return {"status": "done", "velocity_model": model_file}
