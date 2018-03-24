import dateparser
from collections import namedtuple
from bs4 import BeautifulSoup

Post = namedtuple('Post', [
    'forumname',
    'topicname',
    'topicid',
    'date',
    'author',
    'authorid',
    'authortitle',
    'authorregistered',
    'authorposts',
    'message'
])


class TopicParser():

    def __init__(self, file_name, relative_base):
        self.file_name = file_name
        self.relative_base = relative_base

        self.posts = []

    def parse(self):

        print('Processing {}...'.format(self.file_name))

        try:

            # read the file
            with open(self.file_name) as fp:

                # parse it
                html_contents = fp.read()
                soup = BeautifulSoup(html_contents, 'html.parser')

                # get forum name and topic name
                breadcrumbs = soup.find('ul', {'class': 'crumbs'}).find_all('a')
                topic_name = breadcrumbs[-1].getText().strip().encode('ascii', 'ignore')
                forum_name = breadcrumbs[-2].getText().strip().encode('ascii', 'ignore')
                topic_id = int(breadcrumbs[-1].get('href').split('=')[-1])

                # populate posts
                for post in self._get_posts(soup):
                    author, author_id, author_title, author_registered, author_posts, date, message = post
                    self.posts.append(Post(
                        forumname=forum_name,
                        topicname=topic_name,
                        topicid=topic_id,
                        author=author,
                        authorid=author_id,
                        authortitle=author_title,
                        authorregistered=author_registered,
                        authorposts=author_posts,
                        date=date,
                        message=message
                    ))

        except Exception as e:
            print('Error occurred while parsing file {}: {}'.format(self.file_name, str(e)))

    def _parse_date(self, date_str):
        return str(dateparser.parse(date_str, settings={'RELATIVE_BASE': self.relative_base}))

    def _get_posts(self, soup):
        result = []

        rows = soup.find_all('div', {'class': 'blockpost'})
        for row in rows:

            try:

                author = row.find('div', {'class': 'postleft'}).find('a').getText().strip().encode('ascii', 'ignore')
                author_id = int(row.find('div', {'class': 'postleft'}).find('a').get('href').split('=')[-1])
                author_title = row.find('dd', {'class': 'usertitle'}).getText().strip()
                # author_infos = row.find('div', {'class': 'postleft'}).find_all('dd')
                # author_registered = self._parse_date(
                #     author_infos[-3].find('span').getText().strip().replace('Registered: ', '')
                # )
                # author_posts = int(
                #     author_infos[-2].find('span').getText().strip().replace('Posts: ', '').replace(',', '')
                # )
                message = row.find('div', {'class': 'postmsg'}).getText().encode('ascii', 'ignore')
                date = self._parse_date(row.find('h2').find('a').getText().strip())

                result.append((author, author_id, author_title, None, None, date, message))

            except Exception as e:
                print('Error in post {}'.format(str(e)))

        return result