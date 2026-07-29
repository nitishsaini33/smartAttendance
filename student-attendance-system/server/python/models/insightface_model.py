# models/insightface_model.py
from insightface.app import FaceAnalysis

def load_model():
    # Using buffalo_s instead of buffalo_l (Large) to save memory
    app = FaceAnalysis(name="buffalo_s", providers=['CPUExecutionProvider'])
    try:
        # try GPU (ctx_id=0), fall back to CPU (ctx_id=-1) if unavailable
        app.prepare(ctx_id=0, det_size=(640, 640))
    except Exception:
        app.prepare(ctx_id=-1, det_size=(640, 640))
    return app
