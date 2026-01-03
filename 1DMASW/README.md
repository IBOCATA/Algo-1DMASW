# 1DMASW Platform

## Overview

1DMASW is a Platform as a Service (PaaS) solution for seismic data processing. It integrates:

- **Stripe** for payment processing
- **PayPal** for alternative payment options
- **PDF Invoice Generation** for transaction records

## Features

- Secure payment processing with Stripe and PayPal
- Automated PDF invoice generation
- Deployable on Render.com

## Setup

1. Clone the repository:

# 1DMASW – Cloud-Native Seismic Imaging Platform

**1DMASW** is a Platform-as-a-Service (PaaS) that enables online seismic imaging, analysis, and inversion using state-of-the-art geophysical libraries and scalable cloud infrastructure.

> 🌍 *Revolutionizing subsurface imaging for geoscientists, engineers, and researchers through Devito, SimPEG, and Madagascar.*

---

## 🚀 Key Features

- 🔍 SEG-Y file upload and visualization (2D/3D)
- 🧠 Full Waveform Inversion (FWI) with Devito
- 🌐 Travel-time tomography with SimPEG
- 🛠️ Bragg scattering + RSF support with Madagascar
- 📦 Asynchronous job processing with Celery & Redis
- 🔐 Secured REST API with OAuth2 + JWT
- 📈 Web interface powered by FastAPI and React

---

## 📊 Pitch Deck Overview

### 🔹 [1DMASW Pitch Summary](#)
> (*Link to hosted pitch deck or attach PDF if in GitHub repo*)

| Slide | Title                     | Summary                                                  |
|-------|---------------------------|----------------------------------------------------------|
| 1     | Cover Slide               | Tagline, logo, contact                                   |
| 2     | Problem Statement         | Bottlenecks in current seismic imaging methods           |
| 3     | Our Solution              | Unified cloud-native platform                            |
| 4     | Demo                      | Upload, process, visualize SEG-Y                         |
| 5     | Technology Stack          | Devito, SimPEG, FastAPI, Docker, Celery                  |
| 6     | Market Opportunity        | $5B+ seismic software industry                           |
| 7     | Business Model            | Freemium + HPC usage fees                                |
| 8     | Competitive Advantage     | Integration, UX, scalability                             |
| 9     | Traction                  | Beta users, partnerships, pilots                         |
| 10    | Go-to-Market              | Research, energy, environment                            |
| 11    | Team                      | Founders + advisors                                      |
| 12    | Financials                | Projected growth over 3 years                            |
| 13    | Ask                       | $1M seed round                                            |

---

## 🧱 Architecture

[User] → [React Frontend] → [FastAPI + OAuth2] → [Celery Workers]
↓
[Devito | SimPEG | Madagascar]
↓
[PostgreSQL + S3]

yaml
Copier
Modifier

---

## 🛠️ Setup & Installation

### ⚙️ Prerequisites

- Docker & Docker Compose
- Python 3.10+ (for local dev)

### 📦 Launching with Docker

```bash
git clone https://github.com/your-org/1dmasw.git
cd 1dmasw
docker-compose up --build
🎯 Endpoints
POST /upload/ – Upload SEG-Y file

POST /run/devito – Start Devito FWI

POST /run/madagascar – Start Madagascar inversion

POST /token – Get access token

GET /secure-endpoint – Auth-protected test route

🔐 Authentication
Use /token to authenticate with username/password and receive a JWT:

bash
Copier
Modifier
curl -X POST -d "username=admin&password=pass" http://localhost:8000/token
🧪 Testing
Install test tools:

bash
Copier
Modifier
pip install pytest httpx pytest-asyncio
Run tests:

bash
Copier
Modifier
pytest backend/tests
📁 Project Structure
bash
Copier
Modifier
backend/
├── main.py         ← FastAPI app
├── tasks.py        ← Celery tasks
├── inversion/      ← Devito, SimPEG, Madagascar functions
├── tests/          ← Unit & integration tests
└── auth.py         ← OAuth2/JWT
📜 License
MIT License © 2025 1DMASW Team

🤝 Contact
For business inquiries or collaborations:

📧 iliasbounsir@gmail.com
🌐 1dmasw.b12sites.com
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)