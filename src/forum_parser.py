import dateparser
from collections import namedtuple
from bs4 import BeautifulSoup

Topic = namedtuple('Topic', [
    'forumname',
    'name',
    'author',
    'replies',
    'views',
    'lastpost',
    'lastuser'
])


class ForumParser():

    def __init__(self, file_name, relative_base):
        self.file_name = file_name
        self.relative_base = relative_base

        self.topics = []

    def parse(self):

        print('Processing {}...'.format(self.file_name))

        try:

            # read the file
            with open(self.file_name) as fp:

                # parse it
                html_contents = fp.read()
                soup = BeautifulSoup(html_contents, 'html.parser')

                # get topic name
                forum_name = soup.find('div', {'class': 'crumbsplus'}).find('strong').find('a').getText().strip()

                # populate topics
                for topic in self._get_topics(soup):
                    name, author, replies, views, lastpost, lastuser = topic
                    self.topics.append(Topic(
                        forumname=forum_name,
                        name=name,
                        author=author,
                        replies=replies,
                        views=views,
                        lastpost=lastpost,
                        lastuser=lastuser
                    ))

        except Exception as e:
            print('Error occurred while parsing file {}: {}'.format(self.file_name, str(e)))

    def _parse_date(self, date_str):
        return str(dateparser.parse(date_str, settings={'RELATIVE_BASE': self.relative_base}))

    def _get_topics(self, soup):
        result = []

        rows = soup.find_all('tr', {'class': 'rowodd'}) + soup.find_all('tr', {'class': 'roweven'})
        for row in rows:

            try:
                cells = row.find_all('td')

                author = cells[0].find('span', {'class': 'byuser'}).find('a').getText().strip()\
                    .encode('ascii', 'ignore')
                name = cells[0].find('div', {'class': 'tclcon'}).find('a').getText().strip().encode('ascii', 'ignore')
                replies = int(cells[1].getText().strip().replace(',', ''))
                views = int(cells[2].getText().strip().replace(',', ''))
                lastpost = self._parse_date(cells[3].find('a').getText().strip())
                lastuser = cells[3].find('span', {'class': 'byuser'}).find('a').getText().strip()\
                    .encode('ascii', 'ignore')

                result.append((name, author, replies, views, lastpost, lastuser))

            except Exception as e:
                print('Error in topic {}'.format(str(e)))

        return result