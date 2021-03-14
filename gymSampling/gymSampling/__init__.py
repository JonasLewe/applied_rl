from gym.envs.registration import register

register(
    id="GymSampling-v0",
    entry_point="gymSampling.envs.gymSampling:GymSampling",
    max_episode_steps=500,
)