import gym
from gym import spaces
import numpy as np
import pandas as pd
from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import DummyVecEnv
from .base import Strategy

class TradingEnv(gym.Env):
    """Custom Gym environment for trading."""
    def __init__(self, data: pd.DataFrame):
        super(TradingEnv, self).__init__()
        self.data = data
        self.current_step = 0
        self.action_space = spaces.Discrete(3)  # 0: hold, 1: buy, 2: sell
        self.observation_space = spaces.Box(low=0, high=1, shape=(len(data.columns),), dtype=np.float32)
        self.position = 0  # 0: no position, 1: long, -1: short
        self.cash = 10000
        self.asset = 0

    def reset(self):
        self.current_step = 0
        self.position = 0
        self.cash = 10000
        self.asset = 0
        return self._get_observation()

    def step(self, action):
        reward = 0
        done = False
        if action == 1 and self.position == 0:  # Buy
            self.position = 1
            self.asset = self.cash / self.data['close'].iloc[self.current_step]
            self.cash = 0
        elif action == 2 and self.position == 1:  # Sell
            self.position = 0
            self.cash = self.asset * self.data['close'].iloc[self.current_step]
            self.asset = 0
            reward = (self.cash - 10000) / 10000  # Profit percentage

        self.current_step += 1
        if self.current_step >= len(self.data):
            done = True

        return self._get_observation(), reward, done, {}

    def _get_observation(self):
        return self.data.iloc[self.current_step].values

class RLStrategy(Strategy):
    """Reinforcement learning-based trading strategy using DQN."""
    def __init__(self, data: pd.DataFrame):
        self.env = DummyVecEnv([lambda: TradingEnv(data)])
        self.model = DQN("MlpPolicy", self.env, verbose=1)
        self.model.learn(total_timesteps=10000)

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """Generate signals using the trained RL model."""
        obs = self.env.reset()
        signals = []
        for _ in range(len(data)):
            action, _states = self.model.predict(obs)
            signals.append(action == 1)  # Buy if action is 1
            obs, _, done, _ = self.env.step(action)
            if done:
                break
        return pd.Series(signals, index=data.index)