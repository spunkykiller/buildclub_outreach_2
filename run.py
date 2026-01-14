import uvicorn
import os
import shutil

if __name__ == "__main__":
    # Ensure local_system.db exists or init it
    if not os.path.exists("local_system.db"):
        print("Initializing Database...")
        from backend.db import init_db
        init_db()
        
    print("Starting Web App at http://localhost:8001")
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8001, reload=True)
