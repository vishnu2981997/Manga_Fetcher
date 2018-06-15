"""
Manga-Fetcher : downloads a desired chapter of a desired manga from www.MangaFreak.com
"""
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver


def search_results(manga, count):
    """
    :param manga: name of the manga
    :param count: an integer value
    :return: the function itself
    """

    global s_no

    # Getting the source code of the page

    soup = get_source(manga, count, False)

    # Fetching individual search result frames

    frames = soup.find_all("div", {"class" : "mb-right"})

    count += 1

    # Finding all available search results

    for frame in frames:

        frame = frame.find("a")

        name = frame.get_text()

        link = frame["href"]

        s_no += 1

        avaliable[s_no] = [name, link]

    if s_no/25 == float(count) and count == int(s_no/25):

        return search_results(manga, count)

    else:

        return 0

def get_source(manga, count, full):
    """
    :param manga: name of the manga
    :param count: an integer value
    :param full: an integer value to indicate the view full of the page
    :return: source code of the page
    """

    # Generating url

    if count == False and full != 1:

        url = manga

    elif full == 1:

        url = manga+"/full"

    else:

        url = "http://www.mangafreak.com/manga-search?key="+manga+"&page="+str(count)

    # Fetching url

    driver.get(url)

    html = driver.page_source

    # Getting source code

    soup = BeautifulSoup(html, "lxml")

    return soup

def get_latest_chapters():
    """
    :return: Null
    """

    global c_no

    global option

    # Getting user input

    option = int(input("\nSelect your option : "))

    print("\n")

    # Fetching the available chapters source_code

    manga = avaliable[option][1]

    soup = get_source(manga, False, False)

    # Fetching available chapters names and links

    chapters = soup.find("div", {"class" : "manga-latest"}).find("ul", {"class" : "ml-list"})

    chapters = chapters.find_all("a")

    for chapter in chapters:

        number = chapter.get_text()

        number = number.split()

        number = " ".join(i for i in number[-2:])

        link = chapter["href"]

        c_no += 1

        latest_chapters[c_no] = [number, link]

def get_chapter():
    """
    :return: Null
    """

    p_no = 1

    # Getting user input

    opt = int(input("\nEnter your option : "))

    print("\n")

    # Fetching source code of the desired chapter

    soup = get_source(latest_chapters[opt][1], False, 1)

    pages = soup.find("div", {"class" : "chapter-container"})

    # Fetching all pages

    pages = pages.find_all("img")

    folder = "manga"

    # Creating main folder if dose not exist

    if not os.path.exists(folder):

        os.mkdir(folder)

    folder = os.path.join(folder, avaliable[option][0])

    # Creating sub folder if dose not exist
    if not os.path.exists(folder):

        os.mkdir(folder)

    folder = os.path.join(folder, latest_chapters[opt][0])

    # Creating folder for each chapter if dose not exist

    if not os.path.exists(folder):

        os.mkdir(folder)

    print("\nTotal images : "+str(len(pages)))

    # Downloading and saving pages into the specific folder

    for page in pages:

        page = page["src"]

        img = requests.get(page)

        print("Downloading "+str(p_no)+"/"+str(len(pages)))

        fp = open(os.path.join(folder, str(p_no)+".jpg"), 'wb')

        fp.write(img.content)

        fp.close()

        p_no += 1

def display_search_results(count):
    """
    :param count: an integer value
    :return: function itself
    """

    if count == len(avaliable)+1:

        return 0

    else:

        # Printing all search results

        print(str(count)+"   "+avaliable[count][0])

        return display_search_results(count+1)

def display_latest_chapters(count):
    """
    :param count: an integer value
    :return: function itself
    """

    if count == len(latest_chapters)+1:

        return 0

    else:

        # Printing latest chapters

        print(str(count)+"   "+latest_chapters[count][0])

        return display_latest_chapters(count+1)

def main():
    """
    :return: Null
    """

    global driver, avaliable, s_no, latest_chapters, c_no

    # Getting manga name

    manga = input("Enter the name of the manga : ").strip()

    print("\n")

    manga = manga.replace(" ", "+")

    # Initializing chrome driver

    driver = webdriver.Chrome()

    avaliable = {}

    latest_chapters = {}

    count = 1

    s_no = 0

    c_no = 0

    # Fetching all possible results

    search_results(manga, count)

    # Displaying search results

    display_search_results(count)

    # Fetching the latest chapters

    get_latest_chapters()

    # Displaying the latest chapters

    display_latest_chapters(count)

    # Downloading the specific chapter into the corresponding folder

    get_chapter()

if __name__ == "__main__":
    main()