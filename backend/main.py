# backend/main.py
import uvicorn
from settings import API_BASE_URL

if __name__ == "__main__":
    port = int(API_BASE_URL.split(":")[-1])
    # 这里指向 api/__init__.py 里的 app
    uvicorn.run("backend.api:app", host="0.0.0.0", port=port, reload=True)