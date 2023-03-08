from lux.kit import obs_to_game_state, GameState, EnvConfig
from lux.utils import direction_to, my_turn_to_place_factory
import numpy as np
import sys
import logging
from adl.base_agent import BaseAgent
from adl.early_setup_traits import *
from adl.acts import *
from adl.agent_compositions import *

# class Agent(BaseAgent):
#     pass


# # region traits

# Agent.early_setup = early_setup_no_bid
# Agent.act = miner_act

# endregion

Agent = MinerAgent
