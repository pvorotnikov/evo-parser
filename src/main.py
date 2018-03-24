import json, csv, argparse, datetime
import dateparser
from os import path, listdir
from profile_parser import ProfileParser
from forum_parser import ForumParser
from topic_parser import TopicParser


def dump_json(data, out):
    """
    Write output to JSON file
    :param data:
    :param out:
    :return:
    """
    with open(out, 'w') as fp:
        json.dump(data, fp, indent=2)


def dump_csv(fieldnames, data, out):
    """
    Write output to CSV file
    :param fieldnames:
    :param data:
    :param out:
    :return:
    """
    with open(out, 'w') as fp:
        writer = csv.DictWriter(fp, fieldnames=fieldnames)
        writer.writeheader()
        for entry in data:
            writer.writerow(entry)


def process_topic(data_dir, relative_base=None):
    """
    Process topics
    :param data_dir:
    :param relative_base:
    :return:
    """
    topics = []

    count = 0

    for f in listdir(data_dir):

        if f.startswith('viewtopic.php?id='):
            topic = TopicParser(path.join(data_dir, f), relative_base)
            topic.parse()
            for item in topic.posts:
                topics.append({
                    'forumname': item.forumname,
                    'topicname': item.topicname,
                    'topicid': item.topicid,
                    'date': item.date,
                    'author': item.author,
                    'authorid': item.authorid,
                    'authortitle': item.authortitle,
                    'message': item.message
                })

            count += 1
            # if count == 100:
            #     break

    dump_json(topics, 'out/topics-{}.json'.format(str(relative_base.date())))
    dump_csv(['forumname', 'topicname', 'topicid', 'date', 'author', 'authorid', 'authortitle', 'message'],
             topics,
             'out/topics-{}.csv'.format(str(relative_base.date())))


def process_forum(data_dir, relative_base=None):
    """
    Process forums
    :param data_dir:
    :param relative_base:
    :return:
    """
    forums = []

    for f in listdir(data_dir):

        if f.startswith('viewforum.php?id='):
            forum = ForumParser(path.join(data_dir, f), relative_base)
            forum.parse()
            for item in forum.topics:
                forums.append({
                    'forumname': item.forumname,
                    'topicid': item.id,
                    'topicname': item.name,
                    'topicauthor': item.author,
                    'topicreplies': item.replies,
                    'topicviews': item.views,
                    'topiclastpost': item.lastpost,
                    'topiclastuser': item.lastuser
                })

    dump_json(forums, 'out/forums-{}.json'.format(str(relative_base.date())))
    dump_csv(['topicid', 'forumname', 'topicname', 'topicauthor', 'topicreplies', 'topicviews', 'topiclastpost',
              'topiclastuser'],
             forums,
             'out/forums-{}.csv'.format(str(relative_base.date())))


def process_profile(data_dir, relative_base=None):
    """
    Process profiles
    :param data_dir:
    :param relative_base:
    :return:
    """
    profiles = []

    for f in listdir(data_dir):

        if f.startswith('profile.php?id='):
            profile = ProfileParser(path.join(data_dir, f), relative_base)
            profile.parse()
            profiles.append({
                'id': profile.user_id,
                'username': profile.user_name,
                'title': profile.user_title,
                'posts': profile.user_posts,
                'lastpost': profile.user_last_post,
                'registered': profile.user_registered
            })

    dump_json(profiles, 'out/profiles-{}.json'.format(str(relative_base.date())))
    dump_csv(['id', 'username', 'title', 'posts', 'lastpost', 'registered'],
             profiles,
             'out/profiles-{}.csv'.format(str(relative_base.date())))


def main():
    """
    Main entry point
    :return:
    """
    parser = argparse.ArgumentParser(description='EVO Parser.')
    parser.add_argument('datadir', type=str, help='data directory')
    parser.add_argument('timebase', type=str, help='relative time base')
    parser.add_argument('object', type=str, help='what to parse')
    args = parser.parse_args()

    timebase = dateparser.parse(args.timebase)
    if args.object == 'profile':
        process_profile(path.join(path.abspath('.'), args.datadir), timebase)

    elif args.object == 'forum':
        process_forum(path.join(path.abspath('.'), args.datadir), timebase)

    elif args.object == 'topic':
        process_topic(path.join(path.abspath('.'), args.datadir), timebase)


if __name__ == '__main__':
    main()
