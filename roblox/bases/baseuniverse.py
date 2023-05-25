"""

This file contains the BaseUniverse object, which represents a Roblox universe ID.
It also contains the UniverseLiveStats object, which represents a universe's live stats.

"""

from __future__ import annotations
from typing import TYPE_CHECKING, Dict, List, Union

from datetime import datetime
from dateutil.parser import parse

from .baseitem import BaseItem
from ..gamepasses import GamePass
from ..sociallinks import SocialLink
from ..utilities.iterators import PageIterator, SortOrder

if TYPE_CHECKING:
    from ..client import Client
    from ..badges import Badge

class UniverseLiveStats:
    """
    Represents a universe's live stats.

    Attributes:
        total_player_count: The amount of players present in this universe's subplaces.
        game_count: The amount of active servers for this universe's subplaces.
        player_counts_by_device_type: A dictionary where the keys are device types and the values are the amount of
                                      this universe's subplace's active players which are on that device type.
    """

    def __init__(self, data: dict):
        self.total_player_count: int = data["totalPlayerCount"]
        self.game_count: int = data["gameCount"]
        self.player_counts_by_device_type: Dict[str, int] = data["playerCountsByDeviceType"]


def _universe_badges_handler(client: Client, data: dict) -> Badge:
    # inline imports are used here, sorry
    from ..badges import Badge # pylint: disable=import-outside-toplevel
    return Badge(client=client, data=data)

class StandardDatastore: # TODO: Create basedatastore.py, datastores.py and rearrange this code accordingly
    """
    Represents a datastore for a Universe.

    Attributes:
        created: When this datastore was made
        name: The name of this datastore
    """

    def __init__(self, client: Client, data: dict, universe: Union[BaseUniverse, int]):
        self._client: Client = client
        self.name: str = data["name"]
        self.created: datetime = parse(data["createdTime"])
        if isinstance(universe, int):
            self.universe = BaseUniverse(client=self._client, universe_id=universe)
        else:
            self.universe = universe

    async def set_entry(self, entry_key: str, entry_value: any):
        """Sets an entry in the datastore

        Args:
            entry_key (str): The key for the entry
            entry_value (any): The value for the entry

        Returns:
            any: Currently returns JSON, Object coming soon
        """
        entry_response = await self._client.requests.post(
            url=self._client.url_generator.get_url("apis", f"datastores/v1/universes/{self.universe.id}/standard-datastores/datastore/entries/entry?datastoreName={self.name}&entryKey={entry_key}"),
            json=entry_value
        )
        entry_data = entry_response.json()
        # TODO: Make EntryVersion object to respond with
        return entry_data
    
    async def get_entry(self, entry_key: str):
        """Gets an entry from the datastore

        Args:
            entry_key (str): The key for the entry

        Returns:
            any: Currently returns JSON, Object coming soon
        """
        entry_response = await self._client.requests.get(
            url=self._client.url_generator.get_url("apis", f"datastores/v1/universes/{self.universe.id}/standard-datastores/datastore/entries/entry?datastoreName={self.name}&entryKey={entry_key}"),
        )
        entry_data = entry_response.json()
        
        return entry_data


