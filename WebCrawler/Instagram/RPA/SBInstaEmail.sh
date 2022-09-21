#!/bin/bash

__conda_setup="$('/home/jeon2/anaconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"

if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/jeon2/anaconda3/etc/profile.d/conda.sh" ]; then
        . "/home/jeon2/anaconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/jeon2/anaconda3/bin:$PATH"
    fi
fi                    # conda 경로 잡기

echo $(date '+%Y-%m-%d %H:%M:%S')
echo "Skinny Brown의 Instagram을 매일 오후 8시에 크롤링해서 메일로 보냅니다."

conda activate study
/home/jeon2/anaconda3/envs/study/bin/python3 /mnt/FE0A5E240A5DDA6B/workspace/jeon2_package/WebCrawler/Instagram/SBInstaEmail.py