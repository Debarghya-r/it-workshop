import requests
from bs4 import BeautifulSoup
import multiprocessing
import time
from util import prepDir

download_links = {
    2020: [ "https://aclanthology.org/volumes/2020.coling-main/", #613
            "https://aclanthology.org/2020.coling-demos", #17
            "https://aclanthology.org/2020.coling-tutorials", #8
            "https://aclanthology.org/2020.coling-industry", #23
            "https://aclanthology.org/volumes/I17-5/", #7
            "https://aclanthology.org/2020.argmining-1",#14
           "https://aclanthology.org/2020.semeval-1",#301
           "https://aclanthology.org/2020.wanlp-1",#35
            ]
}
pdf_root_dir= "./assets/papers/IJCNLP/pdf/"

def getFilesToDownload():
        files_to_download : list[str] = []
        for conference_page_link in (download_links[2017] + download_links[2019]):
                page = requests.get(conference_page_link)
                soup = BeautifulSoup(page.content, "html.parser")
                results = soup.find_all("a", class_="badge badge-primary align-middle mr-1", href=True)
                for pdf_element in results:
                        files_to_download.append(pdf_element["href"])
        return files_to_download 


def downloadFile(pub_pdf_link, suffix):
        response = requests.get(pub_pdf_link)
        with open(f"{pdf_root_dir}doc{suffix}.pdf", 'wb') as f:
                f.write(response.content)

def downloadAllFiles():
        files_to_download = getFilesToDownload()
        index_array = list(range(0, len(files_to_download)))
        packed_args = tuple(zip(files_to_download, index_array))

        with multiprocessing.Pool(processes=50) as pool:
                pool.starmap(downloadFile, packed_args)

def crawl():
        prepDir([pdf_root_dir])

        print("Crawling the website and downloading the Papers....")

        start_time = time.time()
        downloadAllFiles()
        end_time = time.time()

        print(f"Papers Downloaded in {end_time - start_time} seconds\n")


if __name__ == "__main__" :
        crawl()
