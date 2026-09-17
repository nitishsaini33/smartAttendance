"""
HuggingFace Space Model Client
Replaces local InsightFace by calling the remote Gradio Space:
  https://huggingface.co/spaces/nitishsaini44/baffaloL_model
"""

import json
import tempfile
import os
import numpy as np

from gradio_client import Client, handle_file


HF_SPACE_ID = "nitishsaini44/baffaloL_model"
HF_SPACE_URL = "https://nitishsaini44-baffalol-model.hf.space"


class HFSpaceModel:
    """
    Wrapper around the remote HuggingFace Gradio Space for face embedding extraction.
    
    Usage:
        model = HFSpaceModel()
        faces = model.get_faces(image_bytes)
        # faces is a list of dicts: [{"embedding": [...512 floats...]}, ...]
    """

    def __init__(self):
        print(f"Connecting to HuggingFace Space: {HF_SPACE_ID}")
        # Connect to the Gradio Space (uses the persistent hf.space URL)
        self.client = Client(HF_SPACE_URL)
        print("HuggingFace Space client initialized successfully!")

    def get_faces(self, image_bytes: bytes) -> list:
        """
        Send raw image bytes to the HF Space and get back face data.

        Args:
            image_bytes: Raw image bytes (JPEG/PNG).

        Returns:
            List of face dicts, each containing at minimum:
                {"embedding": [float, ...]}
            Returns empty list if no faces detected or on error.
        """
        tmp_path = None
        try:
            # Write bytes to a temp file so gradio_client can upload it
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
                tmp.write(image_bytes)
                tmp_path = tmp.name

            # Call the /predict endpoint on the HF Space
            result_string = self.client.predict(
                image=handle_file(tmp_path),
                api_name="/predict"
            )

            # The Space returns a JSON string
            if not result_string:
                print("[HFModel] Empty response from HF Space")
                return []

            result = json.loads(result_string)

            # Normalise response to a list of face dicts with "embedding" key
            faces = self._parse_response(result)
            print(f"[HFModel] Received {len(faces)} face(s) from HF Space")
            return faces

        except json.JSONDecodeError as e:
            print(f"[HFModel] JSON parse error: {e}. Raw: {result_string!r}")
            return []
        except Exception as e:
            print(f"[HFModel] Error calling HF Space: {e}")
            return []
        finally:
            # Clean up temp file
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass

    def _parse_response(self, result) -> list:
        """
        Normalise the HF Space response into a consistent list of face dicts.

        The Space may return:
          - A list of face objects: [{"embedding": [...], ...}, ...]
          - A single face dict:     {"embedding": [...], ...}
          - A dict with a "faces" key: {"faces": [...], ...}
          - A list of raw embedding arrays: [[...], ...]

        Returns a list of dicts with at minimum {"embedding": np.ndarray}.
        """
        faces = []

        if isinstance(result, list):
            for item in result:
                if isinstance(item, dict) and "embedding" in item:
                    emb = np.array(item["embedding"], dtype=np.float32)
                    faces.append({"embedding": emb})
                elif isinstance(item, (list, np.ndarray)):
                    # Raw embedding array in a list
                    emb = np.array(item, dtype=np.float32)
                    faces.append({"embedding": emb})

        elif isinstance(result, dict):
            # Could be {"faces": [...]} or a single face {"embedding": [...]}
            if "faces" in result:
                for item in result["faces"]:
                    if isinstance(item, dict) and "embedding" in item:
                        emb = np.array(item["embedding"], dtype=np.float32)
                        faces.append({"embedding": emb})
            elif "embedding" in result:
                emb = np.array(result["embedding"], dtype=np.float32)
                faces.append({"embedding": emb})

        return faces
