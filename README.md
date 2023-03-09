# Compositional Agents

The idea of the repository is that we can compose agents with different behaviors written by authors and reduce code overlap. In the [agent.py ](./agent.py) file, we have only two lines of code:
```
from adl.agent_compositions import *

Agent = MinerAgent
```

So, we are composing our Agent class with another agent called MinerAgent. One can write a new Agent class without modifying any existing code! Let assume we want a new Agent called the DumbAgent. Our DumbAgent will also be a composition of two distinct behaviors.

1. early setup behavior: acts in the early phase of the game where we place the factories.
2. act behavior: acts during the 1000 steps of the game play.

Agent compositions are so light that we can have a hundred different agents in a single file. Let's add our composition to [agent_compositions.py](./adl/agent_compositions.py). If you look at the code below, the agent does not define the behaviors. Instead, they reuse some existing behavior.

```
# region DumbAgent

class DumbAgent(BaseAgent):
    pass

DumbAgent.early_setup = early_setup_no_bid
DumbAgent.act = miner_act

# endregion
```

Let's say we want to add a new "act" behavior.