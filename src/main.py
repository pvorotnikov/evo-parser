import json, re
from datetime import date
from os import path, listdir
from bs4 import BeautifulSoup

def main():

    # define your search filter here
    date_filter_start = date(2015, 1, 1)
    date_filter_end = date(2015, 2, 1)
    folder_match = re.compile('^\d+-\d+-\d+$')

    # get absolute path of the cwd
    cwd = path.abspath('.')

    results = {}

    # list all objects here
    for d in listdir(cwd):

        # if the object is dir and is in yyyy-mm-dd format, list everything inside
        if path.isdir(d) and folder_match.search(d):

            folder_parts = d.split('-')
            folder_date = date(int(folder_parts[0]), int(folder_parts[1]), int(folder_parts[2]))
            if folder_date < date_filter_start or folder_date > date_filter_end:
                continue

            # add new container for the d
            results[d] = {}

            for f in listdir(d):

                # if the object name matches a pattern, parse it
                if f.startswith('index.php?topic='):
                    topic = f.split('=')[1]
                    (topic_number, comment_number) = topic.split('.')


                    # create new topic
                    if None == results[d].get(topic_number):
                        results[d][topic_number] = {'title': 'Unknown title', 'posts': []}


                    # read the file (the file is auto closed after the block exits)
                    with open(path.join(cwd, d, f)) as fp:

                        # put everything in try / except not to stop the execution
                        # should any error occurs
                        try :

                            html_contents = fp.read()

                            # parse it
                            soup = BeautifulSoup(html_contents, 'html.parser')

                            # get the title if present
                            title = soup.h1
                            if None != title:
                                # encode the title in ascii because of reasons (stupid internet culture)
                                results[d][topic_number]['title'] = title.get_text().strip().encode('ascii', 'ignore')

                            # get the posts
                            posts = soup.findAll('div', { 'class' : 'post' })
                            for p in posts:
                                results[d][topic_number]['posts'].append(p.get_text().strip())

                            print('Parsed @ comment {} of topic {} ({}) from {}'.format(comment_number, topic_number, results[d][topic_number]['title'], d))

                        except Exception as e:
                            print('Error occurred: {}'.format(e.message))

            # uncomment this break for development
            # break

    # now that we have all the info, dump it
    with open('result.json', 'w') as fp:
        json.dump(results, fp, indent=2)



if __name__ == '__main__':
    main()