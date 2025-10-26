import requests, json, random

ROOM_NAMES = [
    "Abyssopelagic Zone",
    "Rose Garden",
    "Not a Human Hand",
    "Almost a Tundra",
    "Sentient Blobs",
    "Not Haxball",
    "Roman Emperor",
    "Skongin It",
    "Fa Ri Du La Ci Ma Ne",
    "POSHANKA",
    "Savage Beastfly"
]

STANDARD_PAYLOAD = {
    "game_type": 18, #custom game
    "variant_type": 18, #custom game, both are required
    #The following can be adjusted on a case-by-case basis
    "seed": "",
    "hide_card" : 1,
    "custom_json" : None,
    "lockout_mode" : 1 #1 is no lockout
}

NEW_CARD_PAYLOAD = STANDARD_PAYLOAD.copy()
NEW_CARD_PAYLOAD.update({
    "nickname" : "Bingyflea",
    #update pretty much all of these
    "room_name" : "",
    "passphrase" : "fast"
})

class bingosyncClient():
    """
    Opens a bingosync session with the correct csrf cookies!! Very exciting.
    Implements api methods for bingosync as well probably.
    """
    roomId = None

    def __init__(self):
        self.session = requests.Session()
        #Using a session automatically persists cookies!
        #set user-agent header:
        self.session.headers.update({
            "User-Agent" : "Silksong.Bingogenerator/0.1",
            "Origin": "https://bingosync.com",
            "Host": "bingosync.com",
        })
        #Make a request to get them cookies
        r = self.session.get("https://bingosync.com/")

        self.csrfToken = self.session.cookies["csrftoken"]

    def newRoom(self, boardJSON, hideCard = True, lockout=False, roomName=None, passphrase="fast", seed = ""):
        """
        Opens a new room and sets the instance roomId.
        """ 
        formData = NEW_CARD_PAYLOAD.copy()
        #need to update the following
        formData.update({
            "hide_card" : 1 if hideCard else 0,
            "lockout_mode" : 0 if lockout else 1,
            "custom_json" : boardJSON,
            "passphrase" : passphrase,
            "seed": seed
        })
        if roomName is None:
            formData["room_name"] = random.choice(ROOM_NAMES)
        else:
            formData["room_name"] = roomName
        formData["csrfmiddlewaretoken"] = [self.csrfToken, self.csrfToken]
        response = self.session.post("https://bingosync.com/", data=formData, allow_redirects=False)
        if response.status_code == 302: #expected
            #save the room ID and then disconnect from it
            self.roomId = response.headers["location"].split("/")[2]
            self.session.get(f"https://bingosync.com/room/{self.roomId}/disconnect")
        return formData["room_name"], self.roomId

    def updateCard(self, roomID, boardJSON, hideCard = True, lockout = False, roomName=None, passphrase="fast", seed = ""):
        """
        Updates a room's card with a new board.
        """
        formData = STANDARD_PAYLOAD.copy()
        #need to update the following
        formData.update({
            "room": roomID,
            "hide_card" : 1 if hideCard else 0,
            "lockout_mode" : 0 if lockout else 1,
            "custom_json" : boardJSON,
            "seed": seed
        })
        formData["csrfmiddlewaretoken"] = [self.csrfToken, self.csrfToken]
        response = self.session.post("https://bingosync.com/api/new-card", data=formData)
        return response


    def close(self):
        """
        Closes the session.
        """
        self.session.close()


if __name__ == "__main__":
    c = bingosyncClient()
    rId = c.newRoom('[{"name": "2 Gather Quests"}, {"name": "Obtain a Crafting Kit"}, {"name": "Fully Unlock a Non-Hunter\'s Crest"}, {"name": "Cogwork Dancers"}, {"name": "Savage Beastfly"}, {"name": "3 Blue Tools"}, {"name": "Vaultkeeper\'s Melody"}, {"name": "Phantom"}, {"name": "Moss Mother Duo"}, {"name": "Delver\'s Drill"}, {"name": "Win Against Lumble The Lucky"}, {"name": "Twisted Bud"}, {"name": "Repair Silkshot"}, {"name": "Have 4 Rosary Strings"}, {"name": "Widow"}, {"name": "Sinner\'s Road & Marrows Flea [2]"}, {"name": "Complete 5 Quests"}, {"name": "Crawbug Clearing"}, {"name": "Pollip Pouch"}, {"name": "Sister Splinter"}, {"name": "Moorwing"}, {"name": "2 Wayfarer Quests"}, {"name": "Craggler"}, {"name": "Defeat a Cogwork Clapper"}, {"name": "Pay for a Flea Spa"}]')
    c.close()