import dateparser
from bs4 import BeautifulSoup


class ProfileParser():

    def __init__(self, file_name, relative_base):
        self.file_name = file_name
        self.relative_base = relative_base

        self.user_id = None
        self.user_name = None
        self.user_title = None
        self.user_posts = None
        self.user_last_post = None
        self.user_registered = None

    def parse(self):

        print('Processing {}...'.format(self.file_name))

        # populate user id
        self.user_id = int(self.file_name.split('=')[-1])

        try:

            # read the file
            with open(self.file_name) as fp:

                # parse it
                html_contents = fp.read()
                soup = BeautifulSoup(html_contents, 'html.parser')

                fieldsets = soup.find_all('div', {'class': 'infldset'})

                # populate user name
                user_name = fieldsets[0].select("dd:nth-of-type(1)")
                if user_name:
                    self.user_name = user_name[0].getText().strip().encode('ascii', 'ignore')

                # populate user title
                user_title = fieldsets[0].select("dd:nth-of-type(2)")
                if user_title:
                    self.user_title = user_title[0].getText().strip()

                # populate user posts
                user_posts = fieldsets[-1].find_all("dd")[0]
                if user_posts:
                    self.user_posts = int(user_posts.getText().strip().split(' ')[0].replace(',', ''))

                # populate user registered
                user_registered = fieldsets[-1].find_all("dd")[-1]
                if user_registered:
                    self.user_registered = self._parse_date(user_registered.getText().strip())

                # populate user last post
                if self.user_posts > 0:
                    user_last_post = fieldsets[-1].find_all("dd")[1]
                    if user_last_post:
                        self.user_last_post = self._parse_date(user_last_post.getText().strip())

            print('{:<20}{}'.format('user_id', self.user_id))
            print('{:<20}{}'.format('user_name', self.user_name))
            print('{:<20}{}'.format('user_title', self.user_title))
            print('{:<20}{}'.format('user_posts', self.user_posts))
            print('{:<20}{}'.format('user_last_post', self.user_last_post))
            print('{:<20}{}'.format('user_registered', self.user_registered))

        except Exception as e:
            print('Error occurred while parsing file {}: {}'.format(self.file_name, str(e)))

    def _parse_date(self, date_str):
        return str(dateparser.parse(date_str, settings={'RELATIVE_BASE': self.relative_base}))