from fastapi import FastAPI`n`napp = FastAPI(title="MCP AI System")`n`n@app.get("/")`ndef root():`n    return {"status": "ok"}
