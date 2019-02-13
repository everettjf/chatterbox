

# list all app name order by version count
# list all app name order by version frequency

import os
import sys
import json
from datetime import datetime, timedelta

def compute_days_per_version(appinfo):
    versions = appinfo['version_history']
    if len(versions) < 5:
        return 9999

    first = versions[-1]['release_date']
    last = versions[0]['release_date']

    count = len(versions)
    firsttime = datetime.strptime(first, '%Y年%m月%d日')
    lasttime = datetime.strptime(last, '%Y年%m月%d日')

    delta = lasttime - firsttime

    days_per_version = delta.days * 1.0 / count

    return days_per_version

def compute_days_per_version_last_3_month(appinfo):
    versions = appinfo['version_history']
    if len(versions) < 3:
        return 9999

    latest = versions[0]['release_date']
    latest_time = datetime.strptime(latest, '%Y年%m月%d日')
    three_month_ago = latest_time - timedelta(days=90)

    # find the first datetime

    for version in versions:
        cur = version['release_date']
        cur_time = datetime.strptime(cur, '%Y年%m月%d日')

        if 



    pass


def report_dir(path, option):

    applist = []

    files = os.listdir(path)
    for filename in files:
        filepath = os.path.join(path, filename)

        with open(filepath) as fp:
            appinfo = json.load(fp)

            days_per_version = compute_days_per_version(appinfo)

            applist.append({
                'id':appinfo['id'],
                'app_name':appinfo['app_name'],
                'version_count': len(appinfo['version_history']),
                'days_per_version': days_per_version,
            })
    
    print('*' * 80)

    if option == 'version-count':
        print('=== Order by version count ===')
        applist_orderby_count = sorted(applist, key = lambda app: app['version_count'], reverse=True)
        for app in applist_orderby_count:
            print(app)
    elif option == 'days-per-version':
        print('=== Order by days per version ===')
        applist_orderby_freq = sorted(applist, key = lambda app: app['days_per_version'])
        for app in applist_orderby_freq:
            print(app)
    elif option == 'days-per-version-last-3-month':
        pass
    elif option == 'emergency-release':
        pass
    else:
        print('unknown option')

    print('*' * 80)



def help():
    print('Usage: ')
    print('  python report.py version-count <appinfo-directory-path>')
    print('  python report.py days-per-version <appinfo-directory-path>')
    print('  python report.py days-per-version-last-3-month <appinfo-directory-path>')
    print('  python report.py emergency-release <appinfo-directory-path>')


def main():
    if len(sys.argv) != 3:
        help()
        return
    
    option = sys.argv[1]
    path = sys.argv[2]

    report_dir(path, option)


if __name__ == '__main__':
    main()