class BaseUniverse(BaseItem):
    """
    Represents a Roblox universe ID.

    Attributes:
        id: The universe ID.
    """

    def __init__(self, client: Client, universe_id: int):
        """
        Arguments:
            client: The Client this object belongs to.
            universe_id: The universe ID.
        """

        self._client: Client = client
        self.id: int = universe_id # pylint: disable=invalid-name

    async def get_favorite_count(self) -> int:
        """
        Grabs the universe's favorite count.

        Returns:
            The universe's favorite count.
        """
        favorite_count_response = await self._client.requests.get(
            url=self._client.url_generator.get_url("games", f"v1/games/{self.id}/favorites/count")
        )
        favorite_count_data = favorite_count_response.json()
        return favorite_count_data["favoritesCount"]

    async def is_favorited(self) -> bool:
        """
        Grabs the authenticated user's favorite status for this game.

        Returns:
            Whether the authenticated user has favorited this game.
        """
        is_favorited_response = await self._client.requests.get(
            url=self._client.url_generator.get_url("games", f"v1/games/{self.id}/favorites")
        )
        is_favorited_data = is_favorited_response.json()
        return is_favorited_data["isFavorited"]

    def get_badges(self, page_size: int = 10, sort_order: SortOrder = SortOrder.Ascending,
                   max_items: int = None) -> PageIterator:
        """
        Gets the universe's badges.

        Arguments:
            page_size: How many members should be returned for each page.
            sort_order: Order in which data should be grabbed.
            max_items: The maximum items to return when looping through this object.

        Returns:
            A PageIterator containing this universe's badges.
        """

        return PageIterator(
            client=self._client,
            url=self._client.url_generator.get_url("badges", f"v1/universes/{self.id}/badges"),
            page_size=page_size,
            sort_order=sort_order,
            max_items=max_items,
            handler=_universe_badges_handler,
        )

    async def get_live_stats(self) -> UniverseLiveStats:
        """
        Gets the universe's live stats.
        This data does not update live. These are just the stats that are shown on the website's live stats display.

        Returns:
            The universe's live stats.
        """
        stats_response = await self._client.requests.get(
            url=self._client.url_generator.get_url("develop", f"v1/universes/{self.id}/live-stats")
        )
        stats_data = stats_response.json()
        return UniverseLiveStats(data=stats_data)

    def get_gamepasses(self, page_size: int = 10, sort_order: SortOrder = SortOrder.Ascending,
                       max_items: int = None) -> PageIterator:
        """
        Gets the universe's gamepasses.

        Arguments:
            page_size: How many members should be returned for each page.
            sort_order: Order in which data should be grabbed.
            max_items: The maximum items to return when looping through this object.

        Returns:
            A PageIterator containing the universe's gamepasses.
        """

        return PageIterator(
            client=self._client,
            url=self._client.url_generator.get_url("games", f"v1/games/{self.id}/game-passes"),
            page_size=page_size,
            sort_order=sort_order,
            max_items=max_items,
            handler=lambda client, data: GamePass(client, data), # pylint: disable=unnecessary-lambda
        )

    async def get_social_links(self) -> List[SocialLink]:
        """
        Gets the universe's social links.

        Returns:
            A list of the universe's social links.
        """

        links_response = await self._client.requests.get(
            url=self._client.url_generator.get_url("games", f"v1/games/{self.id}/social-links/list")
        )
        links_data = links_response.json()["data"]
        return [SocialLink(client=self._client, data=link_data) for link_data in links_data]
    
    async def get_standard_datastores(self) -> List[StandardDatastore]:
        """Gets datastores of Universe

        Returns:
            A list of StandardDatastores
        """
        
        datastores_response = await self._client.requests.get(
            url=self._client.url_generator.get_url("apis", f"datastores/v1/universes/{self.id}/standard-datastores")
        )
        datastores_data = datastores_response.json()["datastores"]
        return [StandardDatastore(client=self._client, data=datastore_data, universe=self) for datastore_data in datastores_data]
    
    async def get_standard_datastore(self, datastore_name: str) -> StandardDatastore:
        """Gets datastore by name
        
        Arguments:
            datastore_name: The name of the datastore

        Returns:
            StandardDatastore: The datastore
        """
        
        datastores_response = await self._client.requests.get(
            url=self._client.url_generator.get_url("apis", f"datastores/v1/universes/{self.id}/standard-datastores?limit=100")
        )
        datastores_data = datastores_response.json()["datastores"]
        
        for datastore in datastores_data:
            if datastore["name"] == datastore_name:
                return StandardDatastore(
                    client=self._client,
                    data=datastore,
                    universe=self
                )
    
    async def publish_message(self, topic: str, message: str) -> int:
        """Publishes a message using the Cloud API.

        Args:
            topic (str): Topic
            message (str): Message

        Returns:
            int: Status code
        """

        publish_response = await self._client.requests.post(
            url=self._client.url_generator.get_url("apis", f"messaging-service/v1/universes/{self.id}/topics/{topic}"),
            json={"message": message}
        )
        return publish_response.status_code