import numpy as np
import time

# Convex hull function inspired by https://www.geeksforgeeks.org/convex-hull-using-jarvis-algorithm-or-wrapping/




def FindConvexHull(points_list):
    output = []
    n = len(points_list)

    # Initialize mostLeft to the x-coordinate of the first point
    mostLeft = points_list[0][0]
    mostLeftIndex = 0

    # Find the point with the lowest x-coordinate
    for i in range(1, len(points_list)):
        if points_list[i][0] < mostLeft:
            mostLeft = points_list[i][0]
            mostLeftIndex = i

    p = mostLeftIndex
    q = 0
    while True:
        output.append(points_list[p])
        q = (p + 1) % n

        for i in range(n):
            orientation = (points_list[i][1] - points_list[p][1]) * (points_list[q][0] - points_list[i][0]) - (points_list[q][1] - points_list[i][1]) * (points_list[i][0] - points_list[p][0])
            
            # Check for clockwise rotation
            if orientation < 0:
                q = i

            # Check for collinear points
            elif orientation == 0:
                # Calculate distance between p and q, and p and i
                dist_pq = ((points_list[q][0] - points_list[p][0]) ** 2 + (points_list[q][1] - points_list[p][1]) ** 2)
                dist_pi = ((points_list[i][0] - points_list[p][0]) ** 2 + (points_list[i][1] - points_list[p][1]) ** 2)
                
                # If the distance from p to i is greater than the distance from p to q, set q to i
                if dist_pi > dist_pq:
                    q = i

        p = q

        if p == mostLeftIndex:
            break
        

    return output

def distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def greedy_insertion(points_list):
    start = time.time()
    convex_hull = FindConvexHull(points_list)
    tour = convex_hull.copy()

    points_list = [tuple(point) for point in points_list]
    convex_hull = [tuple(point) for point in convex_hull]

    # Find points inside the convex hull
    inside_points = [p for p in points_list if p not in convex_hull]

    # Create a mapping between points and their indices
    point_to_index = {point: index for index, point in enumerate(points_list)}


    # Counter for number of iterations
    counter = 0

    def insert_point():
        nonlocal tour
        min_increase = np.Infinity
        min_index = None
        min_point = None

        for p in inside_points:
            for i in range(len(tour)):
                prev_point = tour[i]
                next_point = tour[(i + 1) % len(tour)]

                current_distance = distance(prev_point, next_point)
                new_distance = distance(prev_point, p) + distance(p, next_point)

                increase = new_distance - current_distance

                if increase < min_increase:
                    min_increase = increase
                    min_index = i
                    min_point = p

        if min_point is None:
            return False

        # Insert the point with the smallest increase in the tour
        tour.insert(min_index + 1, min_point)
        inside_points.remove(min_point)


        return True


    while insert_point():
        pass

    tour = [tuple(point) for point in tour]
    tour_indices = [point_to_index[point] for point in tour]
    index_0 = tour_indices.index(0)
    tour_indices = tour_indices[index_0:] + tour_indices[:index_0]

    print("TOUR CALCULATED")
    print(tour_indices)

    end = time.time()
    print("Greedy Insertion Algorithm took", (end-start), "seconds!")
    return tour, tour_indices

def solve(nodes):
    greedy_insertion(nodes)

def draw_graph(node_array, tour, length, endFlag, fig, ax):
    ax.clear()
    ax.grid()

    ax.scatter(*zip(*node_array), color='blue', zorder=2)
    path = tour + [tour[0]]
    line, = ax.plot(*zip(*path), color='red', zorder=1)

    for i, point in enumerate(node_array):
        ax.text(point[0] * (1 + 0.03), point[1] * (1 + 0.03), i)
        
    ax.set_title(str("Distance ≈ " + str(round(length, 2))))
    
    fig.canvas.draw_idle()

    





