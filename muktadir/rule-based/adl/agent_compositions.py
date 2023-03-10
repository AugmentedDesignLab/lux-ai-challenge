from .base_agent import BaseAgent
from adl.setups import *
from adl.acts import *
from adl.agent_compositions import *

# region MinerAgent

class MinerAgent(BaseAgent):
    pass

MinerAgent.early_setup = early_setup_no_bid
MinerAgent.act = miner_act

# endregion