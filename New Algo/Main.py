import networkx as nx
from checker import check_planarity
from tsmpy import TSM
import matplotlib.pyplot as plt
from helper_functions import get_dual, debug, draw_graph, vert4
from triangularity import get_nontriangular_face

global cip_check


def Call_Main(g):
    # draw_graph(g)
    new_g = nx.Graph()
    number_of_nodes = g.number_of_nodes()
    min_deg = 1000
    for i in range(number_of_nodes):
        min_deg = min(min_deg, g.degree[i + 1])
    p1 = check_planarity(g)
    print("Value: ", p1)
    if not p1:
        print("Planar")
        error_msg = "Error : Graph is not Planar"
        return error_msg
    origin_pos = nx.planar_layout(g)

    deg2_cnt = 0
    min_deg = 3
    error_msg = None
    for i in g.nodes():
        min_deg = min(min_deg, g.degree[i])
        if g.degree[i] == 2:
            deg2_cnt += 1
    if deg2_cnt > 4:
        # messagebox.showwarning(
        #     "Warning", "More than 4 vertices of degree 2. Floor Plan may not be Planar")
        print("Display CIP")
        msg = vert4(g)
        print("yeah", msg)
        res = ""
        for i in msg:
            var = [x + 1 for x in i]
            i = var
            res += str(i)
        global cip_check
        cip_check = 1
        error_msg = res
    if min_deg <= 1:
        print("Not Bi-Connected")
        error_msg = "Error : Graph is not Bi-Connected"
        return error_msg
    p1 = check_planarity(g)
    print("Value: ", p1)
    p2 = get_nontriangular_face(nx.get_node_attributes(g, 'pos'), g)
    if len(p2) > 0:
        p2 = False
    else:
        p2 = True
    p3 = nx.is_biconnected(g)
    if not (p1 and p2 and p3):
        print("Graph is not:")
        if not p1:
            print("Planar")
            error_msg = "Error : Graph is not Planar"
            # messagebox.showerror("Error", "Graph is not Planar")
        if not p2:
            print("Triangular")
            error_msg = "Error : Graph is not Triangular"
            # messagebox.showerror("Error", "Graph is not Triangular")
        if not p3:
            print("Bi Connected")
            error_msg = "Error : Graph is not Bi-Connected"
            # messagebox.showerror("Error", "Graph is not Bi-Connected")
        print("Dual cannot be created.")
        return error_msg
    # if min_deg < 3:
    #     print("Degree of all vertices not more than 2. Exiting program.")
    #     return

    for nodeId in origin_pos:
        new_g.add_node(nodeId, pos=(
            origin_pos[nodeId][0], origin_pos[nodeId][1]))
    for i in g.edges():
        new_g.add_edge(i[0], i[1])
    # g = new_g
    # took half a day to comment out the upper line and find out the mistake
    # At this point, we have taken the input, performed necessary checks and drawn the input graph.
    # draw_graph(g)
    # plt.show()
    # plt.savefig("FloorPlans/floor_plan1.jpg")
    # plt.show()

    # Now to generate dual.

    # new_dual(g)
    geo_dual = get_dual(g)
    debug(g)
    draw_graph(geo_dual)
    # plt.show()
    plt.savefig("FloorPlans/floor_plan2.jpg")
    plt.show()
    pos = nx.get_node_attributes(geo_dual, 'pos')
    tsm = TSM(geo_dual, pos)
    tsm.display()
    plt.savefig("FloorPlans/floor_plan4.jpg")
    plt.show()
    debug(g)
    # plt.savefig("FloorPlans/floor_plan.jpg")
    plt.close()
    return error_msg
# Call_Main()
