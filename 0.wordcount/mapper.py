# 데이터를 쪼개는 역할
# !/usr/bin/env python3
import sys

for line in sys.stdin: # text.txt 파일을 전부다 sys.stdin으로 불러와서 한줄씩 line에 저장하기
    line = line.strip() # 좌우 공백 없애기
    words = line.split()
    # ['hi', 'good', 'sad']
    
    for word in words:
        print(f'{word}\t1') #\t:한줄씩 내려쓰기 
    