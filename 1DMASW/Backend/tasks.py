from celery import Celery
from obspy.io.segy.segy import _read_segy

app = Celery("tasks", broker="redis://redis:6379/0", backend="redis://redis:6379/0")

@app.task
def process_segy(file_path):
    try:
        st = _read_segy(file_path, headonly=True)
        traces = len(st.traces)
        return {"status": "success", "traces": traces, "file": file_path}
    except Exception as e:
        return {"status": "error", "message": str(e)}
from .inversion import perform_inversion

@celery.task
def process_segy_file(file_path):
    return perform_inversion(file_path)
from .inversion import perform_3d_inversion_with_bragg

@celery.task
def run_3d_inversion():
    return perform_3d_inversion_with_bragg()
@celery.task
def devito_fwi_task():
    return run_devito_fwi()

@celery.task
def simpeg_fwi_task():
    return run_simpeg_traveltime_fwi()

@celery.task
def madagascar_fwi_task(segy_file):
    return run_madagascar_fwi(segy_file)