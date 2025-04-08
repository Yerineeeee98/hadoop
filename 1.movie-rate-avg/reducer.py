import sys


currunt_movie_id = None
currunt_sum = 0
currunt_count = 0

for line in sys.stdin:   
    line = line.strip()
    movie_id, rating = line.split()
    
    try:
        rating = float(rating)
    except:
        continue # for문을 무시하고 다음 for문으로 넘어가기 
    
    # 123, 5.0 
    # 123, 3.5
    # 123, 4.0
    # 234, 4.2  영화의 코드 숫자가 바뀔때까지 출력하기 
    
    if currunt_movie_id == movie_id:
        currunt_count += 1
        currunt_sum += rating
        
    else: # 영화가 바뀌었을 떄
        if currunt_movie_id is not None:
            currunt_avg = currunt_sum / currunt_count
            print(f'{currunt_movie_id}\t{currunt_avg}')
        
        currunt_movie_id = movie_id
        currunt_count = 1
        currunt_sum = rating
    
currunt_avg = currunt_sum / currunt_count
print(f'{currunt_movie_id}\t{currunt_avg}')