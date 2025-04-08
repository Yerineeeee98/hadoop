import sys
import re

time_pattern = re.compile(r':(\d{2}:\d{2}:\d{2})') # (r 뒤에 있는 문자는 정규표현식이라는 의미) :\d{2}어떤 숫자든 2자리 숫자이면 가능하다는 의미


for line in sys.stdin:
    line = line.strip()
    
    match = time_pattern.search(line)
    
    if match:
        hour = match.group(1) # (r':(\d{2}:\d{2}:\d{2})') 여기서 소괄호로 묶은것중 첫번쨰 0번째가 아닌 1번째인 이유는 0번째는 소괄호 그자체를 의미
        print(f'{hour}\t1')
        
    