from bs4 import BeautifulSoup
from requests import get
import io
import math
import time

test_universities = ['Yale','Brown', 'Cornell', 'Harvard', 'Rutgers', 'Cambridge', 'Oxford']


# status codes: A: American; U: International, with US degree; I: International, without US degree; O: Other; ?: Unknown
title = ['Name','Major','Degree','Semester','Status','Notification','Date','GPA','GREV','GREQ','GREW',
         'Nationality','Post_Date','Comment']

base_url = "https://thegradcafe.com/survey/index.php"
per_page = 250

def generate_url(search_string, page_num=1):
    return base_url + "?q=" + '+'.join(search_string.split()) + "&t=a&o=&pp={}&p={}".format(per_page, page_num)

def get_data(search_string = None, filename=None):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/5'}
    response = get(generate_url(search_string), headers=headers)

    html_soup = BeautifulSoup(response.text, 'html.parser')

    num_results = html_soup.find('div', class_ = 'pagination')
    num_results = num_results.find('strong')
    num_results = int(num_results.string.split()[0])
    num_pages = math.ceil(num_results/per_page)
    print(num_pages)

    with io.open(filename, 'w+', encoding="utf-8") as file:
        file.write(','.join(title)+'\n')
        for i in range(1,num_pages+1):
            response = get(generate_url(search_string,i), headers=headers)
            html_soup = BeautifulSoup(response.text, 'html.parser')

            table = html_soup.find_all('table', class_='results narrow-table')
            table_rows = table[0].find_all('tr')[1:]
            # print(table_rows[0])
            # print(len(table_rows))

            for tr in table_rows:
                # datum = ','.join([value.text for value in tr.find_all('td')[:-1]])
                datum = ','.join(process_row(tr))
                file.write(datum + '\n')
            print(i)
            time.sleep(1)
    return response

def process_row(dat):
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/5'}
    # response = get(generate_url("njit"), headers=headers)
    #
    # html_soup = BeautifulSoup(response.text, 'html.parser')
    # table = html_soup.find_all('table', class_='results narrow-table')
    # table_rows = table[0].find_all('tr')[1:]
    #
    # dat = table_rows[0]
    # print(dat)
    # print("num cols: {}".format(len(dat)))
    # for i,td in enumerate(dat):
    #     print(td)

    gpa, greV, greQ, greW = 'n/a', 'n/a', 'n/a', 'n/a'

    # Column 1:
    name = dat.find_all('td')[0].text
    name = name.replace(',', ' ')
    name = name.split('(')[0]

    # Column 2:
    # print(dat.find_all('td')[1].text)
    vals = dat.find_all('td')[1].text.split(',')
    major, degree = vals[0],vals[1]
    degree, semester = vals[-1].split('(')
    semester = semester[0]

    # Column 3
    stats = dat.find_all('td')[2]
    tokens = stats.text.split()
    # status = stats.find('span').text
    status = tokens[0]
    notified = tokens[2]

    if (status == 'Wait'):
        status = tokens[0] + tokens[1]
        notified = tokens[3]

    index = stats.text.index(' on ')
    tokens = stats.text[index:].split()

    date = "-".join(tokens[1:4])
    # tokens = stats.text.split()
    # # status = stats.find('span').text
    # status = tokens[0]
    #
    # notified = tokens[2]
    # if (notified == 'Postal' or notified == 'Phone'):
    #     date = "-".join(tokens[5:8])
    # else:
    #     date = "-".join(tokens[4:7])

    # GRE and GPA
    ext_info = stats.find('a')
    if (ext_info != None):
        raw_gpa = ext_info.find('span').contents[1]
        for c in ": ":
            raw_gpa = raw_gpa.replace(c, "")
        gpa = raw_gpa

        raw_gre = stats.find('a').find('span').contents[4]
        for c in ": ":
            raw_gre = raw_gre.replace(c, "")
        greV, greQ, greW = raw_gre.split('/')

    # Column 4:
    nationality = dat.find_all('td')[3].text

    # Column 5:
    post_date = '-'.join(dat.find_all('td')[4].text.split())

    # Column 6:
    comment = dat.find_all('td')[5].text
    bad_chars = '\n,\r'
    for c in bad_chars:
        comment = comment.replace(c," ")

    return [name, major, degree, semester, status, notified, date, gpa, greV, greQ, greW, nationality, post_date,
            comment]

if __name__ == '__main__':

    # generate_url('Princeton University')
    # response = get_data('Stanford University', 'data/stanford.csv')
    # response = get_data('NJIT', 'data/njit.csv')
    # response = get_data('Georgia Institute Of Technology', 'data/gatech.csv')
    response = get_data('Georgia Institute Of Technology computer science', 'data/gatech_cs.csv')
    # for u in test_universities:
    #     get_data(u+' University', 'data/{}.csv'.format(u.lower()))

