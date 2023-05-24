"""

This module contains classes intended to parse and deal with data from Roblox place information endpoints.

"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .client import Client
from .bases.baseplace import BasePlace
from .bases.baseuniverse import BaseUniverse

class PublishResponse:
    """
    A Publish Response
    
    Attributes:
        version_number (int): Version number received from the Roblox API
    """
    def __init__(self, data: dict) -> None:
        self.version_number = data['versionNumber']

class Place(BasePlace):
    """
    Represents a Roblox place.

    Attributes:
        id: id of the place.
        name: Name of the place.
        description: Description of the place.
        url: URL for the place.
        builder: The name of the user or group who owns the place.
        builder_id: The ID of the player or group who owns the place.
        is_playable: Whether the authenticated user can play this game.
        reason_prohibited: If the place is not playable, contains the reason why the user cannot play the game.
        universe: The BaseUniverse that contains this place.
        universe_root_place: The root place that the universe contains.
        price: How much it costs to play the game.
        image_token: Can be used to generate thumbnails for this place.
        has_verified_badge: If the place has a verified badge.
    """

    def __init__(self, client: Client, data: dict):
        """
        Arguments:
            client: The Client object, which is passed to all objects this Client generates.
            data: data to make the magic happen.
        """
        super().__init__(client=client, place_id=data["placeId"])

        self._client: Client = client

        self.id: int = data["placeId"]
        self.name: str = data["name"]
        self.description: str = data["description"]
        self.url: str = data["url"]

        self.builder: str = data["builder"]
        self.builder_id: int = data["builderId"]

        self.is_playable: bool = data["isPlayable"]
        self.reason_prohibited: str = data["reasonProhibited"]
        self.universe: BaseUniverse = BaseUniverse(client=self._client, universe_id=data["universeId"])
        self.universe_root_place: BasePlace = BasePlace(client=self._client, place_id=data["universeRootPlaceId"])

        self.price: int = data["price"]
        self.image_token: str = data["imageToken"]
        self.has_verified_badge: bool = data["hasVerifiedBadge"]

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} name={self.name!r}>"

    async def publish(self, file: str):
        """Publish to this place with the specified file

        Args:
            file (str): path to the file

        Returns:
            PublishResponse: A Publish Response
        """
        publish_response = await self._client.requests.post(
            url=self._client.url_generator.get_url("apis", f"universes/v1/{self.universe.id}/places/{self.id}/versions"),
            params={
                "versionType": 'Published'
            },
            data = open(file, 'rb').read()
        )
        
        publish_data = publish_response.json()
        
        return PublishResponse(publish_data)
        