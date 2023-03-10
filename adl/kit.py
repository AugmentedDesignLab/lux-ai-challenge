import numpy as np
from lux.unit import Unit
from dataclasses import dataclass, field
from typing import Dict
import numpy as np
from lux.cargo import UnitCargo
from lux.config import EnvConfig
from lux.team import Team, FactionTypes
from lux.unit import Unit
from lux.factory import Factory
from lux.kit import GameState, Board

def animate(imgs, _return=True):
    # using cv2 to generate videos as moviepy doesn't work on kaggle notebooks
    import cv2
    import os
    import string
    import random
    video_name = ''.join(random.choice(string.ascii_letters) for i in range(18))+'.webm'
    height, width, layers = imgs[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'VP90')
    video = cv2.VideoWriter(video_name, fourcc, 10, (width,height))

    for img in imgs:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        video.write(img)
    video.release()
    if _return:
        from IPython.display import Video
        return Video(video_name)
def interact(env, agents, steps):
    # reset our env
    obs = env.reset(seed=1)
    np.random.seed(0)
    imgs = []
    step = 0
    # Note that as the environment has two phases, we also keep track a value called 
    # `real_env_steps` in the environment state. The first phase ends once `real_env_steps` is 0 and used below

    # iterate until phase 1 ends
    while env.state.real_env_steps < 0:
        if step >= steps: break
        actions = {}
        for player in env.agents:
            o = obs[player]
            # print(f"early setup {player} at step {step}")
            a = agents[player].early_setup(step, o)
            actions[player] = a
        step += 1
        obs, rewards, dones, infos = env.step(actions)
        imgs += [env.render("rgb_array", width=640, height=640)]
    done = False
    while not done:
        if step >= steps: break
        actions = {}
        for player in env.agents:
            o = obs[player]
            a = agents[player].act(step, o)
            actions[player] = a
        step += 1
        obs, rewards, dones, infos = env.step(actions)
        imgs += [env.render("rgb_array", width=640, height=640)]
        done = dones["player_0"] and dones["player_1"]
    # print(env.state.real_env_steps)
    return animate(imgs), obs


def obs_to_game_state_fast(step, env_cfg: EnvConfig, obs, prevState: GameState):
    
    units = dict()
    for agent in obs["units"]:
        units[agent] = dict()
        for unit_id in obs["units"][agent]:
            unit_data = obs["units"][agent][unit_id]
            cargo = UnitCargo(**unit_data["cargo"])
            unit = Unit(
                **unit_data,
                unit_cfg=env_cfg.ROBOTS[unit_data["unit_type"]],
                env_cfg=env_cfg
            )
            unit.cargo = cargo
            units[agent][unit_id] = unit
            

    factory_occupancy_map = np.ones_like(obs["board"]["rubble"], dtype=int) * -1 # TODO can be cached
    factories = dict() # factories should be updated and removed
    for agent in obs["factories"]:
        factories[agent] = dict()
        for unit_id in obs["factories"][agent]:
            f_data = obs["factories"][agent][unit_id]
            cargo = UnitCargo(**f_data["cargo"])
            factory = Factory(
                **f_data,
                env_cfg=env_cfg
            )
            factory.cargo = cargo
            factories[agent][unit_id] = factory
            factory_occupancy_map[factory.pos_slice] = factory.strain_id
    teams = dict()
    for agent in obs["teams"]:
        team_data = obs["teams"][agent]
        faction = FactionTypes[team_data["faction"]]
        teams[agent] = Team(**team_data, agent=agent) # teams TODO should be updated

    return GameState(
        env_cfg=env_cfg,
        env_steps=step,
        board=Board(
            rubble=obs["board"]["rubble"],
            ice=obs["board"]["ice"],
            ore=obs["board"]["ore"],
            lichen=obs["board"]["lichen"],
            lichen_strains=obs["board"]["lichen_strains"],
            factory_occupancy_map=factory_occupancy_map,
            factories_per_team=obs["board"]["factories_per_team"],
            valid_spawns_mask=obs["board"]["valid_spawns_mask"]
        ),
        units=units,
        factories=factories,
        teams=teams

    )