import util
from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True, slots=True)
class Resources:
    ore: int
    clay: int
    obsidian: int
    geode: int

    def __add__(self, other: "Resources"):
        return Resources(ore=self.ore+other.ore, clay=self.clay+other.clay, obsidian=self.obsidian+other.obsidian, geode=self.geode+other.geode)

    def __sub__(self, other: "Resources"):
        return Resources(ore=self.ore-other.ore, clay=self.clay-other.clay, obsidian=self.obsidian-other.obsidian, geode=self.geode-other.geode)

    def has(self, other: "Resources"):
        return self.ore >= other.ore and self.clay >= other.clay and self.obsidian >= other.obsidian and self.geode >= self.geode


one_ore = Resources(ore=1, clay=0, obsidian=0, geode=0)
one_clay = Resources(ore=0, clay=1, obsidian=0, geode=0)
one_obsidian = Resources(ore=0, clay=0, obsidian=1, geode=0)
one_geode = Resources(ore=0, clay=0, obsidian=0, geode=1)
zeros = Resources(ore=0, clay=0, obsidian=0, geode=0)


cache = {}

max_costs = {}


def max_geodes(minute: int, resources: Resources, robots: Resources, costs: Dict[str, Resources]) -> int:
    minutes_remaining = 33 - minute
    if minutes_remaining == 0:
        return resources.geode

    N = minutes_remaining+1
    upper_bound_obsidian = resources.obsidian + robots.obsidian * (minutes_remaining) + (N+1) * (N+2) // 2

    if upper_bound_obsidian < costs["geode"].obsidian:
        return resources.geode

    ore_cost = costs["ore"]
    clay_cost = costs["clay"]
    obsidian_cost = costs["obsidian"]
    geode_cost = costs["geode"]
    key = (minute, resources, robots)
    if key in cache:
        return cache[key]
    if resources.has(geode_cost):
        paths = [(max_geodes(minute + 1, resources - geode_cost + robots, robots + one_geode, costs))]
    else:
        paths = [max_geodes(minute + 1, resources + robots, robots, costs)]
        if robots.ore < max_costs["ore"] and resources.has(ore_cost):
            paths.append(max_geodes(minute + 1, resources - ore_cost + robots, robots + one_ore, costs))
        if robots.clay < max_costs["clay"] and resources.has(clay_cost):
            paths.append(max_geodes(minute + 1, resources - clay_cost + robots, robots + one_clay, costs))
        if robots.obsidian < max_costs["obsidian"] and resources.has(obsidian_cost):
            paths.append(max_geodes(minute + 1, resources - obsidian_cost + robots, robots + one_obsidian, costs))

    geodes = max(paths)
    cache[key] = geodes
    return geodes


blue_prints = []
for line in util.read_lines("inputs/day19.txt"):
    _, ore_ore, clay_ore, obsidian_ore, obsidian_clay, geode_ore, geode_obsidian = util.extract_ints(line)
    costs = {
        "ore": Resources(ore=ore_ore, clay=0, obsidian=0, geode=0),
        "clay": Resources(ore=clay_ore, clay=0, obsidian=0, geode=0),
        "obsidian": Resources(ore=obsidian_ore, clay=obsidian_clay, obsidian=0, geode=0),
        "geode": Resources(ore=geode_ore, clay=0, obsidian=geode_obsidian, geode=0),
    }
    blue_prints.append(costs)

ans = 1
for index, blue_print in enumerate(blue_prints[0:3]):
    cache.clear()
    max_costs["ore"] = max(cost.ore for cost in blue_print.values())
    max_costs["clay"] = max(cost.clay for cost in blue_print.values())
    max_costs["obsidian"] = max(cost.obsidian for cost in blue_print.values())

    geodes = max_geodes(minute=1, resources=zeros, robots=one_ore, costs=blue_print)
    ans *= geodes

print(ans)
