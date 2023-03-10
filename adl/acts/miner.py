import numpy as np
from lux.kit import obs_to_game_state, GameState, EnvConfig, Team
from lux.utils import direction_to, my_turn_to_place_factory

def miner_act(self, step: int, obs, remainingOverageTime: int = 60):
    actions = dict()
    game_state = obs_to_game_state(step, self.env_cfg, obs)
    factories = game_state.factories[self.player]
    game_state.teams[self.player].place_first
    factory_tiles, factory_units = [], []
    for unit_id, factory in factories.items():
        if factory.can_build_heavy(game_state):
            actions[unit_id] = factory.build_heavy()
            self.logger.info("{self.player} Building a heavy")
        if self.env_cfg.max_episode_length - game_state.real_env_steps < 50:
            if factory.water_cost(game_state) <= factory.cargo.water:
                actions[unit_id] = factory.water()
        factory_tiles += [factory.pos]
        factory_units += [factory]
    factory_tiles = np.array(factory_tiles)

    units = game_state.units[self.player]
    # ice_map = game_state.board.ice
    # ice_tile_locations = np.argwhere(ice_map == 1)
    ice_tile_locations = self.iceLocations

    for unit_id, unit in units.items():

        # track the closest factory
        closest_factory = None
        adjacent_to_factory = False
        if len(factory_tiles) > 0:
            factory_distances = np.mean((factory_tiles - unit.pos) ** 2, 1)
            closest_factory_tile = factory_tiles[np.argmin(factory_distances)]
            closest_factory = factory_units[np.argmin(factory_distances)]
            adjacent_to_factory = np.mean((closest_factory_tile - unit.pos) ** 2) == 0

            # previous ice mining code
            if unit.cargo.ice < 40:
                # ice_tile_distances = np.mean((ice_tile_locations - unit.pos) ** 2, 1)
                # ice_tile_distances = self.distanceToIceLocations(unit.pos)
                # closest_ice_tile = ice_tile_locations[np.argmin(ice_tile_distances)]
                closest_ice_tile = self.closestIceFrom(unit.pos)
                if np.all(closest_ice_tile == unit.pos):
                    if unit.power >= unit.dig_cost(game_state) + unit.action_queue_cost(game_state):
                        actions[unit_id] = [unit.dig(repeat=0)]
                else:
                    direction = direction_to(unit.pos, closest_ice_tile)
                    move_cost = unit.move_cost(game_state, direction)
                    if move_cost is not None and unit.power >= move_cost + unit.action_queue_cost(game_state):
                        actions[unit_id] = [unit.move(direction, repeat=0)]
            # else if we have enough ice, we go back to the factory and dump it.
            elif unit.cargo.ice >= 40:
                direction = direction_to(unit.pos, closest_factory_tile)
                if adjacent_to_factory:
                    if unit.power >= unit.action_queue_cost(game_state):
                        actions[unit_id] = [unit.transfer(direction, 0, unit.cargo.ice, repeat=0)]
                else:
                    move_cost = unit.move_cost(game_state, direction)
                    if move_cost is not None and unit.power >= move_cost + unit.action_queue_cost(game_state):
                        actions[unit_id] = [unit.move(direction, repeat=0)]
    return actions