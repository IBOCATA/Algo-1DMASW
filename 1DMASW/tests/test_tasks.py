from backend.tasks import devito_fwi_task

def test_devito_task_runs():
    result = devito_fwi_task.apply().get()
    assert result["status"] == "done"