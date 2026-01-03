from fastapi import FastAPI, UploadFile, File, BackgroundTasks
import shutil
import os
from tasks import process_segy

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Send to Celery
        task = process_segy.delay(file_path)
        return {"status": "ok", "task_id": task.id, "file": file.filename}
    except Exception as e:
        return {"status": "error", "message": str(e)}

from fastapi import FastAPI, File, UploadFile
from tasks import devito_fwi_task, simpeg_fwi_task, madagascar_fwi_task
import shutil

app = FastAPI()

@app.post("/run/devito")
def run_devito():
    devito_fwi_task.delay()
    return {"status": "Devito FWI started"}

@app.post("/run/simpeg")
def run_simpeg():
    simpeg_fwi_task.delay()
    return {"status": "SimPEG travel-time FWI started"}

@app.post("/run/madagascar")
def run_madagascar(file: UploadFile = File(...)):
    segy_path = f"/app/uploads/{file.filename}"
    with open(segy_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    madagascar_fwi_task.delay(segy_path)
    return {"status": "Madagascar FWI started", "file": file.filename}
from fastapi import Depends
from auth import verify_token

@app.get("/secure-endpoint/")
def secure_data(user: str = Depends(verify_token)):
    return {"message": f"Hello {user}, you are authorized!"}
from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # ⚠️ À remplacer par une vraie base utilisateur
    if form_data.username == "iliasbounsir@gmail.com" and form_data.password == "Qazwsxedc866556,1@":
        access_token = jwt.encode({"sub": form_data.username}, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
import os
from paypal import create_paypal_order
from invoice import generate_invoice_pdf

app = FastAPI()

@app.post("/create-stripe-session")
async def create_stripe_session():
    # Stripe session creation logic
    pass

@app.post("/create-paypal-session")
async def create_paypal_session():
    return create_paypal_order()

@app.post("/webhook")
async def webhook(request: Request):
    # Handle Stripe and PayPal webhooks
    pass

@app.get("/generate-invoice/{username}")
async def get_invoice(username: str):
    invoice_path = generate_invoice_pdf(username, 20.00, invoice_id="INV123")
    return FileResponse(invoice_path, media_type="application/pdf", filename="invoice.pdf")
@app.get("/visualize/1d_shear")
def get_1d_profile():
    return {"depth": [0, 5, 10, 15, 20], "velocity": [300, 400, 600, 750, 900]}

@app.get("/visualize/2d_fwi")
def get_2d_fwi():
    import numpy as np
    vel = np.random.rand(50, 50).tolist()
    return {"velocity": vel}

@app.get("/visualize/3d_volume")
def get_3d_volume():
    import numpy as np
    x, y, z = np.meshgrid(range(10), range(10), range(10))
    vel = np.random.rand(10, 10, 10).flatten().tolist()
    return {
        "x": x.flatten().tolist(),
        "y": y.flatten().tolist(),
        "z": z.flatten().tolist(),
        "velocity": vel
    }

@app.get("/export")
def export(format: str):
    if format == "csv":
        return FileResponse("processed/fwi_result.csv")
    if format == "xyz":
        return FileResponse("processed/volume.xyz")
    if format == "vtk":
        return FileResponse("processed/volume.vtk")
    if format == "tif":
        return FileResponse("processed/fwi_geotiff.tif")
    raise HTTPException(400, "Unsupported format")

