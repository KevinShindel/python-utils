import time
import requests
import asyncio
import aiohttp

available_regions = ['US','BR','AU','CA','FR','DE','HK','IN','IT','ES','GB','SG']

def get_data(_region: str):

    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-timeseries"

    querystring = {"symbol": "IBM", "region": _region}

    headers = {
        "x-rapidapi-key": "6c6ad0230amshfca4ea19299e7efp1e95ecjsn8dae5b1077d2",
        "x-rapidapi-host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(f'[+] Data for region: {_region} is parsed!')
    time.sleep(1)
    return response.json()

async def async_get_data(_region: str):

    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-timeseries"

    querystring = {"symbol": "IBM", "region": _region}

    headers = {
        "x-rapidapi-key": "6c6ad0230amshfca4ea19299e7efp1e95ecjsn8dae5b1077d2",
        "x-rapidapi-host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(f'[+] Data for region: {_region} is parsed!')
    await asyncio.sleep(1)
    return response.json()

async def gather_data():
    tasks = []
    for region in available_regions:
        task = asyncio.create_task(async_get_data(region), name=region)
        tasks.append(task)

    await asyncio.gather(*tasks)
    return tasks


async def aiohttp_get_data(_region: str):
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-timeseries"
    querystring = {"symbol": "IBM", "region": _region}

    headers = {
        "x-rapidapi-key": "6c6ad0230amshfca4ea19299e7efp1e95ecjsn8dae5b1077d2",
        "x-rapidapi-host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=querystring) as response:
            print(f'[+] Data for region: {_region} is parsed!')
            await asyncio.sleep(1) # avoid throttling
            return await response.json()

async def async_main():
    start = time.perf_counter()

    tasks = [aiohttp_get_data(region) for region in available_regions]
    results = await asyncio.gather(*tasks)

    print(results)
    end = time.perf_counter()
    print(f'Task done at {round(end - start, 2)} seconds')



if __name__ == '__main__':

    # start = time.perf_counter()
    # for region in available_regions:
    #     get_data(region)
    # end = time.perf_counter()
    # print(f'All data parsed at: {round(end - start, 2)} seconds') # total 32.62 sec

    # start = time.perf_counter()
    # tasks = []
    # for region in available_regions:
    #     task = asyncio.ensure_future(async_get_data(region))
    #     task.set_name(region)
    #     tasks.append(
    #         task
    #     )
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(asyncio.wait(tasks))
    # end = time.perf_counter()
    # print(f'All data parsed at: {round(end - start, 2)} seconds') # total 16.47 seconds
    #
    # # tasks = asyncio.run(gather_data())
    #
    # result_data = {}
    # for task in tasks:
    #     result_data[task.get_name()] = task.result()
    #
    # with open('data.json', 'w', encoding='utf-8') as f:
    #     json.dump(result_data, f, ensure_ascii=False, indent=4)
    #
    # print(f'Data saved to file: data.json')

    asyncio.run(async_main())