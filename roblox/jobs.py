"""

This module contains classes intended to parse and deal with data from Roblox server instance (or "job") endpoints.

"""
from __future__ import annotations

from typing import TYPE_CHECKING

from typing import List

from .bases.basejob import BaseJob
from .bases.baseplace import BasePlace

if TYPE_CHECKING:
    from .client import Client


class GameInstancePlayerThumbnail:
    """
    Represent a player in a game instance's thumbnail.
    As the asset part of these thumbnails is no longer in use, this endpoint does not attempt to implement asset
    information.
    
    Attributes:
        url: The thumbnail's URL.
        final: Whether the thumbnail is finalized or not.
    """

    def __init__(self, client: Client, data: dict):
        self._client: Client = client

        self.url: str = data["Url"]
        self.final: bool = data["IsFinal"]

    def __repr__(self):
        return f"<{self.__class__.__name__} url={self.url!r} final={self.final}"

class GameInstance(BaseJob):
    """
    Represents a game (or place) instance, or "job".

    Attributes:
        id: The instance's job ID.
        max_players: The amount of players the server can hold.
        playing: The amount of players in the server.
        ping: The server's ping.
        fps: The server's FPS.
        place: The server's place.
    """

    def __init__(self, client: Client, data: dict, place_id: int):
        self._client: Client = client
        self.id: str = data["id"]

        super().__init__(client=self._client, job_id=self.id)

        self.max_players: int = data["maxPlayers"]
        self.playing: int = data["playing"]
        self.ping: int = data["ping"]
        self.fps: float = data["fps"]
        self.place: BasePlace = BasePlace(client=self._client, place_id=place_id)

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id!r} capacity{self.max_players}>"


class GameInstances:
    """
    Represents a game/place's active server instances.

    Attributes:
        place: The place.
        show_shutdown_all_button: Whether to show the "Shutdown All" button on the server list.
        is_game_instance_list_unavailable: Whether the list is unavailable.
        collection: A list of the game instances.
        total_collection_size: How many active servers there are.
    """

    def __init__(self, client: Client, data: dict, place_id: int):
        self._client: Client = client

        self.place: BasePlace = BasePlace(client=self._client, place_id=place_id)
        self.collection: List[GameInstance] = [
            GameInstance(
                client=self._client,
                data=instance_data,
                place_id=place_id
            ) for instance_data in data["data"]
        ]
