# Name: Adeline Chin
# CSE 160
# Homework 5

import utils  # noqa: F401, do not remove if using a Mac
import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter


###
#  Problem 1a
###

def get_practice_graph():
    """Builds and returns the practice graph
    """
    practice_graph = nx.Graph()

    practice_graph.add_node("A")
    practice_graph.add_node("B")
    practice_graph.add_node("C")
    practice_graph.add_node("D")
    practice_graph.add_node("E")
    practice_graph.add_node("F")

    practice_graph.add_edge("A", "B")
    practice_graph.add_edge("A", "C")
    practice_graph.add_edge("B", "C")
    practice_graph.add_edge("B", "D")
    practice_graph.add_edge("C", "F")
    practice_graph.add_edge("C", "D")
    practice_graph.add_edge("D", "F")
    practice_graph.add_edge("D", "E")

    return practice_graph


def draw_practice_graph(graph):
    """Draw practice_graph to the screen.
    """
    nx.draw_networkx(graph)
    plt.show()


###
#  Problem 1b
###

def get_romeo_and_juliet_graph():
    """Builds and returns the romeo and juliet graph
    """
    rj = nx.Graph()

    rj.add_node("Juliet")
    rj.add_node("Nurse")
    rj.add_node("Tybalt")
    rj.add_node("Capulet")
    rj.add_node("Friar Laurence")
    rj.add_node("Romeo")
    rj.add_node("Benvolio")
    rj.add_node("Montague")
    rj.add_node("Escalus")
    rj.add_node("Mercutio")
    rj.add_node("Paris")

    rj.add_edge("Juliet", "Nurse")
    rj.add_edge("Juliet", "Tybalt")
    rj.add_edge("Juliet", "Capulet")
    rj.add_edge("Juliet", "Friar Laurence")
    rj.add_edge("Juliet", "Romeo")
    rj.add_edge("Tybalt", "Capulet")
    rj.add_edge("Capulet", "Paris")
    rj.add_edge("Capulet", "Escalus")
    rj.add_edge("Friar Laurence", "Romeo")
    rj.add_edge("Romeo", "Benvolio")
    rj.add_edge("Romeo", "Montague")
    rj.add_edge("Romeo", "Mercutio")
    rj.add_edge("Benvolio", "Montague")
    rj.add_edge("Montague", "Escalus")
    rj.add_edge("Mercutio", "Escalus")
    rj.add_edge("Mercutio", "Paris")
    rj.add_edge("Paris", "Escalus")
    return rj


def draw_rj(graph):
    """Draw the rj graph to the screen and to a file.
    """
    nx.draw_networkx(graph)
    plt.savefig("romeo-and-juliet.pdf")
    plt.show()


###
#  Problem 2
###

def friends(graph, user):
    """Returns a set of the friends of the given user, in the given graph.
    """
    # This function has already been implemented for you.
    # You do not need to add any more code to this (short!) function.
    return set(graph.neighbors(user))


def friends_of_friends(graph, user):
    """Find and return the friends of friends of the given user.

    Arguments:
        graph: the graph object that contains the user and others
        user: a string

    Returns: a set containing the names of all of the friends of
    friends of the user. The set should not contain the user itself
    or their immediate friends.
    """
    friends_list = friends(graph, user)
    recommended = set()
    for friend in friends_list:
        friends_friends = friends(graph, friend)
        for f in friends_friends:
            recommended.add(f)
    for friend in friends_list:
        recommended.discard(friend)
    recommended.discard(user)
    return recommended


def common_friends(graph, user1, user2):
    """Finds and returns the set of friends that user1 and user2 have in common.

    Arguments:
        graph:  the graph object that contains the users
        user1: a string representing one user
        user2: a string representing another user

    Returns: a set containing the friends user1 and user2 have in common
    """
    set = friends(graph, user1).intersection(friends(graph, user2))
    return set


def num_common_friends_map(graph, user):
    """Returns a map (a dictionary), mapping a person to the number of friends
    that person has in common with the given user. The map keys are the
    people who have at least one friend in common with the given user,
    and are neither the given user nor one of the given user's friends.
    Example: a graph called my_graph and user "X"
    Here is what is relevant about my_graph:
        - "X" and "Y" have two friends in common
        - "X" and "Z" have one friend in common
        - "X" and "W" have one friend in common
        - "X" and "V" have no friends in common
        - "X" is friends with "W" (but not with "Y" or "Z")
    Here is what should be returned:
      num_common_friends_map(my_graph, "X")  =>   { 'Y':2, 'Z':1 }

    Arguments:
        graph: the graph object that contains the user and others
        user: a string

    Returns: a dictionary mapping each person to the number of (non-zero)
    friends they have in common with the user
    """
    common_friends_map = dict()
    for person in friends_of_friends(graph, user):
        num_common_friends = len(common_friends(graph, user, person))
        if num_common_friends > 0:
            common_friends_map[person] = num_common_friends
    return common_friends_map


