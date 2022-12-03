import re
import ssl
import certifi
import asyncio
import aiohttp
from bs4 import BeautifulSoup

jokes_list = list()


async def get_page_info(session, page: int, start_page: int):
    global jokes_list

    if page == start_page:
        url = 'https://anekdotov.net'
    else:
        url = f'https://anekdotov.net/arc/{page}.html'

    async  with session.get(url) as response:
        try:
            response_text = await response.text()

            page_info = BeautifulSoup(response_text, 'html.parser')

            jokes = page_info.find_all('div', class_='anekdot')
            for joke in jokes:
                jokes_list.append(joke.text.strip())

        except Exception as ex:
            print(repr(ex))


async def load_page_info():
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    conn = aiohttp.TCPConnector(ssl=ssl_context)
    headers = {
        'accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / avif, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3;q = 0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.72',
    }

    async with aiohttp.ClientSession(connector=conn, headers=headers) as session:
        async with session.get(url='https://anekdotov.net') as response:
            try:
                response_text = await response.text()
                page_info = BeautifulSoup(response_text, 'html.parser')

                page = page_info.find_all('a', string='Д А Л Е Е!', href=True)
                for href in page:
                    count_of_pages = int(re.sub('[\\D]', '', href['href']))

            except Exception as ex:
                print(repr(ex))

        tasks = []
        for page in range(count_of_pages - 1, count_of_pages):
            task = asyncio.create_task(get_page_info(session=session, page=page, start_page=count_of_pages - 1))
            tasks.append(task)

        await asyncio.gather(*tasks)

async def run_tasks():
    global jokes_list
    await load_page_info()
    print(jokes_list)
    for joke in jokes_list:
        print(joke)
        print()
    print(len(jokes_list))

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(run_tasks())
