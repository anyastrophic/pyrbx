from ro_py import User
import requests

endpoint = "https://games.roblox.com/"


class Votes:
    def __init__(self, votes_data):
        self.up_votes = votes_data["upVotes"]
        self.down_votes = votes_data["downVotes"]


class Game:
    def __init__(self, universe_id):
        self.id = universe_id
        game_info_req = requests.get(
            url=endpoint + "v1/games",
            params={
                "universeIds": str(self.id)
            }
        )
        game_info = game_info_req.json()
        game_info = game_info["data"][0]
        self.name = game_info["name"]
        self.description = game_info["description"]
        if game_info["creator"]["type"] == "User":
            self.creator = User(game_info["creator"]["id"])
        self.price = game_info["price"]
        self.allowed_gear_genres = game_info["allowedGearGenres"]
        self.allowed_gear_categories = game_info["allowedGearCategories"]
        self.max_players = game_info["maxPlayers"]
        self.studio_access_to_apis_allowed = game_info["studioAccessToApisAllowed"]
        self.create_vip_servers_allowed = game_info["createVipServersAllowed"]

    def get_votes(self):
        votes_info_req = requests.get(
            url=endpoint + "v1/games/votes",
            params={
                "universeIds": str(self.id)
            }
        )
        votes_info = votes_info_req.json()
        votes_info = votes_info["data"][0]
        votes = Votes(votes_info)
        return votes
