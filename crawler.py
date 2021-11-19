import requests
from bs4 import BeautifulSoup
import multiprocessing
import time
from util import prepDir

download_links = {
    2017: [ "https://aclanthology.org/volumes/I17-1/", #104
            "https://aclanthology.org/volumes/I17-2/", #77
            "https://aclanthology.org/volumes/I17-3/", #18
            "https://aclanthology.org/volumes/I17-4/", #37
            "https://aclanthology.org/volumes/I17-5/", #7
            ],
    2019: [ "https://aclanthology.org/volumes/D19-1/", #682
            "https://aclanthology.org/volumes/D19-2/", #7 no pdfs
            "https://aclanthology.org/volumes/D19-3/", #45
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
