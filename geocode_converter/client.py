import asyncio

import aiohttp
from ratelimit import limits, sleep_and_retry

from .configs import Configs


@sleep_and_retry
@limits(calls=1, period=1)
async def fetch(latitude: float, longitude: float, api_key: str) -> dict:
    url: str = "https://us1.locationiq.com/v1/reverse.php"
    payload: dict = {
        "key": api_key,
        "lat": str(latitude),
        "lon": str(longitude),
        "normalizeaddress": 1,
        "format": "json",
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, params=payload) as response:
            try:
                assert response.status == 200
            except AssertionError:
                print(f"> error code {response.status}\n")
                return None

            return await response.json()


async def parse_dict(dict_obj: dict) -> dict:
    address = dict_obj.get("address", None)
    display_name = dict_obj.get("display_name", None)

    if address is not None:
        return {
            "display_name": display_name,
            "name": address.get("name"),
            "house_number": address.get("house_number"),
            "road": address.get("road"),
            "neighbourhood": address.get("neighbourhood"),
            "suburb": address.get("suburb"),
            "island": address.get("island"),
            "city": address.get("city"),
            "county": address.get("county"),
            "state": address.get("state"),
            "state_code": address.get("state_code"),
            "postcode": address.get("postcode"),
            "country": address.get("country"),
            "country_code": address.get("country_code"),
        }

    else:
        print("dict doesn't have the 'address' key")
        return None


"""
async def main():

    items = [
        [-26.245412, -48.804151],
        [-26.338351, -48.805051],
        [-26.289929, -48.774843],
        [-23.987037, -46.296200],
        [-26.245412, -48.804151],
        [-26.338351, -48.805051],
        [-26.289929, -48.774843],
        [-23.987037, -46.296200],
    ]

    for id, item in enumerate(items):
        search = await fetch(*item, Configs.API_KEY)
        if search is not None:
            result = await parse_dict(search)
            print(id, result)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
"""