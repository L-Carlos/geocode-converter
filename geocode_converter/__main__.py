import asyncio
from .client import fetch, parse_dict
from .excel import load_file, output_data
from .configs import Configs


async def main():

    print(f"\n> Reading file at {Configs.INPUT_FILE} ...\n")
    data_input = load_file(Configs.INPUT_FILE)

    data_output = []

    print(f"> Searching geocoordinates ...\n")
    for item in data_input:
        search = await fetch(
            latitude=item["latitude"],
            longitude=item["longitude"],
            api_key=Configs.API_KEY,
        )
        if search is not None:
            result = await parse_dict(search)

            merged_result = {**item, **result}

            data_output.append(merged_result)

    print("> Search Complete, saving file ...\n")
    output_data(data_output, Configs.OUTPUT_FILE)
    print(f"> Data saved at {Configs.OUTPUT_FILE}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
