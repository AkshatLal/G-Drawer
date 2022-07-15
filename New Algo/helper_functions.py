from math import atan2, pi
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from operations import ordered_bdy, get_bdy, get_trngls, get_directed
from shortcutresolver import get_shortcut
from cip import find_cip

plt.rcParams.update({'font.size': 12})
INT_MAX = 10000
v_to_face = {}
added = []
factor = 1.2


def vert4(g):
    matrix = nx.to_numpy_matrix(g)
    tries = get_trngls(matrix)
    digraph = get_directed(matrix)
    bdy_nodes, bdy_edges = get_bdy(tries, digraph)
    bdy_ordered = ordered_bdy(bdy_nodes, bdy_edges)
    shortcuts = get_shortcut(matrix, bdy_nodes, bdy_edges)
    cips = find_cip(bdy_ordered, shortcuts)
    return cips
    pass


def merger(g, merge_to, merge_from):
    sm_list = []
    while len(merge_from) > 0:
        ff = merge_from[0]
        merge_from.remove(ff)
        em1 = [ff]
        while True:
            initial_size = len(em1)
            for i in em1:
                for j in merge_from:
                    if g.has_edge(i, j):
                        em1.append(j)
                        merge_from.remove(j)
            if initial_size == len(em1):
                break
        sm_list.append(em1)
    # print("My list", sm_list)
    for i in merge_to:
        for j in sm_list:
            count = 0
            for k in merge_to[i]:
                for m in j:
                    if g.has_edge(k, m):
                        count += 1
            if count == 2:
                for k in j:
                    merge_to[i].append(k)


def draw_graph(g):
    plt.axis('off')
    # origin_pos = nx.planar_layout(g)
    # for nodeId in origin_pos:
    #     g.add_node(nodeId, pos=(origin_pos[nodeId][0], origin_pos[nodeId][1]))
    origin_pos = nx.get_node_attributes(g, 'pos')
    nx.draw(g, origin_pos, with_labels=True)
    # plt.show()


def common_edge(a, b):
    """Returns true if a and b have a common edge"""
    count = 0
    for i in a:
        for j in b:
            if i == j:
                count = count + 1
    return count > 1


def common_vertex(a, b):
    """Returns true if a and b have a common vertex"""
    count = 0
    for i in a:
        for j in b:
            if i == j:
                count = count + 1
    return count > 0


def outer_edges(g):
    out_face = get_outer_face(g)
    # print("Outer Face: ", out_face)
    outer_edge_list = set()
    for i in g.edges():
        cnt = 0
        for j in out_face:
            if j in i:
                cnt += 1
        if cnt == 2:
            outer_edge_list.add(i)
    # print("Outer edge list: ", outer_edge_list)
    return list(outer_edge_list)


def get_outer_face(g):
    vertices = list(g.nodes())
    origin_pos = nx.get_node_attributes(g, 'pos')
    x1 = 0
    y1 = 0
    y2 = 0
    x2 = 0
    node1 = -1
    node2 = -1
    ff = -1
    for i in vertices:
        if y2 < origin_pos[i][1]:
            y1 = y2 = origin_pos[i][1]
            x2 = origin_pos[i][0]
            x1 = x2 - 1
            ff = node2 = i
    flag = False
    A = (x1, y1)
    B = (x2, y2)
    cycle = [ff]
    while not flag:
        min_diff = 2 * pi
        next_ver = -1
        for i in vertices:
            if i == node1 or i == node2 or not g.has_edge(i, node2):
                continue
            C = origin_pos[i]
            Ax = A[0] - B[0]
            Ay = A[1] - B[1]
            Cx, Cy = C[0] - B[0], C[1] - B[1]
            a = atan2(Ay, Ax)
            c = atan2(Cy, Cx)
            if a < 0:
                a += pi * 2
            if c < 0:
                c += pi * 2
            angle = (pi * 2 + c - a) if a > c else (c - a)
            if ((2 * pi - angle) - angle) < min_diff:
                min_diff = (2 * pi - angle) - angle
                next_ver = i
        node1 = node2
        node2 = next_ver
        A = origin_pos[node1]
        B = origin_pos[node2]
        cycle.append(next_ver)
        if next_ver == ff:
            break
    cycle.pop()
    # print(cycle)
    return cycle


def outer_faces_edge_mapping(my_graph, face_list):
    # print("my list", face_list)
    out_face = get_outer_face(my_graph)
    outer_face_edge_map = {}

    out_face.append(out_face[0])
    for i in face_list:
        for j in range(len(out_face) - 1):
            if out_face[j] in i and out_face[j + 1] in i:
                outer_face_edge_map[tuple(i)] = [out_face[j], out_face[j + 1]]
    return outer_face_edge_map


