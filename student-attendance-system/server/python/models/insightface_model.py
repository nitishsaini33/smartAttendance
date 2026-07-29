import os
from insightface.app import FaceAnalysis

def load_model():
    # Using buffalo_sc (Scratch) instead of buffalo_s to save memory and stay under Render's 512MB limit.
    # buffalo_s physically cannot fit in 512MB RAM, even with aggressive ONNX optimizations, 
    # because the base weights + Python interpreter overhead exceed the limit.
    app = FaceAnalysis(name="buffalo_sc", providers=['CPUExecutionProvider'])
    
    try:
        # try GPU (ctx_id=0), fall back to CPU (ctx_id=-1) if unavailable
        app.prepare(ctx_id=0, det_size=(640, 640))
    except Exception:
        app.prepare(ctx_id=-1, det_size=(640, 640))
        
    return app
