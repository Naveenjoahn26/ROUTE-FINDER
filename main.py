from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from schemas.request_models import RouteRequest
from services.route_service import find_route, _load_graph
import os

app = FastAPI(title="SafeRoute AI | Intelligent Navigation Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")

@app.on_event("startup")
def startup_event():
    """Pre-warm road network graph and model on server start for instantaneous route queries."""
    try:
        print("[Startup] Pre-loading road network graph...")
        _load_graph()
        print("[Startup] SafeRoute AI Backend is ready!")
    except Exception as e:
        print(f"[Startup Warning] Could not pre-warm graph: {e}")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    favicon_path = os.path.join(FRONTEND_DIR, "favicon.ico")
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path)
    return Response(status_code=204)

@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}

@app.post("/predict")
def predict_route(data: RouteRequest):
    try:
        results = find_route(
            data.start_lat,
            data.start_lon,
            data.end_lat,
            data.end_lon
        )
        
        # If both routes are None, the selected points are unreachable
        if not results.get("safe_route") and not results.get("short_route"):
            raise HTTPException(
                status_code=422,
                detail="No walkable path found between the selected points. Try selecting points closer to roads."
            )

        return results
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"[ERROR] /predict failed: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal routing error: {str(e)}")

# Serve frontend at root and /static
if os.path.isdir(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def home():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Sentinel AI Routing Backend Running"}

# Static files fallback for style.css, app.js at root level
if os.path.isdir(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend_root")
