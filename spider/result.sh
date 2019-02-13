# !/bin/bash
rm -rf result
mkdir result

echo 'start'

python rank.py version-count data/20190213/appinfo > result/version-count.txt
python rank.py days-per-version data/20190213/appinfo > result/days-per-version.txt
python rank.py days-per-version-last-6-month data/20190213/appinfo > result/days-per-version-last-6-month.txt
python rank.py emergency-release-count data/20190213/appinfo > result/emergency-release-count.txt

echo 'complete :)'