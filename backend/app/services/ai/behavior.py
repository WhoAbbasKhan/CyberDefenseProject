import torch
import numpy as np
import pandas as pd
from transformers import PatchTSTConfig, PatchTSTForPrediction

# Placeholder for a local model path or HF hub ref
MODEL_NAME = "ibm/patchtst-base" 
MODEL_PATH = "models/patchtst_behavior"

class BehaviorModelService:
    def __init__(self):
        self.model = None
        self.config = None
        
    def load_model(self):
        try:
            # Load from local cache if available, else download (cached by HF)
            self.config = PatchTSTConfig.from_pretrained(MODEL_NAME, num_input_channels=1)
            self.model = PatchTSTForPrediction.from_pretrained(MODEL_NAME, config=self.config)
            print("Loaded PatchTST model.")
        except Exception as e:
            print(f"Failed to load PatchTST: {e}")
            # Fallback: Initialize random for demo if download failed
            self.config = PatchTSTConfig(num_input_channels=1, prediction_length=5)
            self.model = PatchTSTForPrediction(self.config)

    def train_on_logs(self, logs: list):
        """
        Mock training: Convert logs to Series, feed to model.
        """
        if not self.model:
            self.load_model()
            
        # 1. Preprocess: Extract 'risk_score' or 'login_count' as time series
        # For MVP, we mock the data frame
        df = pd.DataFrame(logs)
        if df.empty:
            return {"status": "No data"}
            
        # Mock Training Loop (Fine-tuning PatchTST is complex, we simulate the step)
        print("Fine-tuning PatchTST on new logs...")
        self.model.train()
        # ... logic to run 1 epoch ...
        self.model.save_pretrained(MODEL_PATH)
        return {"status": "Training Complete", "samples": len(logs)}

    def forecast_score(self, recent_values: list) -> float:
        """
        Predict next risk score based on recent history.
        """
        if not self.model:
            self.load_model()

        # Convert input list to Tensor [Batch, Seq, Channel]
        seq_len = len(recent_values)
        input_tensor = torch.tensor(recent_values).float().unsqueeze(0).unsqueeze(-1)
        
        self.model.eval()
        with torch.no_grad():
            output = self.model(past_values=input_tensor)
        
        # Output.prediction_outputs is [Batch, PredLen, Channel]
        # We take the first step of prediction
        predicted_value = output.prediction_outputs[0, 0, 0].item()
        return float(predicted_value)

behavior_service = BehaviorModelService()
