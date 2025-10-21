import os, json, random

#file paths and names
ASSETS_PATH = "assets"
COMPUTED_SUBDIR = "generated"
GOALS_FILENAME = "silksong-v6.json"
CAT_FILENAME = "categorized_v2.json"

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


def getAllGoals(fname = CAT_FILENAME, exclusions = False):
    """
    Loads goals file into code. Outputs one list of goal dictionaries and another list of exclusive goal lists. 
    Only one goal from each exclusive list can be present in the final board.
    """
    with open(os.path.join(ASSETS_PATH, fname)) as f:
        fileObj = json.load(f)
    if exclusions: #it's the uncategorized list
        goals = fileObj[0]
        uniques = fileObj[1]
        goals = processGoalList(goals)
        uniques = processUniquesList(uniques)
        return goals, uniques
    else:
        return fileObj

def processGoalList(rawGoals):
    """
    Goals are provided in an odd format with exclusions set to true. Process them into a simple list of names.
    """
    out = []
    for goal in rawGoals:
        out.append(goal["name"])
    return out

def processUniquesList(rawExclus):
    """
    Exclusions are provided in an odd format. Process them into a simple list of lists.
    """
    out = []
    for l in rawExclus:
        out.append(l["unique"])
    return out

def findExclusions(goalName, exclusionList):
    """
    Given a goal name and the main exclusion list, returns the exclusions relevant to this goal or an empty list if none.
    """
    exclus = []
    for exclusionSet in exclusionList:
        if goalName in exclusionSet:
            exclus = exclus + exclusionSet
    return exclus

def board(allGoals:list, exclusionList):
    """
    Generates a list of 25 goals from the list of goals pass as a dictionary. Goals will have a name and optionally exclusions.
    Returns a list of dictionaries like {"name": "GOAL_NAME"} because that's what bingosync wants for some reason.
    """
    goals = []
    while len(goals) < 25:
        newGoal = random.choice(allGoals)
        for excludedGoal in findExclusions(newGoal, exclusionList):
            try:
                allGoals.remove(excludedGoal)
            except ValueError: #goal not present in list, job done
                pass
        goals.append(newGoal)
        try:
            allGoals.remove(newGoal)
        except ValueError:
            pass
    random.shuffle(goals)
    return goals

def defaultBoard():
    """
    Generates a board using the default settings and returns a bingosync formatted list.
    """
    boardList = board(*getAllGoals(fname=GOALS_FILENAME, exclusions=True))
    out = []
    for name in boardList:
        out.append({"name": name})
    return out

def compareLists():
    oldGoals, _ = getAllGoals(exclusions=True)
    noMatchRose = oldGoals.copy()
    with open(os.path.join(ASSETS_PATH, CAT_FILENAME)) as f:
        catList = json.load(f)
    catListNames = [g["name"] for g in catList]
    noMatchCatList = catList.copy()
    for goal in catList:
        if goal["name"] in noMatchRose:
            noMatchRose.remove(goal["name"])
    for goal in oldGoals:
        if goal in catListNames:
            catListNames.remove(goal)
            
    return f"Goals that exist without categories: {noMatchRose}\n\nGoals that have categories that aren't in Rose's list: {catListNames}"

def printTypes():
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
    with open(os.path.join(ASSETS_PATH, CAT_FILENAME)) as f:
        catList = json.load(f)
    out = {
        "game" : "Hollow Knight: Silksong",
        "limits" : LL_LIMITS
    }
    goalsList = []
    for goalDic in catList["goals"]:
        try:
            r = goalDic["range"]
        except KeyError:
            r = []
        totTypes = goalDic["progression"] + goalDic["types"]
        bTypes = []
        lTypes = []
        for t in totTypes:
            if t == "widow":
                t = "walljump"
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

if __name__ == "__main__":
    #dump the current format for lockout.live
    with open(os.path.join(ASSETS_PATH,COMPUTED_SUBDIR,"silksong_lockoutlive_v1.json"), "w") as f:
        json.dump(lockoutFormat(), f, indent=4)
    print("File dumped.")