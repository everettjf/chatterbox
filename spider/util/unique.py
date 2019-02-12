
import os
import sys
import json


def help():
    print('Usage: python unique.py <path-to-url-json>')

def unique_file(path):
    idset = set()
    with open(path) as fp:
        items = json.load(fp)
        for item in items:
            idset.add(item['id'])
    
    idarr = []
    for id in idset:
        idarr.append({
            'id':id
        })

    with open(path, 'w') as fp:
        json.dump(idarr, fp, indent=2)


def main():
    if len(sys.argv) != 2:
        help()
        return
    
    path = sys.argv[1]
    unique_file(path)


if __name__ == '__main__':
    main()