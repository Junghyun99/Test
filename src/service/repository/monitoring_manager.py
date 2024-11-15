def main():
data_ids = [1, 2, 3, 4, 5] # 작업할 ID 목록
results = []

# 스레드 풀을 생성하고 스레드를 관리
with ThreadPoolExecutor(max_workers=3) as executor:
    # 각 ID에 대해 fetch_data 작업을 비동기로 제출
    futures = [executor.submit(fetch_data, data_id) for data_id in data_ids]

    # 작업 완료를 기다리며 결과 수집
    for future in as_completed(futures):
        result = future.result()  # 작업 결과 가져오기
        results.append(result)
        print(result)

print("All tasks completed.")