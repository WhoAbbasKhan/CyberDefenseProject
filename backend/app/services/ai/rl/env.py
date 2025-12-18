import gymnasium as gym
from gymnasium import spaces
import numpy as np

class SecurityEnv(gym.Env):
    """
    Custom Environment that follows gym interface.
    State: [Risk Score (0-100), Anomaly Score (-1 to 1), Kill Chain Stage (0-7)]
    Actions: 0=Monitor, 1=Block IP, 2=Step-Up Auth, 3=Isolate User
    """
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(SecurityEnv, self).__init__()
        # Actions: 4 discrete actions
        self.action_space = spaces.Discrete(4)
        
        # Observation: Risk(0-100), Anomaly(-1.0 to 1.0), Stage(0-7)
        self.observation_space = spaces.Box(
            low=np.array([0, -1.0, 0]), 
            high=np.array([100, 1.0, 7]),
            dtype=np.float32
        )
        
        self.state = None
        self.steps_left = 50

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        # Random initial state for training simulation
        self.state = np.array([
            np.random.randint(0, 50), # Low initial risk
            np.random.uniform(-0.5, 0.5), # Normal anomaly
            0 # Recon stage
        ], dtype=np.float32)
        self.steps_left = 50
        return self.state, {}

    def step(self, action):
        risk, anomaly, stage = self.state
        reward = 0
        terminated = False
        truncated = False
        
        # Simulation Logic
        # Action 0: Monitor (Passive)
        if action == 0:
            # Risk naturally increases if under attack (simulated)
            if np.random.rand() > 0.7:
                risk += 10
                stage = min(7, stage + 1)
                reward -= 5 # Penalty for letting attack grow
            else:
                reward += 1 # Reward for stability

        # Action 1: Block IP (Aggressive)
        elif action == 1:
            if risk > 80 or stage > 5:
                reward += 50 # Great decision!
                # Attack stopped
                risk = 0
                stage = 0
                terminated = True
            else:
                reward -= 20 # Penalty for false positive blocking
        
        # Action 2: Step-Up Auth (Moderate)
        elif action == 2:
            if risk > 50:
                 reward += 10
                 risk = max(0, risk - 20) # Mitigated
            else:
                 reward -= 5 # Annoying user

        # Update State
        self.state = np.array([min(100, risk), anomaly, stage], dtype=np.float32)
        self.steps_left -= 1
        
        if self.steps_left <= 0:
            truncated = True
            
        return self.state, reward, terminated, truncated, {}