def outer_faces(my_graph, face_list):
    outer_face = []
    out_face = get_outer_face(my_graph)
    out_face.append(out_face[0])
    # print("out_face:", out_face)
    for i in face_list:
        for j in range(len(out_face) - 1):
            if out_face[j] in i and out_face[j + 1] in i:
                outer_face.append(i)
    # print("outer faces FFF:", outer_face)
    return list(outer_face)


def sign(x1, y1, x2, y2, x3, y3):
    return (x1 - x3) * (y2 - y3) - (x2 - x3) * (y1 - y3)


def point_in_triangle(x1, y1, x2, y2, x3, y3, x, y):
    d1 = sign(x, y, x1, y1, x2, y2)
    d2 = sign(x, y, x2, y2, x3, y3)
    d3 = sign(x, y, x3, y3, x1, y1)
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not (has_neg and has_pos)


def get_face_list(g, origin_pos):
    ver = list(g.nodes())
    # print(ver)
    face_list = []
    out_face = get_outer_face(g)
    out_face.sort()
    for i in range(0, len(ver) - 2):
        for j in range(i + 1, len(ver) - 1):
            for k in range(j + 1, len(ver)):
                if g.has_edge(ver[i], ver[j]) and g.has_edge(ver[j], ver[k]) and g.has_edge(ver[k], ver[i]):
                    face = [ver[i], ver[j], ver[k]]
                    face.sort()
                    if face != out_face:
                        face_list.append(face)
    all_triangles = face_list
    for i in all_triangles:
        i.sort()

    all_triangles = np.unique(all_triangles, axis=0)
    triangular_faces = []

    for face in all_triangles:
        flag = False
        for NodeID in origin_pos:
            if NodeID == face[0] or NodeID == face[1] or NodeID == face[2]:
                continue

            if (point_in_triangle(origin_pos[face[0]][0], origin_pos[face[0]][1], origin_pos[face[1]][0],
                                  origin_pos[face[1]
                                  ][1], origin_pos[face[2]][0],
                                  origin_pos[face[2]][1], origin_pos[NodeID][0], origin_pos[NodeID][1])):
                flag = True
                break
        if not flag:
            triangular_faces.append(face.tolist())
    return triangular_faces


def add_corner(g):
    origin_pos = nx.get_node_attributes(g, 'pos')
    outer_face = get_outer_face(g)
    node_count = g.number_of_nodes()
    # print("Outer face of dual:", outer_face)

    # And modifications begin...
    # First, remove the outer 2 edges

    g.remove_edge(outer_face[0], outer_face[1])
    x = (origin_pos[outer_face[0]][0] + origin_pos[outer_face[1]][0]) / 2
    y = (origin_pos[outer_face[0]][1] + origin_pos[outer_face[1]][1]) / 2
    g.add_node(node_count, pos=(x, y))
    added.append(node_count)
    g.add_edge(outer_face[0], node_count)
    g.add_edge(outer_face[1], node_count)

    node_count += 1
    g.remove_edge(outer_face[1], outer_face[2])
    x = (origin_pos[outer_face[1]][0] + origin_pos[outer_face[2]][0]) / 2
    y = (origin_pos[outer_face[1]][1] + origin_pos[outer_face[2]][1]) / 2
    g.add_node(node_count, pos=(x, y))
    added.append(node_count)
    g.add_edge(outer_face[1], node_count)
    g.add_edge(outer_face[2], node_count)

    if len(outer_face) > 4:
        node_count += 1
        g.remove_edge(outer_face[2], outer_face[3])
        x = (origin_pos[outer_face[2]][0] + origin_pos[outer_face[3]][0]) / 2
        y = (origin_pos[outer_face[2]][1] + origin_pos[outer_face[3]][1]) / 2
        g.add_node(node_count, pos=(x, y))
        added.append(node_count)
        g.add_edge(outer_face[2], node_count)
        g.add_edge(outer_face[3], node_count)

        node_count += 1
        g.remove_edge(outer_face[3], outer_face[4])
        x = (origin_pos[outer_face[3]][0] + origin_pos[outer_face[4]][0]) / 2
        y = (origin_pos[outer_face[3]][1] + origin_pos[outer_face[4]][1]) / 2
        g.add_node(node_count, pos=(x, y))
        added.append(node_count)
        g.add_edge(outer_face[3], node_count)
        g.add_edge(outer_face[4], node_count)
    elif len(outer_face) == 4:
        node_count += 1
        g.remove_edge(outer_face[2], outer_face[3])
        x = (origin_pos[outer_face[2]][0] + origin_pos[outer_face[3]][0]) / 2
        y = (origin_pos[outer_face[2]][1] + origin_pos[outer_face[3]][1]) / 2
        g.add_node(node_count, pos=(x, y))
        added.append(node_count)
        g.add_edge(outer_face[2], node_count)
        g.add_edge(outer_face[3], node_count)

        node_count += 1
        g.remove_edge(outer_face[3], outer_face[0])
        x = (origin_pos[outer_face[3]][0] + origin_pos[outer_face[0]][0]) / 2
        y = (origin_pos[outer_face[3]][1] + origin_pos[outer_face[0]][1]) / 2
        g.add_node(node_count, pos=(x, y))
        added.append(node_count)
        g.add_edge(outer_face[3], node_count)
        g.add_edge(outer_face[0], node_count)
        pass
    else:
        node_count += 1
        g.remove_edge(outer_face[2], outer_face[0])
        x1 = (origin_pos[outer_face[2]][0] * 2 +
              origin_pos[outer_face[0]][0]) / 3
        y1 = (origin_pos[outer_face[2]][1] * 2 +
              origin_pos[outer_face[0]][1]) / 3
        x2 = (origin_pos[outer_face[2]][0] +
              origin_pos[outer_face[0]][0] * 2) / 3
        y2 = (origin_pos[outer_face[2]][1] +
              origin_pos[outer_face[0]][1] * 2) / 3
        g.add_node(node_count, pos=(x1, y1))
        added.append(node_count)
        g.add_node(node_count + 1, pos=(x2, y2))
        added.append(node_count + 1)
        g.add_edge(outer_face[0], node_count + 1)
        g.add_edge(outer_face[2], node_count)
        g.add_edge(node_count, node_count + 1)
    return g


