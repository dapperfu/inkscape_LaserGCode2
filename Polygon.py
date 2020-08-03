class Polygon:
    def __init__(self, polygon=None):
        self.polygon = [] if polygon is None else polygon[:]

    def move(self, x, y):
        for i in range(len(self.polygon)):
            for j in range(len(self.polygon[i])):
                self.polygon[i][j][0] += x
                self.polygon[i][j][1] += y

    def bounds(self):
        minx, miny, maxx, maxy = 1e400, 1e400, -1e400, -1e400
        for poly in self.polygon:
            for p in poly:
                if minx > p[0]:
                    minx = p[0]
                if miny > p[1]:
                    miny = p[1]
                if maxx < p[0]:
                    maxx = p[0]
                if maxy < p[1]:
                    maxy = p[1]
        return minx * 1, miny * 1, maxx * 1, maxy * 1

    def width(self):
        b = self.bounds()
        return b[2] - b[0]

    def rotate_(self, sin, cos):
        for i in range(len(self.polygon)):
            for j in range(len(self.polygon[i])):
                x, y = self.polygon[i][j][0], self.polygon[i][j][1]
                self.polygon[i][j][0] = x * cos - y * sin
                self.polygon[i][j][1] = x * sin + y * cos

    def rotate(self, a):
        cos, sin = math.cos(a), math.sin(a)
        self.rotate_(sin, cos)

    def drop_into_direction(self, direction, surface):
        # Polygon is a list of simple polygons
        # Surface is a polygon + line y = 0
        # Direction is [dx,dy]
        if len(self.polygon) == 0 or len(self.polygon[0]) == 0:
            return
        if direction[0] ** 2 + direction[1] ** 2 < 1e-10:
            return
        direction = normalize(direction)
        sin, cos = direction[0], -direction[1]
        self.rotate_(-sin, cos)
        surface.rotate_(-sin, cos)
        self.drop_down(surface, zerro_plane=False)
        self.rotate_(sin, cos)
        surface.rotate_(sin, cos)

    def centroid(self):
        centroids = []
        sa = 0
        for poly in self.polygon:
            cx, cy, a = 0, 0, 0
            for i in range(len(poly)):
                [x1, y1], [x2, y2] = poly[i - 1], poly[i]
                cx += (x1 + x2) * (x1 * y2 - x2 * y1)
                cy += (y1 + y2) * (x1 * y2 - x2 * y1)
                a += x1 * y2 - x2 * y1
            a *= 3.0
            if abs(a) > 0:
                cx /= a
                cy /= a
                sa += abs(a)
                centroids += [[cx, cy, a]]
        if sa == 0:
            return [0.0, 0.0]
        cx, cy = 0.0, 0.0
        for c in centroids:
            cx += c[0] * c[2]
            cy += c[1] * c[2]
        cx /= sa
        cy /= sa
        return [cx, cy]

    def drop_down(self, surface, zerro_plane=True):
        # Polygon is a list of simple polygons
        # Surface is a polygon + line y = 0
        # Down means min y (0,-1)
        if len(self.polygon) == 0 or len(self.polygon[0]) == 0:
            return
        # Get surface top point
        top = surface.bounds()[3]
        if zerro_plane:
            top = max(0, top)
        # Get polygon bottom point
        bottom = self.bounds()[1]
        self.move(0, top - bottom + 10)
        # Now get shortest distance from surface to polygon in positive x=0 direction
        # Such distance = min(distance(vertex, edge)...)  where edge from surface and
        # vertex from polygon and vice versa...
        dist = 1e300
        for poly in surface.polygon:
            for i in range(len(poly)):
                for poly1 in self.polygon:
                    for i1 in range(len(poly1)):
                        st, end = poly[i - 1], poly[i]
                        vertex = poly1[i1]
                        if st[0] <= vertex[0] <= end[0] or end[0] <= vertex[0] <= st[0]:
                            if st[0] == end[0]:
                                d = min(vertex[1] - st[1], vertex[1] - end[1])
                            else:
                                d = (
                                    vertex[1]
                                    - st[1]
                                    - (end[1] - st[1])
                                    * (vertex[0] - st[0])
                                    / (end[0] - st[0])
                                )
                            if dist > d:
                                dist = d
                        # and vice versa just change the sign because vertex
                        # now under the edge
                        st, end = poly1[i1 - 1], poly1[i1]
                        vertex = poly[i]
                        if st[0] <= vertex[0] <= end[0] or end[0] <= vertex[0] <= st[0]:
                            if st[0] == end[0]:
                                d = min(-vertex[1] + st[1], -
                                        vertex[1] + end[1])
                            else:
                                d = (
                                    -vertex[1]
                                    + st[1]
                                    + (end[1] - st[1])
                                    * (vertex[0] - st[0])
                                    / (end[0] - st[0])
                                )
                            if dist > d:
                                dist = d

        if zerro_plane and dist > 10 + top:
            dist = 10 + top
        # print_(dist, top, bottom)
        # self.draw()
        self.move(0, -dist)

    def draw(self, color="#075", width=0.1):
        for poly in self.polygon:
            csp_draw([csp_subpath_line_to([], poly + [poly[0]])],
                     color=color, width=width)

    def add(self, add):
        if isinstance(add, type([])):
            self.polygon += add[:]
        else:
            self.polygon += add.polygon[:]

    def point_inside(self, p):
        inside = False
        for poly in self.polygon:
            for i in range(len(poly)):
                st, end = poly[i - 1], poly[i]
                if p == st or p == end:
                    return True  # point is a vertex = point is on the edge
                if st[0] > end[0]:
                    # This will be needed to check that edge if open only at
                    # rigth end
                    st, end = (end, st, )
                c = (p[1] - st[1]) * (end[0] - st[0]) - (end[1] - st[1]) * (
                    p[0] - st[0]
                )
                # print_(c)
                if st[0] <= p[0] < end[0]:
                    if c < 0:
                        inside = not inside
                    elif c == 0:
                        return True  # point is on the edge
                # point is on the edge
                elif st[0] == end[0] == p[0] and (
                    st[1] <= p[1] <= end[1] or end[1] <= p[1] <= st[1]
                ):
                    return True
        return inside

    def hull(self):
        # Add vertices at all self intersection points.
        hull = []
        for i1 in range(len(self.polygon)):
            poly1 = self.polygon[i1]
            poly_ = []
            for j1 in range(len(poly1)):
                s, e = poly1[j1 - 1], poly1[j1]
                poly_ += [s]

                # Check self intersections
                for j2 in range(j1 + 1, len(poly1)):
                    s1, e1 = poly1[j2 - 1], poly1[j2]
                    int_ = line_line_intersection_points(s, e, s1, e1)
                    for p in int_:
                        if (
                            point_to_point_d2(p, s) > 0.000001
                            and point_to_point_d2(p, e) > 0.000001
                        ):
                            poly_ += [p]
                # Check self intersections with other polys
                for i2 in range(len(self.polygon)):
                    if i1 == i2:
                        continue
                    poly2 = self.polygon[i2]
                    for j2 in range(len(poly2)):
                        s1, e1 = poly2[j2 - 1], poly2[j2]
                        int_ = line_line_intersection_points(s, e, s1, e1)
                        for p in int_:
                            if (
                                point_to_point_d2(p, s) > 0.000001
                                and point_to_point_d2(p, e) > 0.000001
                            ):
                                poly_ += [p]
            hull += [poly_]
        # Create the dictionary containing all edges in both directions
        edges = {}
        for poly in self.polygon:
            for i in range(len(poly)):
                s, e = tuple(poly[i - 1]), tuple(poly[i])
                if point_to_point_d2(e, s) < 0.000001:
                    continue
                break_s, break_e = False, False
                for p in edges:
                    if point_to_point_d2(p, s) < 0.000001:
                        break_s = True
                        s = p
                    if point_to_point_d2(p, e) < 0.000001:
                        break_e = True
                        e = p
                    if break_s and break_e:
                        break
                l = point_to_point_d(s, e)
                if not break_s and not break_e:
                    edges[s] = [[s, e, l]]
                    edges[e] = [[e, s, l]]
                    # draw_pointer(s+e,"red","line")
                    # draw_pointer(s+e,"red","line")
                else:
                    if e in edges:
                        for edge in edges[e]:
                            if point_to_point_d2(edge[1], s) < 0.000001:
                                break
                        if point_to_point_d2(edge[1], s) > 0.000001:
                            edges[e] += [[e, s, l]]
                            # draw_pointer(s+e,"red","line")

                    else:
                        edges[e] = [[e, s, l]]
                        # draw_pointer(s+e,"green","line")
                    if s in edges:
                        for edge in edges[s]:
                            if point_to_point_d2(edge[1], e) < 0.000001:
                                break
                        if point_to_point_d2(edge[1], e) > 0.000001:
                            edges[s] += [[s, e, l]]
                            # draw_pointer(s+e,"red","line")
                    else:
                        edges[s] = [[s, e, l]]
                        # draw_pointer(s+e,"green","line")

        def angle_quadrant(sin, cos):
            # quadrants are (0,pi/2], (pi/2,pi], (pi,3*pi/2], (3*pi/2, 2*pi],
            # i.e. 0 is in the 4-th quadrant
            if sin > 0 and cos >= 0:
                return 1
            if sin >= 0 and cos < 0:
                return 2
            if sin < 0 and cos <= 0:
                return 3
            if sin <= 0 and cos > 0:
                return 4

        def angle_is_less(sin, cos, sin1, cos1):
            # 0 = 2*pi is the largest angle
            if [sin1, cos1] == [0, 1]:
                return True
            if [sin, cos] == [0, 1]:
                return False
            if angle_quadrant(sin, cos) > angle_quadrant(sin1, cos1):
                return False
            if angle_quadrant(sin, cos) < angle_quadrant(sin1, cos1):
                return True
            if sin >= 0 and cos > 0:
                return sin < sin1
            if sin > 0 and cos <= 0:
                return sin > sin1
            if sin <= 0 and cos < 0:
                return sin > sin1
            if sin < 0 and cos >= 0:
                return sin < sin1

        def get_closes_edge_by_angle(edges, last):
            # Last edge is normalized vector of the last edge.
            min_angle = [0, 1]
            next = last
            last_edge = [
                (last[0][0] - last[1][0]) / last[2],
                (last[0][1] - last[1][1]) / last[2],
            ]
            for p in edges:
                # draw_pointer(list(p[0])+[p[0][0]+last_edge[0]*40,p[0][1]+last_edge[1]*40], "Red", "line", width=1)
                # print_("len(edges)=",len(edges))
                cur = [(p[1][0] - p[0][0]) / p[2], (p[1][1] - p[0][1]) / p[2]]
                cos, sin = dot(cur, last_edge), cross(cur, last_edge)
                # draw_pointer(list(p[0])+[p[0][0]+cur[0]*40,p[0][1]+cur[1]*40], "Orange", "line", width=1, comment = [sin,cos])
                # print_("cos, sin=",cos,sin)
                # print_("min_angle_before=",min_angle)

                if angle_is_less(sin, cos, min_angle[0], min_angle[1]):
                    min_angle = [sin, cos]
                    next = p
                # print_("min_angle=",min_angle)

            return next

        # Join edges together into new polygon cutting the vertexes inside new
        # polygon
        self.polygon = []
        len_edges = sum([len(edges[p]) for p in edges])
        loops = 0

        while len(edges) > 0:
            poly = []
            if loops > len_edges:
                raise ValueError("Hull error")
            loops += 1
            # Find left most vertex.
            start = (1e100, 1)
            for edge in edges:
                start = min(start, min(edges[edge]))
            last = [(start[0][0] - 1, start[0][1]), start[0], 1]
            first_run = True
            loops1 = 0
            while last[1] != start[0] or first_run:
                first_run = False
                if loops1 > len_edges:
                    raise ValueError("Hull error")
                loops1 += 1
                next = get_closes_edge_by_angle(edges[last[1]], last)
                # draw_pointer(next[0]+next[1],"Green","line", comment=i, width= 1)
                # print_(next[0],"-",next[1])

                last = next
                poly += [list(last[0])]
            self.polygon += [poly]
            # Remove all edges that are intersects new poly (any vertex inside
            # new poly)
            poly_ = Polygon([poly])
            for p in edges.keys()[:]:
                if poly_.point_inside(list(p)):
                    del edges[p]
        self.draw(color="Green", width=1)