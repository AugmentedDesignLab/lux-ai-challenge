from lux.factory import Factory
from lux.unit import Unit
from lux.kit import obs_to_game_state, GameState, EnvConfig, Team
from typing import *

class Debugger:
    
    def printTeam(self, team: Team):
        print("faction:", team.faction)
        print("\tteam_id:", team.team_id)
        print("\tagent:", team.agent)
        print("\twater:", team.water)
        print("\tmetal:", team.metal) 
        print("\tfactories_to_place:", team.factories_to_place) 
        print("\tfactory_strains:", team.factory_strains) 
        
    def printFactories(self, factories: Dict[str, Factory]):
        print("#factories:", len(factories))
        for unit_id, factory in factories.items():
            # print("\tteam_id:", factory.team_id)
            print("\tunit_id:", factory.unit_id)
            print("\tstrain_id:", factory.strain_id)
            print("\tpower:", factory.power)
            print("\tcargo:", factory.cargo)
            print("\tpos:", factory.pos)
    
    def printUnits(self, units: Dict[str, Unit]):
        print("#units:", len(units))
        for unit_id, unit in units.items():
            # print("\tteam_id:", unit.team_id)
            print("\tunit_id:", unit.unit_id)
            print("\tunit_type:", unit.unit_type)
            print("\tpower:", unit.power)
            print("\tcargo:", unit.cargo)
            print("\tpos:", unit.pos)
            print("\tunit_cfg:", unit.unit_cfg)
            print("\taction_queue:", unit.action_queue)
        

    def printStateFromState(self, game_state, agentPlayerName):
        # print(game_state.factories[agentPlayerName])
        self.printTeam(game_state.teams[agentPlayerName])
        self.printFactories(game_state.factories[agentPlayerName])
        self.printUnits(game_state.units[agentPlayerName])
        
    def printAgentStates(self, agent, step, obs):
        game_state = obs_to_game_state(step, agent.env_cfg, obs)
        self.printStateFromState(game_state, agent.player)
    
    def printOpponentStates(self, agent, step, obs):
        game_state = obs_to_game_state(step, agent.env_cfg, obs)
        self.printStateFromState(game_state, agent.opp_player)