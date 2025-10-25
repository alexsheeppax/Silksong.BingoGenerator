import os, json, random

#file paths and names
ASSETS_PATH = "assets"
COMPUTED_SUBDIR = "generated"
GOALS_FILENAME = "silksong-v6.json"
CAT_FILENAME = "categorized_v3.json"

#Lockout.live formatting
BOARD_TYPES = [
    'cloak', 'walljump', 'act2', 'dash', 'early', 'clawline', 
    'feydown', 'craft', 'hardsave', 'melody', 'flea', "key", 'tool', ]
    
LL_LIMITS = {
            "board" : {
                "early" : 20,
                "dash"  : 20,
                "cloak" : 30,
                "walljump" : 25,
                "act2" : 30,
                "clawline" : 40,
                "feydown" : 50,
                "hardsave" : 20,
                "craft" : 40,
                "flea" : 15,
                "key" : 20,
                "tool" : 30,
                "melody" : 20
            },
            "line" : {
                "quest" : 60,
                "locket" : 60,
                "upgrade" : 80,
                "fight" : 60,
                "npc" : 40,
                "location" : 60,
                "collection" : 60,
                "relic" : 60
            }
        }

def getAllGoals(noTags=[]):
    """
    Loads the file given in variables at the top of the script and returns the parts.
    Returns list of Goal dictionaries and list of Exclusive lists.
    """
    with open(os.path.join(ASSETS_PATH, CAT_FILENAME)) as f:
        catList = json.load(f)
    #can't modify list during iteration so keep track of removables here
    remGoals = []
    for g in catList["goals"]: #add weight=1 to all non-weighted goals for later
        if "weight" not in g.keys():
            g["weight"] = 1
        #check if we should exclude the goal based on options passed
        goalTags = g["types"] + g["progression"]
        for tag in goalTags:
            if tag in noTags:
                remGoals.append(g)
                break
    for g in remGoals:
        if g in catList["goals"]: #in case goal got added to remList twice; don't want to error out due to typo or w/e
            catList["goals"].remove(g)
    return catList["goals"], [u["unique"] for u in catList["exclusions"]]

def findExclusions(goalName, exclusionList):
    """
    Given a goal name and the main exclusion list, returns the exclusions relevant to this goal or an empty list if none.
    """
    exclus = []
    for exclusionSet in exclusionList:
        if goalName in exclusionSet:
            exclus = exclus + exclusionSet
    return exclus

def removeGoalByName(goalList:list, toRemove):
    listCopy = goalList.copy()
    for goal in goalList:
        if goal["name"] == toRemove:
            listCopy.remove(goal) #can't change mutable types during iteration
    return listCopy

def board(allGoals:dict, exclusionList):
    """
    Generates a list of 25 goals from the dict of goals pass as a dictionary. Goals will have a name and optionally exclusions.
    Returns a list of goal names.
    """
    goals = []
    while len(goals) < 25:
        newGoal = random.choices(allGoals, weights=[g["weight"] for g in allGoals])[0] #list comprehension to extract weights
        for excludedGoal in findExclusions(newGoal["name"], exclusionList):
            allGoals = removeGoalByName(allGoals, excludedGoal)
        if "range" in newGoal.keys(): #goal has a range
            goals.append(newGoal["name"].replace("{{X}}", str(random.choice(newGoal["range"]))))
        else: #no range, ez
            goals.append(newGoal["name"])
        try:
            allGoals.remove(newGoal)
        except ValueError: #what
            pass
    random.shuffle(goals) #mix em all up
    return goals

def bingosyncBoard(noTags=[]):
    """
    Generates a board and returns a bingosync formatted list.
    """
    boardList = board(*getAllGoals(noTags=noTags))
    out = []
    for name in boardList:
        out.append({"name": name})
    return out

def printTypes():
    """
    Prints all types and progression flags currently in use.
    """
    with open(os.path.join(ASSETS_PATH, CAT_FILENAME)) as f:
        catList = json.load(f)
    types = []
    prog = []
    for g in catList:
        for t in g["types"]:
            if t not in types:
                types.append(t)
        for p in g["progression"]:
            if p not in prog:
                prog.append(p)
    print(f"Types: {types}\n\nProg:{prog}")

def lockoutFormat():
    """
    Outputs a list of goals formatted for Lockout.Live.
    """
    mainList, _ = getAllGoals() #lockout.live doesn't acknowledge exclusions
    out = {
        "game" : "Hollow Knight: Silksong",
        "limits" : LL_LIMITS
    }
    goalsList = []
    for goalDic in mainList:
        try:
            r = goalDic["range"]
        except KeyError:
            r = []
        totTypes = goalDic["progression"] + goalDic["types"]
        bTypes = []
        lTypes = []
        for t in totTypes:
            if t == "widow":    #the difference between widow and walljump progression was small enough that categorizing things was hard
                t = "walljump"  #it was also causing balance issues. get outta here
            if t in BOARD_TYPES:
                bTypes.append(t)
            else:
                lTypes.append(t)
        newDic = {
            "goal" : goalDic["name"],
            "range": r,
            "individual_limit": 1,
            "board_categories": bTypes,
            "line_categories" : lTypes,
            "tooltip": "",
            "icons" : [],
        }
        goalsList.append(newDic)
    out["objectives"] = goalsList
    return out

def bingosyncFormat():
    """
    Outputs a list of goals formatted for bingosync.
    """
    with open(os.path.join(ASSETS_PATH, CAT_FILENAME)) as f:
        catList = json.load(f)
    goalsList = []
    for goalDic in catList["goals"]:
        if "range" in goalDic.keys():
            for x in goalDic["range"]:
                goalsList.append({"name": goalDic["name"].replace("{{X}}", str(x))})
        else:
            goalsList.append({"name": goalDic["name"]})
    return goalsList

if __name__ == "__main__":
    ####dump the current format for lockout.live
    with open(os.path.join(ASSETS_PATH,COMPUTED_SUBDIR,"silksong_lockoutlive.json"), "w") as f:
        json.dump(lockoutFormat(), f, indent=4)

    ####dump the current format for bingosync
    with open(os.path.join(ASSETS_PATH,COMPUTED_SUBDIR,"silksong_bingosync.json"), "w") as f:
        json.dump(bingosyncFormat(), f, indent=4)
    #print("File dumped.")

    ####Test bingosync format
    #print(json.dumps(bingosyncFormat()))

    ####Test lockout format
    #print(json.dumps(lockoutFormat()))

    ####Test board generation
    print(json.dumps(bingosyncBoard(noTags=["clawline","faydown"])))