# In the get dual code, fix when dual has more than 26 nodes (Code breaks otherwise)
def get_dual(g):
    initial_v_count = g.number_of_nodes()
    global v_to_face
    origin_pos = nx.get_node_attributes(g, 'pos')
    # print("origin pos:", origin_pos)
    # Gives me the list of all faces, i.e. triangles
    my_set = get_face_list(g, origin_pos)
    outer_faces_final = outer_faces(g, my_set)
    outer_face = get_outer_face(g)
    my_list = list(my_set)
    vertex_to_face_map = {}
    pos0 = []
    geo_dual = nx.Graph()
    for i in my_set:
        pos_x = tuple(
            map(sum, zip(origin_pos[i[0]], origin_pos[i[1]], origin_pos[i[2]])))
        pos_x = tuple(pos_xe / 3 for pos_xe in pos_x)
        if i in outer_faces_final:
            pos0.append(pos_x)  # centroids of triangles having an outer edge
        vertex_to_face_map[my_list.index(i)] = i
        geo_dual.add_node(my_list.index(i), pos=pos_x)
    for i in my_list:
        for j in my_list:
            if i < j:
                if common_edge(i, j):
                    # geo_dual graph edges of inner centroids
                    geo_dual.add_edge(my_list.index(i), my_list.index(j))
    # draw_graph(geo_dual)

    cnt = 1
    number_of_nodes = geo_dual.number_of_nodes()
    vertex_to_side = {}
    out_face_side = []
    for i in range(len(outer_face)):
        out_face_side.append(
            [outer_face[i], outer_face[(i + 1) % len(outer_face)]])
    dual_coord = nx.get_node_attributes(geo_dual, 'pos')
    glob_X = 0
    glob_Y = 0
    pripyat = {}
    for i in vertex_to_face_map:
        p = int(i)
        p1 = vertex_to_face_map[i][0]
        p2 = vertex_to_face_map[i][1]
        p3 = vertex_to_face_map[i][2]
        tri = [p1, p2, p3]
        for k in range(3):
            p1 = tri[k]
            p2 = tri[(k + 1) % 3]
            if [p1, p2] in out_face_side or [p2, p1] in out_face_side:
                x1 = origin_pos[p1][0]
                x2 = origin_pos[p2][0]
                y1 = origin_pos[p1][1]
                y2 = origin_pos[p2][1]
                x3 = dual_coord[p][0]
                y3 = dual_coord[p][1]
                x4 = ((x1 + x2) - 0.2 * x3)
                x4 += (x4 - x3)
                y4 = ((y1 + y2) - 0.2 * y3)
                y4 += (y4 - y3)
                glob_X += x4
                glob_Y += y4
                geo_dual.add_node(number_of_nodes + cnt, pos=(x4, y4))
                pripyat[number_of_nodes + cnt] = [p1, p2]
                vertex_to_side[number_of_nodes + cnt] = (p1, p2)
                geo_dual.add_edge(number_of_nodes + cnt, p)
                cnt += 1
    for i in pripyat:
        vertex_to_face_map[i] = pripyat[i]
    glob_X /= (cnt - 1)
    glob_Y /= (cnt - 1)
    in_X = 0
    in_Y = 0
    dual_coord = nx.get_node_attributes(geo_dual, 'pos')
    for i in geo_dual.nodes:
        if i < number_of_nodes:
            in_X += dual_coord[i][0]
            in_Y += dual_coord[i][1]
    in_X /= number_of_nodes
    in_Y /= number_of_nodes
    for i in geo_dual.nodes:
        if i < number_of_nodes:
            geo_dual.add_node(
                i, pos=(dual_coord[i][0] + (glob_X - in_X), dual_coord[i][1] + (glob_Y - in_Y)))
        else:
            geo_dual.add_node(i, pos=(
                factor * dual_coord[i][0] - (factor - 1) * glob_X, factor * dual_coord[i][1] - (factor - 1) * glob_Y))
    print("final maps", vertex_to_side)
    for i in vertex_to_side:
        for j in vertex_to_side:
            if i != j and ((vertex_to_side[i][0] == vertex_to_side[j][0]) or (
                    vertex_to_side[i][0] == vertex_to_side[j][1]) or (vertex_to_side[i][1] == vertex_to_side[j][0]) or (
                                   vertex_to_side[i][1] == vertex_to_side[j][1])):
                geo_dual.add_edge(i, j)
    # num = 0
    # x_center = 0
    # y_center = 0
    # for i in pos:
    #     num = num + 1
    #     x_center += pos[i][0]
    #     y_center += pos[i][1]
    #
    # # print("Size:", np.size(pos0) / 2)
    # print("The number of nodes added", np.size(pos0))
    # for i in range(0, int(np.size(pos0) / 2)):
    #     geo_dual.add_node(number_of_nodes + i)  # we add the external nodes
    # for i in range(0, int(np.size(pos0) / 2)):
    #     vertex_to_face_map[number_of_nodes + i] = list(face_edge_outer[tuple(outer_faces_final[i])])
    # print("My map", vertex_to_face_map)
    #
    # for i in vertex_to_face_map:
    #     if i >= number_of_nodes:
    #         for j in outer_faces_final:
    #             flag = 0
    #             if all(x in j for x in vertex_to_face_map[i]):
    #                 flag = 1
    #             if flag:
    #                 pos_x = tuple(map(sum, zip(origin_pos[j[0]], origin_pos[j[1]], origin_pos[j[2]])))
    #                 pos_x = tuple(pos_xe / 3 for pos_xe in pos_x)
    #                 coord1 = origin_pos[vertex_to_face_map[i][0]]
    #                 coord2 = origin_pos[vertex_to_face_map[i][1]]
    #                 x1 = coord1[0]
    #                 y1 = coord1[1]
    #                 x2 = coord2[0]
    #                 y2 = coord2[1]
    #                 k = (y2 - y1) / (x2 - x1)
    #                 a = pos_x[0]
    #                 b = pos_x[1]
    #                 xf = (x1 * k * k + a + k * (b - y1)) / (1 + k * k)
    #                 yf = (b * k * k + y1 + k * (a - x1)) / (1 + k * k)
    #                 push = 2  # Here, varying the value of push, we can vary the
    #                 # position of the outer cycle vertices and prevent edges from coinciding
    #                 tup = (xf * push, yf * push)
    #                 geo_dual.add_node(i, pos=tup)
    #                 pos[i] = tup
    #
    # for i in vertex_to_face_map:
    #     for j in vertex_to_face_map:
    #         if i < j:
    #             if i >= number_of_nodes and j >= number_of_nodes and common_vertex(vertex_to_face_map[i],
    #                                                                                vertex_to_face_map[j]):
    #                 geo_dual.add_edge(i, j)
    #             if common_edge(vertex_to_face_map[i], vertex_to_face_map[j]):
    #                 geo_dual.add_edge(i, j)  # geo_dual graph edges of inner centroids
    for i in range(1, initial_v_count + 1):
        v_to_face[i] = []
    for i in vertex_to_face_map:
        for j in vertex_to_face_map[i]:
            v_to_face[int(j)].append(int(i))
    print("vertex to face map: ", vertex_to_face_map)
    merger(geo_dual, v_to_face, added)
    print("map: ", v_to_face)
    return geo_dual


def debug(g):
    # print("v_to_face:", v_to_face)
    # print("added", added)
    pass
# 5
# 1:2,4,5
# 2:1,3,4,5
# 3:2,4,5
# 4:1,2,3,5
# 5:1,2,3,4
