"""Prediction logic for the machine learning client."""


def predict_letter(frames):
    """Return a (letter, confidence) prediction for a list of frames.

    Placeholder until the real model is added. Raise ValueError for invalid
    input so the /predict route can return a 400 response.
    """
    if not frames:
        raise NotImplementedError(f"model not implemented yet ({len(frames)} frames)")
    return "S", 0.95  # stub
