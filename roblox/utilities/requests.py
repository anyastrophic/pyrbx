import asyncio
from json.decoder import JSONDecodeError
from httpx import AsyncClient


class CleanAsyncClient(AsyncClient):
    """
    This is a clean-on-delete alternative to httpx.AsyncClient.
    """

    def __init__(self):
        super(CleanAsyncClient, self).__init__()

    def __del__(self):
        # asyncio.create_task(self.client.aclose())
        try:
            asyncio.get_event_loop().create_task(self.aclose())
        except RuntimeError:
            pass


class Requests:
    def __init__(self):
        self.session = CleanAsyncClient()
        """Session to use for requests."""
        self.xcsrf_token_name = "X-CSRF-TOKEN"
        """Header that will contain the X-CSRF-TOKEN. Should be set to "X-CSRF-TOKEN" under most circumstances."""

        self.session.headers["User-Agent"] = "Roblox/WinInet"
        self.session.headers["Referer"] = "www.roblox.com"

    async def request(self, method, *args, **kwargs):
        skip_roblox = kwargs.pop("skip_roblox", False)
        handle_xcsrf_token = kwargs.pop("handle_xcsrf_token", True)
        this_request = await self.session.request(method, *args, **kwargs)

        method = method.lower()

        if handle_xcsrf_token and (
                (method == "post") or (method == "put") or (method == "patch") or (method == "delete")):
            if self.xcsrf_token_name in this_request.headers:
                self.session.headers[self.xcsrf_token_name] = this_request.headers[self.xcsrf_token_name]
                if this_request.status_code == 403:  # Request failed, send it again
                    this_request = await self.session.request(method, *args, **kwargs)

        if kwargs.pop("stream", False):
            return this_request

        try:
            this_request_json = this_request.json()
        except JSONDecodeError:
            return this_request

        if isinstance(this_request_json, dict):
            try:
                get_request_error = this_request_json["errors"]
            except KeyError:
                return this_request
        else:
            return this_request

        if skip_roblox:
            return this_request

        request_exception = status_code_error(this_request.status_code)
        raise request_exception(f"[{this_request.status_code}] {get_request_error[0]['message']}")

    async def get(self, *args, **kwargs):
        """
        Shortcut to self.request using the GET method.
        """

        return await self.request("GET", *args, **kwargs)

    async def post(self, *args, **kwargs):
        """
        Shortcut to self.request using the POST method.
        """

        return await self.request("post", *args, **kwargs)

    async def patch(self, *args, **kwargs):
        """
        Shortcut to self.request using the PATCH method.
        """

        return await self.request("patch", *args, **kwargs)

    async def delete(self, *args, **kwargs):
        """
        Shortcut to self.request using the DELETE method.
        """

        return await self.request("delete", *args, **kwargs)