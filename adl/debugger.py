from adl.stats.map_stats import ClusterType, MapStats
from adl.utils import Utils
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
    
    def printMapStats(self, mapStats: MapStats):
        print("nIceTiles:", mapStats.nIceTiles)
        print("nOreTiles:", mapStats.nOreTiles)
        print("nTotalRubble:", mapStats.nTotalRubble)
        print("nHighRubble:", mapStats.nHighRubble)
        print("nLowRubble:", mapStats.nLowRubble)
        print("factoriesPerPlayer:", mapStats.factoriesPerPlayer)
        print("resourcePerPlayer:", mapStats.resourcePerPlayer)
        print("costLichen:", mapStats.costLichen)
        print("costLight:", mapStats.costLight)
        print("costHeavy:", mapStats.costHeavy)
        print("costFactory:", mapStats.costFactory)
        print("chargeFactory:", mapStats.chargeFactory)
        print("chargeLight:", mapStats.chargeLight)
        print("chargeHeavy:", mapStats.chargeHeavy)
        
        print("Ice Clusters:")
        self.printClusters(mapStats.iceClusters)
        print("Ore Clusters:")
        self.printClusters(mapStats.oreClusters)
        print("Resource Clusters:")
        self.printClusters(mapStats.resourceClusters)

    def printClusters(self, clusters: ClusterType):
        for center, info in clusters.items():
            # print(info)
            print(" center:", center)
            if "ice" in info:
                print("\tice:", info['ice'])
                print("\tclosest_ice:", info['closest_ice'])
                print("\tclosest_ice_distance:", Utils.distance(center, info['closest_ice']))
            if "ore" in info:
                print("\tore:", info['ore'])
                print("\tclosest_ore:", info['closest_ore'])
                print("\tclosest_ore_distance:", Utils.distance(center, info['closest_ore']))
                
            if "rubble" in info:
                print("\trubble:", info['rubble'])
                # print("\tclosest_ore:", info['closest_ore'])
                # print("\tclosest_ore_distance:", Utils.distance(center, info['closest_ore']))
