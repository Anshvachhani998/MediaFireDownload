from time import sleep
import os

from curl_cffi import requests
from bs4 import BeautifulSoup


class MediaFireAPI:
    def __init__(self, sleep_per_download: int = 2):
        self.base_url = "https://www.mediafire.com/api/1.4/"
        self.sleep_per_download = sleep_per_download

        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        })

    def download_folder(self, folder_key: str, output_path: str):
        print(f"Downloading folder: {folder_key} in {output_path}")

        download_pages = self.__get_download_pages(folder_key)

        for download_page in download_pages:
            download_link = self.__get_download_link(download_page)
            self.__download_to_folder(download_link, output_path)

            sleep(self.sleep_per_download)

        folders = self.__get_folders(folder_key)
        for folder in folders:
            self.download_folder(folder[1], f"{output_path}/{folder[0]}")

    def __get_html_page(self, url: str):
        response = self.session.get(url, impersonate="chrome123")

        if response.ok:
            return BeautifulSoup(response.content, "html.parser")
        else:
            print(response.text)
            raise Exception(f"Failed to fetch page ({response.url}): {response.status_code}")

    def __get_folders(self, folder_key: str) -> list[(str, str)]:
        params = {
            'content_type': 'folders',
            'filter': 'all',
            'order_by': 'name',
            'order_direction': 'asc',
            'chunk': '1',
            'version': '1.5',
            'folder_key': folder_key,
            'response_format': 'json',
        }

        response = self.__api_request("folder/get_content.php", params=params)
        data = response.json()

        folders = data.get('response', {}).get('folder_content', {}).get('folders', [])
        folder_tuple = [(folder.get('name'), folder.get('folderkey')) for folder in folders]

        return folder_tuple

    def __get_download_pages(self, folder_key: str) -> list[str]:
        params = {
            'content_type': 'files',
            'filter': 'all',
            'order_by': 'name',
            'order_direction': 'asc',
            'chunk': '1',
            'version': '1.5',
            'folder_key': folder_key,
            'response_format': 'json',
        }

        response = self.__api_request("folder/get_content.php", params=params)
        data = response.json()

        files = data.get('response', {}).get('folder_content', {}).get('files', [])
        download_pages = [file.get('links', {}).get('normal_download') for file in files]

        return [page for page in download_pages if page is not None]

    def __get_download_link(self, url: str) -> str:
        html_page = self.__get_html_page(url)
        download_link = html_page.find("a", {"id": "downloadButton"})["href"]

        return download_link

    def __api_request(self, endpoint: str, params: dict = None, data: dict = None):
        url = f"{self.base_url}{endpoint}"

        response = self.session.get(url, params=params, data=data)

        if response.status_code == 200:
            return response
        else:
            raise Exception(f"API request failed: {response.status_code}")

    def __download_to_folder(self, url: str, output_path: str):
        response = self.session.get(url, stream=True)

        if response.status_code == 200:
            filename = url.split("/")[-1]
            filepath = f"{output_path}/{filename}"

            self.__check_or_create_folder(output_path)

            with open(filepath, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download: {url} ({response.status_code})")

    def __check_or_create_folder(self, folder_path: str):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
