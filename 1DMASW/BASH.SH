1dmasw/
│
├── backend/
│   ├── main.py                # FastAPI
│   ├── tasks.py               # Celery tasks
│   ├── Dockerfile
│   └── requirements.txt
│
├── worker/
│   └── Dockerfile             # Pour Madagascar + Celery worker
│
├── uploads/                   # Stockage des fichiers SEG-Y
├── processed/                 # Résultats
├── docker-compose.yml
└── README.md
