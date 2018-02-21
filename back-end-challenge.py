'''
ASSUMPTIONS MADE DURING CHALLENGE: 

- All nodes without parent_ids are roots 
- A maximum depth of 4 refers to a total of 5 layers, creating 4 layers of depth  

COMMENTS: 
- The extra challenge is also solvable using this program, simply change the value of the int CHALLENGE from 1 -> 2

'''

import requests 
import numpy as np
import json
import math 

def search(graph, start, visited): #dfs function 
    x = graph[start]["id"]  # sets starting node 
    children = set()
    visited.append(x) #adds node to list of visited nodes 
    children = graph[start]["child_ids"] #creates a set of all children nodes of current node 

    for y in children: 
        if y in visited: #checks that current node has not been visited 
            return 0
        else: 
            if len(graph[y-1]["child_ids"]) != 0: #if there is a child node, then visit 
                lol = search(graph, y-1, visited) # if child node has been visited, it is a circular menu thus will return 0
                if lol == 0: 
                    return 0
    return 1

def main(): 
    parent = list()
    visited = list()
    new = list()
    children = list()

    challenge = 1 # to view answer to extra challenge, change value from 1 to 2
    menu = {}
    menu["invalid_menus"] = []
    menu["valid_menus"] = []

    values = {}

    payload = {'id': challenge, 'page': 1} # http requests 
    r = requests.get('https://backend-challenge-summer-2018.herokuapp.com/challenges.json', params=payload)   
    r.json()
    data = json.loads(r.text)
    new += (data["menus"])

    total = data["pagination"]["total"]
    page = data["pagination"]["per_page"]
    
    up = int(math.ceil(float(total) / page)) # math so that the least amount of requests needed are sent, reducing run time 

    for x in range (2, up+1):
        payload = {'id': challenge, 'page': x}
        r = requests.get('https://backend-challenge-summer-2018.herokuapp.com/challenges.json', params=payload)   
        r.json()

        data = json.loads(r.text)

        new += (data["menus"])

    for x in new: # saves all starting nodes 
        if "parent_id" not in x.keys():
            parent.append(x["id"]-1)

    for x in range(len(parent)): 
        switch = 0

        val = search(new, parent[x], visited)

        if val == 1: 
            switch = 1 #not circular
        else: 
            switch = 0 # circular

        for y in visited: 
            children += new[y-1]["child_ids"] # creates list of all children nodes of parent node 
        
        children.sort()

        values["root_id"] = parent[x] + 1
        values["children"] = children

        if switch == 0:
            menu["invalid_menus"].append(values) # appends the parent node and all its children nodes to either valid / invalid menus 
        else: 
            menu["valid_menus"].append(values)

        values = {} # reset all values 
        children = []
        visited = []

    menuJSON = json.dumps(menu, ensure_ascii=False) # dictionary -> JSON 

    print menuJSON # prints as a JSON 

if __name__ == "__main__":
    main()



