# postgresql sample db에서 actor table을 이용하여 CRUD를 만들기

# 1. actor table의 모든 데이터를 조회하기
# 2. actor table에 데이터를 추가하기
# 3. actor table의 데이터를 수정하기
# 4. actor table의 데이터를 삭제하기
# class를 만들기

import psycopg2

class ActorCRUD:
    def __init__ (self, dbname, user, password, host, port):
        self.conn_params = {
            "dbname": dbname,
            "user": user,
            "password": password,
            "host": host,
            "port": port
        }
        self.conn = None
        self.connect()

    def connect(self):
        # DB 연결
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            print("데이터베이스에 성공적으로 연결되었습니다.")
        except psycopg2.Error as e:
            print(f"데이터베이스 연결 중 오류가 발생했습니다: {e}")

    # CRUD 제작
    def create_actor(self, first_name, last_name):
        # actor 테이블에 data 추가
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO actor (first_name, last_name)
                VALUES (%s, %s) RETURNING actor_id;
            """, (first_name, last_name))
            actor_id = cur.fetchone()[0]
            self.conn.commit()
            print(f"배우 '{first_name} {last_name}'이(가) actor {actor_id}로 추가되었습니다.")
            return actor_id
        
    def read_actor(self, actor_id):
        # actor 테이블 data 읽기
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM actor WHERE actor_id = %s;", (actor_id,))

            actor = cur.fetchone()

            if actor:
                print(actor)
                return actor
            else:
                print("배우를 찾을 수 없습니다.")
                return None


    def read_actor_all(self):
        # actor 테이블 data 전체 읽기
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM actor;")
            actors = cur.fetchall()
            for actor in actors:
                print(actor)

    def update_actor(self, first_name, last_name, actor_id):
        # actor 테이블 data 갱신하기
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE actor
                SET first_name = %s, last_name = %s
                WHERE actor_id = %s;
            """, (first_name, last_name, actor_id))
            self.conn.commit()
            print(f"배우 {actor_id}의 정보가 업데이트되었습니다.")
    
    def delete_actor(self, actor_id):
        # actor 테이블 data 삭제하기
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM actor WHERE actor_id = %s;", (actor_id,))
            self.conn.commit()
            print(f"actor {actor_id}의 정보가 삭제되었습니다.")

    def close(self):
        self.conn.close()
            
print("데이터베이스 연결에 필요한 사전 정보를 입력해주세요.")
DBNAME = input("DBNAME : ")
USER = input("USER : ")
PASSWORD = input("PASSWORD : ")
HOST = input("HOST : ")
PORT = input("PORT : ")
actor_crud = ActorCRUD(DBNAME, USER, PASSWORD, HOST, PORT)
while True:
    select = input("""원하는 기능을 선택하세요.
                   1. 데이터 추가(Create)
                   2. 데이터 읽기(Read)
                   3. 데이터 갱신(Update)
                   4. 데이터 삭제(Delete)
                   5. 프로그램 종료
                   >>> """)
    if select == "1":
        input_name = input("추가할 데이터의 First name과 Last name을 적어주세요. 구분은 띄어쓰기로 이루어집니다.\n>>> ")
        name_list = input_name.split(" ")
        first_name = name_list[0]
        last_name = name_list[1]
        actor_id = actor_crud.create_actor(first_name=first_name, last_name=last_name)

    elif select == "2":
        read_select = input("""원하는 읽기 기능을 선택하세요.
                                1) 전체 읽기(read all)
                                2) actor_id를 통해 특정 레코드만 읽기(read one)
                            >>> """)
        if read_select == "1":
            actor_crud.read_actor_all()
        if read_select == "2":
            read_actor_id = input("읽으려는 데이터의 actor_id를 입력해주세요 : ")
            actor_crud.read_actor(actor_id)

    elif select == "3":
        update_data = input("갱신하려는 데이터의 actor_id를 입력해주세요 : ")
        update_name_data = input("갱신할 데이터의 First name과 Last name을 적어주세요. 구분은 띄어쓰기로 이루어집니다.\n>>> ")
        update_name_list = update_name_data.split(" ")
        update_first_name = update_name_list[0]
        update_last_name = update_name_list[1]
        actor_crud.update_actor(update_first_name, update_last_name, actor_id = update_data)

    elif select == "4":
        delete_data = input("삭제하려는 데이터의 actor_id를 입력해주세요 : ")
        actor_crud.delete_actor(delete_data)

    elif select == "5":
        print("프로그램을 종료합니다.")
        break

actor_crud.close()