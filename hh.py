from bs4 import BeautifulSoup
import requests
import sqlite3
import pandas as pd

db_file = "jobs.bd"
job_name_search = "python"
items = 20
url = f"https://hh.ru/search/vacancy?text={job_name_search}&items_on_page=20"

def update_job_name_search(new_job_name):
    global job_name_search
    job_name_search = new_job_name
    global url
    url = f"https://hh.ru/search/vacancy?text={job_name_search}&items_on_page=20"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "TE": "Trailers"
    }

def extr_max_page():

    hh_request = requests.get(url, headers = headers)
    hh_soup = BeautifulSoup(hh_request.text, "html.parser")

    #достаем номера страниц
    paginator = hh_soup.find("div", {"class": "pager"})
    pages = paginator.find_all("a")
    page_nubmers = [page.get_text() for page in pages]
    max_page = int(page_nubmers[-2]) 

    return max_page




def extr_hh_jobs(last_page):

    conn = sqlite3.connect('/Users/malfurion/Desktop/Практика/Parser/jobs.db')
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM jobs
    ''')


    conn.commit()
    
    for page in range(last_page):
        result = requests.get(f"{url}&page={page}", headers = headers)
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "vacancy-card--z_UXteNo7bRGzxWVcL7y font-inter"})
        for result in results:

            conn = sqlite3.connect('/Users/malfurion/Desktop/Практика/Parser/jobs.db')
            cursor = conn.cursor()


            # Job
            job_name = result.find("a").text
            job_link = result.find("h2", {"data-qa": "bloko-header-2"}).find("a", {"class": "bloko-link"})["href"]
                # job_link_txt = f'<a href="{job_link}">Ссылка</a>'# на будущее



            # Зарплата
            if result.find("div", {"class": "compensation-labels--uUto71l5gcnhU2I8TZmz"}).find("span", {"class": "fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni compensation-text--kTJ0_rp54B2vNeZ3CTt2 separate-line-on-xs--mtby5gO4J0ixtqzW38wh"}) == None:

                salary = "Не указана"

            else:

                salary = result.find("div", {"class": "compensation-labels--uUto71l5gcnhU2I8TZmz"}).find("span", {"class": "fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni compensation-text--kTJ0_rp54B2vNeZ3CTt2 separate-line-on-xs--mtby5gO4J0ixtqzW38wh"}).text



            # Опыт работы
            if result.find("div", {"class": "compensation-labels--uUto71l5gcnhU2I8TZmz"}).find("span", {"class": "label--rWRLMsbliNlu_OMkM_D3 label_light-gray--naceJW1Byb6XTGCkZtUM"}) == None:

                experience = "Не указан"

            else:

                experience = result.find("div", {"class": "compensation-labels--uUto71l5gcnhU2I8TZmz"}).find("span", {"class": "label--rWRLMsbliNlu_OMkM_D3 label_light-gray--naceJW1Byb6XTGCkZtUM"}).text

            

            # Company
            if result.find("a", {"data-qa": "vacancy-serp__vacancy-employer"}) == None:

                company = "Не указана"

            else:

                company = result.find("a", {"data-qa": "vacancy-serp__vacancy-employer"}).find("span").text

            

            # City
            if result.find("div", {"class": "info-section--N695JG77kqwzxWAnSePt"}).find("span", {"class": "fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni"}) == None:

                city = "Не указан"

            else:

                city = result.find("div", {"class": "info-section--N695JG77kqwzxWAnSePt"}).find("span", {"class": "fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni"}).text
            
            cursor.execute('''
                INSERT INTO jobs (job_name, company, salary, experience, city, job_link)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (job_name, company, salary, experience, city, job_link))
            conn.commit()

            conn.close()

            # print(job_name, "|", salary, "|", experience, "|", company, "|", city) 
        
