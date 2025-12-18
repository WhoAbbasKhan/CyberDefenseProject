import os
import numpy as np
from stable_baselines3 import PPO
from app.services.ai.rl.env import SecurityEnv

MODEL_PATH = "models/ppo_defense_agent"

class ResponseAgent:
    def __init__(self):
        self.model = None
        self.env = SecurityEnv()

    def train(self, total_timesteps=10000):
        """Train a new agent from scratch."""
        print("Training Autonomous Response Agent...")
        model = PPO("MlpPolicy", self.env, verbose=1)
        model.learn(total_timesteps=total_timesteps)
        
        if not os.path.exists("models"):
            os.makedirs("models")
        
        model.save(MODEL_PATH)
        self.model = model
        print(f"Model saved to {MODEL_PATH}")

    def load(self):
        """Load pretrained agent."""
        if os.path.exists(f"{MODEL_PATH}.zip"):
            self.model = PPO.load(MODEL_PATH)
            print("Loaded PPO Agent.")
        else:
            print("No model found. Training new one...")
            self.train()

    def decide(self, risk_score: float, anomaly_score: float, kill_chain_stage: int) -> str:
        """
        Predict optimal action based on security state.
        Returns: ACTION_NAME
        """
        if not self.model:
            self.load()
            
        obs = np.array([risk_score, anomaly_score, kill_chain_stage], dtype=np.float32)
        action, _states = self.model.predict(obs, deterministic=True)
        
        actions_map = {
            0: "MONITOR",
            1: "BLOCK_IP",
            2: "STEP_UP_AUTH",
            3: "ISOLATE_USER"
        }
        return actions_map.get(int(action), "MONITOR")

# Global Instance
agent = ResponseAgent()
