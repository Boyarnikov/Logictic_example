from Route import Route
import datetime


class Manager:
    points = set()
    routs = dict()

    def __init__(self):
        self.points = set()
        self.routs = dict()

    def add_point(self, point):
        self.points.add(point)

    def get_points(self):
        return self.points

    def get_routs(self):
        return self.routs

    def add_route(self, route: Route = None, point_a=None, point_b=None, ets=datetime.time(), eta=datetime.time()):
        if route is not None:
            point_a, point_b = route.get_points()
        elif point_a is not None and point_b is not None:
            route = Route(point_a, point_b, ets, eta)
        if point_a not in self.points:
            self.points.add(point_a)
        if point_b not in self.points:
            self.points.add(point_b)

        if point_a not in self.routs:
            self.routs[point_a] = list()
        self.routs[point_a].append(route)

    def find_fastest_route(self, point_a, point_b, ets=datetime.time(),
                           eta=datetime.time(hour=23, minute=59, second=59)):
        found_ways = dict()  # hub: (eta, last_route)
        found_ways[point_a] = (ets, None)

        while True:
            fastest_route = None
            fastest_ets = datetime.time(hour=23, minute=59, second=59)

            for h in found_ways.keys():
                latest_ets = found_ways[h][0]
                for r in self.routs[h]:
                    _ets, _eta = r.get_timings()
                    if latest_ets <= _ets:
                        continue
                    _from, _to = r.get_points()
                    if _to not in found_ways.keys():
                        if fastest_ets > _ets:
                            fastest_route = r
                            fastest_ets = _ets

            if fastest_route is None:
                raise Exception("Не найдена следующая вершина")

            _from, _to = fastest_route.get_points()
            _ets, _eta = fastest_route.get_timings()

            found_ways[_to] = (_eta, fastest_route)
            if _to is point_b:
                break

        if found_ways[point_b][0] > eta:
            return None

        way = list()
        current = point_b

        while found_ways[current][1] is not None:
            route = found_ways[current][1]
            current, _to = route.get_points()
            way.append(route)

        way.reverse()

        return way

    def __str__(self):
        string = "manager:\n"
        for i in self.points:
            string += f"{str(i)}\n"
        for i in self.routs:
            string += f"{str(i)}: {str(self.routs[i])}\n"
        return string
