import os
import time
import requests
from urllib.parse import urlparse
import threading
from multiprocessing import Process
import asyncio
import aiohttp
import argparse

parser = argparse.ArgumentParser(description='Download images from URLs')
parser.add_argument('urls', metavar='URL', type=str, nargs='+',
                    help='list of URLs to download')
args = parser.parse_args()

urls = args.urls

# urls = ['https://wp-s.ru/wallpapers/9/16/559439035761618/uyutnyj-domik-u-vody-v-ya-islandii.jpg',
#             'https://new-science.ru/wp-content/uploads/2024/01/587.jpg',
#             'https://st-gdefon.gallery.world/wallpapers_original/653134_gallery.world.jpg',
#             'https://mykaleidoscope.ru/x/uploads/posts/2022-09/1663091157_62-mykaleidoscope-ru-p-gollandiya-vkontakte-68.jpg',
#             'https://mykaleidoscope.ru/x/uploads/posts/2022-09/1663411336_3-mykaleidoscope-ru-p-portugaliya-azorskie-ostrova-krasivo-3.jpg',
#             'http://media.gq.com/photos/597f928b0a1a9d4a0b9e4f4d/master/w_1600%252Cc_limit/2017_07_GQ_PortugalBeaches_Azores.jpg',
#             'https://www.youloveit.ru/uploads/posts/2019-12/1575158276_youloveit_ru_zima_i_gyvotnye06.jpg',
#             'https://i.pinimg.com/originals/5f/ac/e1/5face126d2691cd75f7e54e3ba293f06.jpg',
#             'https://мояпоходнаяжизнь.рф/wp-content/uploads/2023/09/%D0%B1%D0%B0%D0%B9%D0%BA%D0%B0%D0%BB-03-min.jpeg',
#             'http://static.tildacdn.com/tild6365-3833-4231-b931-373730316430/baikal_1.jpg'
#             ]

def checkUrls():
    folder = 'images'
    if not os.path.exists(folder):
        os.mkdir(folder)
    for url in urls:
        filename = os.path.basename(url)
        filepath = os.path.join(folder, filename)
        download_image(url, filepath)


def download_image(url, filepath):
    response = requests.get(url)
    with open(filepath, 'wb') as f:
        f.write(response.content)

async def async_download_image(url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            contents = await response.read()
            with open(filename, "wb") as f:
                f.write(contents)

if __name__ == '__main__':
    start_time = time.time()
    checkUrls()
    print(f'Синхронный подход {time.time() - start_time:.2f} секунд')

    threads = []
    start_time = time.time()
    folder = 'images'
    if not os.path.exists(folder):
        os.mkdir(folder)

    for url in urls:
        filename = os.path.basename(urlparse(url).path)
        filepath = os.path.join(folder, filename)
        thread = threading.Thread(target=download_image, args=[url, filepath])
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    print(f'Многопоточный подход {time.time() - start_time:.2f} секунд')

    processes = []
    start_time = time.time()
    folder = 'images'
    if not os.path.exists(folder):
        os.mkdir(folder)

    for url in urls:
        filename = os.path.basename(urlparse(url).path)
        filepath = os.path.join(folder, filename)
        process = Process(target=download_image, args=[url, filepath])
        process.start()
        processes.append(process)
    for process in processes:
        process.join()
    print(f'Многопроцессорный подход {time.time() - start_time:.2f} секунд')

    tasks = []
    start_time = time.time()
    folder = 'images'
    if not os.path.exists(folder):
        os.mkdir(folder)
    for url in urls:
        filename = os.path.basename(urlparse(url).path)
        filepath = os.path.join(folder, filename)
        task = asyncio.ensure_future(async_download_image(url, filepath))
        tasks.append(task)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    print(f'Асинхронный подход {time.time() - start_time:.2f} секунд')