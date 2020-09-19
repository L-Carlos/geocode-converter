import aiohttp
from ratelimit import limits, sleep_and_retry


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
