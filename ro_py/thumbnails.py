"""

This file houses functions and classes that pertain to Roblox icons and thumbnails.

"""

from ro_py.utilities.errors import InvalidShotTypeError

endpoint = "https://thumbnails.roblox.com/"

# TODO: turn these into enums
PlaceHolder = "PlaceHolder"
AutoGenerated = "AutoGenerated"
ForceAutoGenerated = "ForceAutoGenerated"

AvatarFullBody = 0
AvatarBust = 1
AvatarHeadshot = 2

size_30x30 = "30x30"
size_42x42 = "42x42"
size_48x48 = "48x48"
size_50x50 = "50x50"
size_60x62 = "60x62"
size_75x75 = "75x75"
size_110x110 = "110x110"
size_128x128 = "128x128"
size_140x140 = "140x140"
size_150x150 = "150x150"
size_160x100 = "160x100"
size_250x250 = "250x250"
size_256x144 = "256x144"
size_256x256 = "256x256"
size_300x250 = "300x240"
size_304x166 = "304x166"
size_384x216 = "384x216"
size_396x216 = "396x216"
size_420x420 = "420x420"
size_480x270 = "480x270"
size_512x512 = "512x512"
size_576x324 = "576x324"
size_720x720 = "720x720"
size_768x432 = "768x432"

format_png = "Png"
format_jpg = "Jpeg"
format_jpeg = "Jpeg"


class ThumbnailGenerator:
    """
    This object is used to generate thumbnails.
    """
    def __init__(self, requests):
        self.requests = requests

    def get_group_icon(self, group, size=size_150x150, file_format=format_png, is_circular=False):
        """
        Gets a group's icon.
        :param group: The group.
        :param size: The thumbnail size, formatted widthxheight.
        :param file_format: The thumbnail format
        :param is_circular: The circle thumbnail output parameter.
        :return: Image URL
        """
        group_icon_req = self.requests.get(
            url=endpoint + "v1/groups/icons",
            params={
                "groupIds": str(group.id),
                "size": size,
                "file_format": file_format,
                "isCircular": is_circular
            }
        )
        group_icon = group_icon_req.json()["data"][0]["imageUrl"]
        return group_icon

    def get_game_icon(self, game, size=size_256x256, file_format=format_png, is_circular=False):
        """
        Gets a game's icon.
        :param game: The game.
        :param size: The thumbnail size, formatted widthxheight.
        :param file_format: The thumbnail format
        :param is_circular: The circle thumbnail output parameter.
        :return: Image URL
        """
        game_icon_req = self.requests.get(
            url=endpoint + "v1/games/icons",
            params={
                "universeIds": str(game.id),
                "returnPolicy": PlaceHolder,
                "size": size,
                "file_format": file_format,
                "isCircular": is_circular
            }
        )
        game_icon = game_icon_req.json()["data"][0]["imageUrl"]
        return game_icon

    def get_avatar_image(self, user, shot_type=AvatarFullBody, size=None, file_format=format_png, is_circular=False):
        """
        Gets a full body, bust, or headshot image of a user.
        :param user: User to use for avatar.
        :param shot_type: Type of shot.
        :param size: The thumbnail size, formatted widthxheight.
        :param file_format: The thumbnail format
        :param is_circular: The circle thumbnail output parameter.
        :return: Image URL
        """
        shot_endpoint = endpoint + "v1/users/"
        if shot_type == AvatarFullBody:
            shot_endpoint = shot_endpoint + "avatar"
            size = size or size_30x30
        elif shot_type == AvatarBust:
            shot_endpoint = shot_endpoint + "avatar-bust"
            size = size or size_50x50
        elif shot_type == AvatarHeadshot:
            size = size or size_48x48
            shot_endpoint = shot_endpoint + "avatar-headshot"
        else:
            raise InvalidShotTypeError("Invalid shot type.")
        shot_req = self.requests.get(
            url=shot_endpoint,
            params={
                "userIds": str(user.id),
                "size": size,
                "file_format": file_format,
                "isCircular": is_circular
            }
        )
        return shot_req.json()["data"][0]["imageUrl"]
