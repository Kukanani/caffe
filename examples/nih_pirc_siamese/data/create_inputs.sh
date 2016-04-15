ls -1 dr | tail -n 1000 | sed 's|^|data/dr/|' > dr2.txt;
ls -1 dr | head -n 1000 | sed 's|^|data/dr/|' > dr1.txt;
ls -1 dc | sed 's|^|data/dc/|' > dc.txt
