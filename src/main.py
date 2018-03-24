import json, csv, argparse, datetime
import dateparser
from os import path, listdir
from profile_parser import ProfileParser


def dump_json(data, out):
    """
    Write output to JSON file
    """
    with open(out, 'w') as fp:
        json.dump(data, fp, indent=2)


def dump_csv(data, out):
    with open(out, 'w') as fp:
        fieldnames = ['id', 'username', 'title', 'posts', 'lastpost', 'registered']
        writer = csv.DictWriter(fp, fieldnames=fieldnames)
        writer.writeheader()
        for entry in data:
            writer.writerow(entry)


def process_dir(data_dir, timebase=None):

    profiles = []
    forums = []
    topics = []

    if timebase is not None:
        relative_base = dateparser.parse(timebase)
    else:
        relative_base = datetime.datetime.now()

    for f in listdir(data_dir):

        # if the object name matches a pattern, parse it
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

        if f.startswith('viewforum.php?id='):
            # TODO: parse forum
            pass

        if f.startswith('viewtopic.php?id='):
            # TODO: parse topic
            pass

    dump_json(profiles, 'out/profiles-{}.json'.format(str(relative_base.date())))
    dump_csv(profiles, 'out/profiles-{}.csv'.format(str(relative_base.date())))


def main():
    parser = argparse.ArgumentParser(description='EVO Parser.')
    parser.add_argument('datadir', type=str, help='data directory')
    parser.add_argument('timebase', type=str, help='relative time base')
    args = parser.parse_args()
    process_dir(path.join(path.abspath('.'), args.datadir), args.timebase)


if __name__ == '__main__':
    main()
