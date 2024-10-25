import sqlite3

def createTable():    
    #데이터 베이스 연결 (파일로 저장)
    conn = sqlite3.connect('example.db')
    # 파일이름이 없으면 새로 생성

    #커서 생성
    cursor = conn.cursor()
    # SQL 쿼리를 실행할 커서

    #table 생성
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS
                users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                age INTEGER,
                email TEXT)
                ''')
    # users라는 테이블 생성
    # id, username, age, email 컬럼이 존재
    # id는 기본 키로 설정, 자동 증가
    # IF NOT EXISTS는 해당 테이블이 이미 존재할 경우 생성하지 않는다는 의미
    '''
    타입 INTEGER, REAL, TEXT, BLOB, NUMERIC
    키 PRIMARY KEY 유일키, INTEGER PRIMARY KEY AUTOINCREMENT 자동증가
    NOT NULL 값이 반드시 있어야하며 NULL이면 안됨
    UNIQUE 컬럼에 중복값 없도록
    DEFAULT 값이 입력되지 않았을때 기본값 DEFAULT 0
    CHECK 조건을 설정해서 입력 제한, CHECK (age>=18) 18 이상만 입력가능
    
    '''

    #변경사항 저장
    conn.commit()
    # 작업한 내용을 SQLite3에 커밋하는 동작, 그전까지는 임시 저장임

def insertdata():
    #데이터 베이스 연결 (파일로 저장)
    conn = sqlite3.connect('example.db')

    #커서 생성
    cursor = conn.cursor()
    #데이터 삽입
    cursor.execute('''INSERT INTO users (username,age,email)
                   VALUES(?,?,?)''',('john_doe',30,'john@example.com'))
    # users 테이블에 삽입한다
    # ?를 통해 자리 표시를 하고
    # 두번째 인자에 튜블로 값을 넣는다.
    # key는 자동 증가되는 값으로 그외 컬럼들일 표기함

    #데이터 저장
    conn.commit()


def serachdata():
    #데이터 베이스 연결 (파일로 저장)
    conn = sqlite3.connect('example.db')

    #커서 생성
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users')
    # users 테이블의 모든 데이터 조회
    '''
    검색 조건1. 특정 사용자 이름
        SELECT * FROM users WHERE username = ? , ('john_doe',)
        조건2. 나이가 30 이상
        SELECT * FROM users WHERE age >= ?, (30,)
        조건3 이메일에 특정 문자열이 포함
        SELECT * FROM users WHERE email LIKE ?, ('%example.com%',) %는 0개이상의 문자
        조건4. 복수 조건
        SELECT * FROM users WHERE age > ? AND username = ?, (25,'john_doe')
        조건5. 정렬 결과
        SELECT * FROM users ORDER BY age DESC  나이로 내림차순
        조건6. 최대 n개 결과
        SELECT * FROM users ORDER BY age DESC LIMIT 5  나이 내림차순으로 5개
        조건7. 특정 범위 안
        SELECT * FROM users WHERE age BETWEEN ? AND ?,(25,35)
        조건8. 비어있지 않은
        SELECT * FROM users WHERE eamil IS NOT NULL
        조건9. 여러 값중 하나
        SELECT * FROM users WHERE username IN (?,?,?) , ('jon','alice','hane')
        조건10. 그룹별 집계
        SELECT age, COUNT(*) as count FROM users GROUP BY age <- age별 사용자 수
        조건11. 서브 쿼리
        SELECT * FROMW users WHERE age = (SELECT MAX(age) FROM users) <-나이가 가장 큰 사용자
        조건12. 중복제거
        SELECT DISTINCT age FROM users <- age값이 고유한 사용자들의 나이 목록
        조건13. 최대/최소/평균
        SELECT MIN(age) FROM users
        SELECT MAX(age) FROM users
        SELECT AVG(age) FROM users
        SELECT SUM(age) FROM users
        조건14. 조건과 함께 집계
        SELECT age, COUNT(*) as count FROM users GROUP BY age HAVING count > 1 <- 나이가 같은 사용자가 1명 이상일때, having은 group by의 결과에 조건을 추가할때

        
    '''
    rows = cursor.fetchall()
    # 조회된 모든 결과를 가져온다. 튜플 리스트로 반환

    for row in rows:
        print(row)

def updatedata():
    #데이터 베이스 연결 (파일로 저장)
    conn = sqlite3.connect('example.db')

    #커서 생성
    cursor = conn.cursor()

    cursor.execute('''UPDATE users
                   SET age = ?
                   WHERE username = ?''',(31,'john_doe'))
    # 이름을 조건으로 대상을 찾고 age 값을 변경한다는 의미
    conn.commit()

def deletedata():
    #데이터 베이스 연결 (파일로 저장)
    conn = sqlite3.connect('example.db')

    #커서 생성
    cursor = conn.cursor()

    cursor.execute('''DELETE FROM users
                   WHERE username = ?''',('john_doe',))
    # 이름으로 검색해서 지운다는 의미
    conn.commit()
