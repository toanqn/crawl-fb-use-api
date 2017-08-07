import facebook
import csv
import requests
import requests_cache


def read_input(file_name):
    with open(file_name) as f:
        content = f.readlines()

    content = [x.strip() for x in content]
    return content

def write_csv(file_name, data, fieldnames):
    # Write CSV
    with open(file_name, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

        writer.writeheader()
        writer.writerows(data)

def crawl_fb_page(list_university):
    token = input('Input your token:')
    graph = facebook.GraphAPI(access_token=token, version='2.9')

    for u in list_university:
        res = graph.search(type='page', q=u, fields='name,link,fan_count,rating_count,bio,category,phone')
        data = res['data']

        file_name = 'page/' + u + '.csv'
        fieldnames = ['name', 'link', 'fan_count', 'rating_count', 'bio', 'category', 'phone', 'id']
        write_csv(file_name, data, fieldnames)

def crawl_fb_group(list_university):
    token = input('Input your token:')
    graph = facebook.GraphAPI(access_token=token, version='2.9')

    for u in list_university:
        res = graph.search(type='group', q=u, fields='name,privacy,updated_time')
        data = res['data']

        # get data on next_paging
        try:
            next_page = res['paging']['next']
            r = requests.get(next_page)
            next_data = r.json()['data']
            if (next_data):
                data += next_data
        except Exception as e:
            pass

        # add group link into data
        for d in data:
            d['link'] = 'https://www.facebook.com/groups/' + d['id']

        file_name = 'group/' + u + '.csv'
        fieldnames = ['name', 'link', 'privacy', 'updated_time', 'id']
        write_csv(file_name, data, fieldnames)

if __name__ == '__main__':
    list_university = read_input('university-in-hanoi.txt')

    choise = input('(1) Crawl page: \n(2) Crawl group:\nEnter your choise (1 or 2):')
    if (choise == 1):
        crawl_fb_page(list_university)
    else:
        crawl_fb_group(list_university)

