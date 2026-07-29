import os
from insightface.app import FaceAnalysis

def load_model():
    # 1. Disable memory arenas and restrict threads to save memory
    os.environ["ORT_DISABLE_ALL_ARENAS"] = "1"
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"

    # 2. Use buffalo_s, but ONLY load the modules we need (detection & recognition). 
    # This skips loading the GenderAge and 3D Landmark models, saving ~40% RAM.
    app = FaceAnalysis(
        name="buffalo_s", 
        allowed_modules=['detection', 'recognition'],
        providers=['CPUExecutionProvider']
    )
    
    try:
        # 3. Reduce det_size to 320x320 (from 640x640).
        # This drastically reduces the memory allocated for images during inference.
        app.prepare(ctx_id=-1, det_size=(320, 320))
    except Exception:
        app.prepare(ctx_id=-1, det_size=(320, 320))
        
    return app
