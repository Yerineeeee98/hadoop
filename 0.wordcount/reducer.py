# !/usr/bin/env python3

import sys

# hi      1
# good    1
# sad     1
# home    1
# ...
# 위에 데이터들이 sys.stdin에 들어감

last_word = None # 글자가 바뀌는 시점을 찾기 위해
total_count = 0


for line in sys.stdin:
    word, value = line.split() 
    value = int(value)
    
    if last_word == word:
        total_count += value

    else:
        if last_word is not None: # none이 아닐 때 (최초가 아닐때)
            print(f'{last_word}\t{total_count}')
        last_word = word
        total_count = value # 새로운 단어가 들어왔으니깐 1부터 다시 시작
        
if last_word == word:
    print(f'{last_word}\t{total_count}')