def num_map_to_sorted_list(map_with_number_vals):
    """Given a dictionary, return a list of the keys in the dictionary.
    The keys are sorted by the number value they map to, from greatest
    number down to smallest number.
    When two keys map to the same number value, the keys are sorted by their
    natural sort order for whatever type the key is, from least to greatest.

    Arguments:
        map_with_number_vals: a dictionary whose values are numbers

    Returns: a list of keys, sorted by the values in map_with_number_vals
    """
    items = list(map_with_number_vals.items())
    sort_by_key = sorted(items, key=itemgetter(0))
    sort_by_value = sorted(sort_by_key, key=itemgetter(1), reverse=True)
    sorted_items = []
    for pair in sort_by_value:
        sorted_items.append(pair[0])
    return sorted_items


def recommend_by_num_common_friends(graph, user):
    """
    Returns a list of friend recommendations for the user, sorted
    by number of friends in common.

    Arguments:
        graph: the graph object that contains the user and others
        user: a string

    Returns: A list of friend recommendations for the given user.
    The friend recommendation list consists of names/IDs of people in
    the graph who are not yet a friend of the given user.  The order
    of the list is determined by the number of common friends (people
    with the most common friends are listed first).  In the
    case of a tie in number of common friends, the names/IDs are
    sorted by their natural sort order, from least to greatest.
    """
    common_friends = num_common_friends_map(graph, user)
    sorted_list = num_map_to_sorted_list(common_friends)
    return sorted_list


###
#  Problem 3
###

def influence_map(graph, user):
    """Returns a map (a dictionary) mapping from each person to their
    influence score, with respect to the given user. The map only
    contains people who have at least one friend in common with the given
    user and are neither the user nor one of the users's friends.
    See the assignment writeup for the definition of influence scores.
    """
    common_friends_map = num_common_friends_map(graph, user)
    recommended_people = list(common_friends_map.keys())
    influence_map = dict()
    for person in recommended_people:
        person_score = 0
        com_friends = common_friends(graph, user, person)
        for friend in com_friends:
            num_friends = len(friends(graph, friend))
            score = 1 / num_friends
            person_score += score
        influence_map[person] = person_score
    return influence_map


def recommend_by_influence(graph, user):
    """Return a list of friend recommendations for the given user.
    The friend recommendation list consists of names/IDs of people in
    the graph who are not yet a friend of the given user.  The order
    of the list is determined by the influence score (people
    with the biggest influence score are listed first).  In the
    case of a tie in influence score, the names/IDs are sorted
    by their natural sort order, from least to greatest.
    """
    return num_map_to_sorted_list(influence_map(graph, user))


###
#  Problem 5
###

def get_facebook_graph():
    """Builds and returns the facebook graph
    """
    facebook = nx.Graph()
    fb = open("facebook-links-small.txt", "r")
    for line in fb:
        edge = line.split()
        facebook.add_node(int(edge[0]))
        facebook.add_node(int(edge[1]))
        facebook.add_edge(int(edge[0]), int(edge[1]))
    fb.close()
    return facebook


def main():
    # practice_graph = get_practice_graph()
    # Comment out this line after you have visually verified your practice
    # graph.
    # Otherwise, the picture will pop up every time that you run your program.
    # draw_practice_graph(practice_graph)

    rj = get_romeo_and_juliet_graph()
    # Comment out this line after you have visually verified your rj graph and
    # created your PDF file.
    # Otherwise, the picture will pop up every time that you run your program.
    # draw_rj(rj)

    ###
    #  Problem 4
    ###

    print("Problem 4:")
    print()

    nodes = list(rj.nodes)
    same = []
    different = []
    for node in nodes:
        if recommend_by_influence(rj, node) == \
                recommend_by_num_common_friends(rj, node):
            same.append(node)
        else:
            different.append(node)
    print("Unchanged Recommendations: ", same)
    print("Changed Recommendations: ", different)

    ###
    #  Problem 5
    ###

    facebook = get_facebook_graph()

    assert len(facebook.nodes()) == 63731
    assert len(facebook.edges()) == 817090

    ###
    #  Problem 6
    ###
    print()
    print("Problem 6:")
    print()

    nodes = list(facebook.nodes)
    nodes_list = []
    for node in nodes:
        if node % 1000 == 0:
            nodes_list.append(node)
    nodes_list.sort()
    for id in nodes_list:
        num_recommended = recommend_by_num_common_friends(facebook, id)
        if len(num_recommended) >= 10:
            num_recommended = num_recommended[0:10]
        print(id, " (by num_common_friends): ", num_recommended)

    ###
    #  Problem 7
    ###
    print()
    print("Problem 7:")
    print()

    for id in nodes_list:
        influence_recommended = recommend_by_influence(facebook, id)
        if len(influence_recommended) >= 10:
            influence_recommended = influence_recommended[0:10]
        print(id, " (by influence): ", influence_recommended)

    ###
    #  Problem 8
    ###
    print()
    print("Problem 8:")
    print()

    same = 0
    different = 0
    for id in nodes_list:
        num_recommended = recommend_by_num_common_friends(facebook, id)
        influence_recommended = recommend_by_influence(facebook, id)
        if num_recommended == influence_recommended:
            same += 1
        else:
            different += 1
    print("Same: ", same)
    print("Different: ", different)


if __name__ == "__main__":
    main()


###
#  Collaboration
###

# This homework was finished independently and with help from Ed posts.
