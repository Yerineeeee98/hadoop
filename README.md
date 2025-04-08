# hadoop command

- `ls`
    - `hdfs dfs -ls /`
    -  : hdfs dfs -ls <확인하고 싶은 경로> 위에 `/`는 루트 표시 

- `mkdir`
    - `hdfs dfs -mkdir /input`
    - : hdfs dfs -mkdir <생성하고 싶은 폴더 이름>

- `put`
    - `hdfs dfs -put <업로드할 파일 경로> <업로드할 위치>`
    - : hdfs dfs -put ml-25m/movies.csv /input

- `cat`
    - `hdfs dfs -cat <출력하고싶은 파일 경로 >`
    - hdfs dfs -cat /input/movies.csv 
    - 내가 출력하고 싶은 전체 코드 

- `head`, `tail`
    - `hdfs dfs -head <출력하고 싶은 파일 경로>`
    - hdfs dfs -head /input/movies.csv
    - head (앞에 내용), tail (뒤에 내용)

- `rm`
    - `hdfs dfs -rm <지울 파일 경로>`
    - hdfs dfs -rm /ratings.csv
    - 폴더를 삭제할 경우 -r 옵션 추가
    - `hdfs dfs -rm -r /input`


---

# 2025.04.08 
- windows/system32/drivers/etc/hosts(맨위에 파일)
    - ![alt text](img/image.png) 여기서 yerin. 가져오기 
    - 127.0.0.1 yerin. vscode로 실행해서 저장하기
    - ![alt text](img/image-1.png) 
    - 그럼 이렇게 데이터를 볼 수 있음   
- 하둡은 데이터를 수정 할 수 없음 (추가는 가능)

## 🔹MapReduce의 Map과 Reduce 개념 정리
- Map 단계

    - 데이터를 꺼내서 가공하는 역할

    - 입력 데이터를 키-값(key-value) 쌍으로 변환함

    - 데이터를 분할하고 필터링하는 단계로, 병렬로 실행됨

    - 예시:

        - 텍스트에서 단어를 꺼내고 (단어, 1) 형태로 변환

- Reduce 단계

    - Map에서 나온 키-값 쌍을 같은 키끼리 모아서 처리함

    - 합산, 평균, 집계, 정렬 등의 로직을 수행

    - 예시:

        - (단어, [1, 1, 1, 1]) → 단어의 총 개수: 4


- ![alt text](img/image-2.png)
    - `mapper.py`에서 
        - ```python
            # 데이터를 쪼개는 역할
            import sys

            for line in sys.stdin: # text.txt 파일을 전부다 sys.stdin으로 불러와서 한줄씩 line에 저장하기
                line = line.strip() # 좌우 공백 없애기
                words = line.split()
                # ['hi', 'good', 'sad']
    
                for word in words:
                 print(f'{word}\t1') #\t:한줄씩 내려쓰기 
            ```
    - `cat text.txt | python3 mapper.py`로 출력해보면 ![alt text](img/image-3.png)
    - `reducer.py`에서
        - ```python
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
            ```
- ![alt text](img/image-4.png)
- ![alt text](img/image-5.png)
- 여기서 터미널에 명령어 
    - `hadoop jar ~/hadoop-3.3.6/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar\
 -input /input/text.txt \
 -output /output/wordcount \
 -mapper 'python3 /home/ubuntu/damf2/hadoop/0.wordcount/mapper.py' \
 -reducer 'python3 /home/ubuntu/damf2/hadoop/0.wordcount/reducer.py'`를 실행하면 `http://localhost:9870/explorer.html#/output/wordcount`에서![alt text](image-6.png) 이러한 결과가 나옴

---
## hadoop version
- input : 데이터 어디서 가져올건지
- output : 데이터를 어디다가 저장할지
- mapper
- reducer
- 명령어 실행행
- `hadoop jar ~/hadoop-3.3.6/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar\
 -input /input/text.txt \
 -output /output/wordcount \
 -mapper 'python3 /home/ubuntu/damf2/hadoop/0.wordcount/mapper.py' \
 -reducer 'python3 /home/ubuntu/damf2/hadoop/0.wordcount/reducer.py'`

 - chmod +x or chmod 755 rwx|rwx|rwx

---
# 1. 영화의 평점 평균 
- hdfs dfs -put ml-25m/input

- `/hadoop/1.movie-rate/avg/mapper.py`
    - ```python 
        import sys

        for line in sys.stdin:
            line = line.strip()
            
            fields = line.split(',') # ,를 기준으로 쪼개기
            # ['1', '296', '5.0', '11133451414']
            
            movie_id = fields[1]
            rating = fields[2]
            
            
            print(f'{movie_id}\t{rating}')
        ```
- `/hadoop/1.movie-rate/avg/reducer.py`
    - ```python
        import sys


        currunt_movie_id = None
        currunt_sum = 0
        currunt_count = 0

        for line in sys.stdin:   
            line = line.strip() # 공백제거
            movie_id, rating = line.split() # movie_id, rating 분리
            
            try:
                rating = float(rating)
            except: # 평점이 숫자가 아닌 경우는 건너뜀
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
        print(f'{currunt_movie_id}\t{currunt_avg}') # 마지막 영화의 결과도 출력해야 하므로 추가로 한 번 더 처리함
        ```
- 터미널에 명령어 실행
    - `hadoop jar ~/hadoop-3.3.6/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar\
 -input /input/ratings.csv \
 -output /output/movie-rate-avg \
 -mapper 'python3 /home/ubuntu/damf2/hadoop/1.movie-rate-avg/mapper.py' \
 -reducer 'python3 /home/ubuntu/damf2/hadoop/1.movie-rate-avg/reducer.py'`
- http://localhost:9870/explorer.html#/output 에서 ![alt text](image-7.png) 이러한 결과가 나옴 
