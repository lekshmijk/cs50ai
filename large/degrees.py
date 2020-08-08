import csv
import sys
import time

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass

start_time = time.time()
def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")
    print("--- %s seconds ---" % (time.time() - start_time))
    
    while True:
        source = person_id_for_name(input("Actor 1:"))
        if source is None:
            #sys.exit("Person not found.")
            print("Person not found! Please try again:")
            continue
        else:
            break

    while True:
        target = person_id_for_name(input("Actor 2:"))
        if target is None:
            #sys.exit("Person not found.")
            print("Person not found! Please try again:")
            continue
        else:
            break

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")
    print("--- %s seconds ---" % (time.time() - start_time))


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    #Initialize frontier:-
    frontier = QueueFrontier()       #for BFS
    start = Node(source, None, None) #state -> people, action -> movies
    frontier.add(start)              #frontier initially contains start state

    #Initialize explored set, which is initially empty:-
    explored_set = set()

    #Iterate using while loop until a solution is found:-
    while True:

        #If frontier is empty- no solution:-
        if frontier.empty():
            return None
            
        #If frontier not empty- remove node:-
        node = frontier.remove()

        #Expand node and add the neighbours to the frontier, if not already in frontier or explored set:-
        for action, state in neighbors_for_person(node.state):
            if not frontier.contains_state(state) and state not in explored_set: 
                child_node = Node(state,node,action)

                #If node is goal- found a solution:-
                if child_node.state == target:
                    connections = []
                    while child_node.parent is not None:
                        connections.append((child_node.action,child_node.state))
                        child_node = child_node.parent #keep track of parent node
                    connections.reverse()              #reverse to get the path taken to get to target
                    return connections
                else:
                    frontier.add(child_node)
                
        #add node to explored set:-
        explored_set.add(node.state)
        

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()


  
