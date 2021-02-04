from gym.envs.registration import register

register(
    id='2048-v0',
    entry_point='openai.gym_game.envs:CustomEnv', #TODO might need to change relative path to library game
    max_episode_steps=2000,
)
