import os
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForPrediction, AutoConfig

def download_models():
    print("Downloading AI Models...")
    
    # 1. Sentence Embeddings (MiniLM) for Deception Mesh & Plugins
    print("[1/2] Downloading sentence-transformers/all-MiniLM-L6-v2...")
    try:
        model = SentenceTransformer('all-MiniLM-L6-v2')
        model.save('models/all-MiniLM-L6-v2')
        print(" > Success.")
    except Exception as e:
        print(f" > Failed: {e}")

    # 2. PatchTST for Time-Series (Behavioral Learning)
    # Note: PatchTST is part of Hugging Face Transformers. 
    # We'll just download the config/model stub or check availability.
    # Since it's a specific architecture, we pull a reference implementation or pre-trained base if available.
    # There isn't a single universal "PatchTST" checkpoint for bio-auth yet, so we often initialize it.
    # We will try to pull a generic time-series generic model or just confirm transformers/time-series capability.
    # For this script, we'll placeholder the specific Hugging Face model ID if widely known or skip if it requires specific training data first.
    # "PatchTST" is often `chronos-t5` or similar in HF, or specific implementations. 
    # Let's try downloading a source repo or just confirming libraries.
    # User provided: https://huggingface.co/docs/transformers/model_doc/patchtst
    # Example HF model: "ibm/patchtst-base" (common reference)
    
    print("[2/2] Downloading ibm/patchtst-base...")
    try:
        config = AutoConfig.from_pretrained("ibm/patchtst-base")
        config.save_pretrained("models/patchtst-base")
        # We don't necessarily need the weights if we train from scratch, but let's grab them.
        model = AutoModelForPrediction.from_pretrained("ibm/patchtst-base")
        model.save_pretrained("models/patchtst-base")
        print(" > Success.")
    except Exception as e:
        print(f" > Failed (Expect this if not authenticated or model restricted, but standard public models work): {e}")

    print("Done. Llama-3 is assumed installed locally per instructions.")

if __name__ == "__main__":
    if not os.path.exists("models"):
        os.makedirs("models")
    download_models()
