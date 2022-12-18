import util
from dataclasses import dataclass, field
from typing import List
from itertools import product

lines = util.read_lines("inputs/day15.txt", util.extract_ints)

closest = dict()
beacons = []

for line in lines:
    sx, sy, bx, by = map(int, line)
    closest[(sx, sy)] = abs(sx-bx) + abs(sy-by)
    beacons.append((bx, by))


@dataclass
class Regions:
    sub_regions: List[List[int]] = field(default_factory=list)

    def add(self, x_min, x_max):
        if len(self.sub_regions) == 0:
            self.sub_regions.append([x_min, x_max])
            return
        added = False
        for i, (tx_min, tx_max) in enumerate(self.sub_regions):
            if x_min >= tx_min and x_min <= tx_max:
                self.sub_regions[i][1] = max(self.sub_regions[i][1], x_max)
                added = True
                break
            elif x_max >= tx_min and x_max <= tx_max:
                self.sub_regions[i][0] = min(self.sub_regions[i][0], x_min)
                added = True
                break
        if not added:
            self.sub_regions.append([x_min, x_max])

        modified = True
        while modified and len(self.sub_regions) > 1:
            N = len(self.sub_regions)
            for i, j in product(range(N), range(N)):
                if i != j and self.sub_regions[i][0] <= self.sub_regions[j][0] and self.sub_regions[i][1] >= self.sub_regions[j][0]:
                    self.sub_regions[j][0] = self.sub_regions[i][0]
                    self.sub_regions[j][1] = max(self.sub_regions[i][1], self.sub_regions[j][1])
                    self.sub_regions.pop(i)
                    modified = True
                    break
                if i != j and self.sub_regions[i][1] == self.sub_regions[j][0] - 1:
                    self.sub_regions[j][0] = self.sub_regions[i][0]
                    self.sub_regions.pop(i)
                    modified = True
                    break
            modified = False
        self.sub_regions.sort(key=lambda x: x[0])

    def search(self):
        for i in range(len(self.sub_regions) - 1):
            left = self.sub_regions[i][1]
            right = self.sub_regions[i+1][0]

            if left < right and left >= 0 and left <= 4000000 and right >= 0 and right <= 4000000:
                return left + 1
        return None


for y in range(4000000):
    regions = Regions()
    for bx, by in beacons:
        if by == y:
            regions.add(bx, bx)
    for (sx, sy), distance in closest.items():
        d = distance - abs(y-sy)
        if d >= 0:
            regions.add(sx - d, sx + d)

    x = regions.search()
    if x is not None:
        print(x * 4000000 + y)
        break
