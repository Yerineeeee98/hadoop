import sys

last_hour = None
total_count = 0

# 03 1 3시에 요청한 사람 1명
# 03 1
# 04 1

for line in sys.stdin:
    line = line.strip()
    
    hour, value = line.split()
    value = int(value)
    
    if last_hour == hour:
        total_count += value 
    else: # 3시에서 4시로 바뀌는 분기점
        if last_hour is not None:
            print(f'{last_hour}\t{total_count}')
            
        last_hour = hour
        total_count = value
        
print(f'{last_hour}\t{total_count}')