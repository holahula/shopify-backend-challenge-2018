import requests 
import numpy as np
import json
import math 

def search(graph, start, visited):
    x = graph[start]["id"] 
    children = set()
    visited.append(x)
    children = graph[start]["child_ids"]

    for y in children:
        if y in visited:
            return 0
        else: 
            if len(graph[y-1]["child_ids"]) != 0:
                lol = search(graph, y-1, visited)
                if lol == 0: 
                    return 0
    return 1

def main(): 
    parent = list()
    visited = list()
    new = list()
    children = list()

    menu = {}
    menu["invalid_menus"] = []
    menu["valid_menus"] = []

    values = {}

    payload = {'id': 2, 'page': 1}
    r = requests.get('https://backend-challenge-summer-2018.herokuapp.com/challenges.json', params=payload)   
    r.json()
    data = json.loads(r.text)
    new += (data["menus"])

    total = data["pagination"]["total"]
    page = data["pagination"]["per_page"]
    
    up = int(math.ceil(float(total) / page))

    for x in range (2, up+1):
        payload = {'id': 2, 'page': x}
        r = requests.get('https://backend-challenge-summer-2018.herokuapp.com/challenges.json', params=payload)   
        r.json()

        data = json.loads(r.text)

        new += (data["menus"])

    for x in new:
        if "parent_id" not in x.keys():
            parent.append(x["id"]-1)

    #print 'parent', parent
    #for x in new:
        #print x["id"], x["child_ids"]

    #print new
    #print 'test', new[19]["child_ids"]
    for x in range(len(parent)): 
        switch = 0
        orderA = 0
        orderB = 0

        val = search(new, parent[x], visited)

        if val == 1: 
            switch = 1 #circular
        else: 
            switch = 0 #not circular
        for y in visited: 
            children += new[y-1]["child_ids"]
        
        children.sort()

        values["root_id"] = parent[x] + 1
        values["children"] = children

        if switch == 0:
            menu["invalid_menus"].append(values)
        else: 
            menu["valid_menus"].append(values)

        values = {}
        children = []
        visited = []

    menuJSON = json.dumps(menu, ensure_ascii=False)

    print menuJSON

if __name__ == "__main__":
    main()



