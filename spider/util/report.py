

# list all app name order by version count
# list all app name order by version frequency

import os
import sys
import json
from datetime import datetime


def report_dir(path):

    applist = []

    files = os.listdir(path)
    for filename in files:
        filepath = os.path.join(path, filename)

        with open(filepath) as fp:
            appinfo = json.load(fp)

            days_per_version, days = compute_version_frequency(appinfo)

            applist.append({
                'id':appinfo['id'],
                'app_name':appinfo['app_name'],
                'version_count': len(appinfo['version_history']),
                'days_per_version': days_per_version,
            })
    
    # print('*' * 80)
    # print('=== Order by version count ===')
    # applist_orderby_count = sorted(applist, key = lambda app: app['version_count'], reverse=True)
    # for app in applist_orderby_count:
    #     print(app)

    # print('')
    # print('')

    print('*' * 80)
    print('=== Order by days per version ===')
    applist_orderby_freq = sorted(applist, key = lambda app: app['days_per_version'])
    for app in applist_orderby_freq:
        print(app)


def compute_version_frequency(appinfo):
    versions = appinfo['version_history']
    if len(versions) < 5:
        return 9999,9999

    first = versions[-1]['release_date']
    last = versions[0]['release_date']

    count = len(versions)
    firsttime = datetime.strptime(first, '%Y年%m月%d日')
    lasttime = datetime.strptime(last, '%Y年%m月%d日')

    delta = lasttime - firsttime

    days_per_version = delta.days * 1.0 / count

    return days_per_version, delta.days


def help():
    print('Usage: ')
    print('  python report.py <path-to-appinfo-directory>')


def main():
    if len(sys.argv) != 2:
        help()
        return
    
    path = sys.argv[1]

    report_dir(path)


if __name__ == '__main__':
    main()