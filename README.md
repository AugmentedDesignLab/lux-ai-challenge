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

Let's say we want to add a new "act" behavior. The acts and setups are inside the [adl](./adl) folder. You can define the act method follow any of the existing one. Make sure you give it a unique name and export it in the __init__.py file in the folder. The act must follow the following signature

adl/acts/dumb_act.py
```
def dumb_act(self, step: int, obs, remainingOverageTime: int = 60) -> Dict[str, Union[int, List[any]]]:
    pass
```

adl/__init__.py
```
...
...
from .dumb_act import *
```

Now we can update our DumbAgent's behavior in [agent_compositions.py](./adl/agent_compositions.py).

```

# region DumbAgent

class DumbAgent(BaseAgent):
    pass

DumbAgent.early_setup = early_setup_no_bid
DumbAgent.act = dumb_act

# endregion
```

Test your agent using the notebook in the root. 

# Utility methods

## BaseAgent:
1. factoriesToPlace
2. isMyTurn
3. distanceToIceLocations
4. closestIceFrom
5. distanceToOreLocations
6. closestOreFrom