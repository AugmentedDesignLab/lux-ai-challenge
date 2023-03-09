from .base_agent import BaseAgent
from adl.setups import *
from adl.acts import *
from adl.agent_compositions import *

class MinerAgent(BaseAgent):
    pass


# region traits

MinerAgent.early_setup = early_setup_no_bid
MinerAgent.act = miner_act

# endregion