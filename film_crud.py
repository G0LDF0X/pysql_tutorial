# 제목, 장르, 배우 등의 조건으로 영화를 검색하기 위해서는 category, actor 등의 테이블과 join이 필요하다.

import psycopg2

def print_data(print_type, data):
    if print_type == "Print in Paragraph":
        print("""
film_id : {},
title : {}
description : {},
release_year : {},
rental_duration : {},
rental_rate : {},
length : {},
replacement_cost : {},
rating : {},
category_id : {},
categordy_name : {},
language_id : {},
language_name : {}""".format(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12]))
    elif print_type == "Print in Line":
        print(data)

class filmCRUD:
    def __init__ (self, dbname, user, password, host, port):
        self.conn_params = {
            "dbname": dbname,
            "user": user,
            "password": password,
            "host": host,
            "port": port
        }
        self.print_type = "Print in Line"
        self.conn = None
        self.connect()

    def connect(self):
        # DB 연결
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            print("데이터베이스에 성공적으로 연결되었습니다.")
        except psycopg2.Error as e:
            print(f"데이터베이스 연결 중 오류가 발생했습니다: {e}")

    # 영화 제목으로 검색
    def read_film_title(self, title):
        with self.conn.cursor() as cur:
            cur.execute("""SELECT f.film_id, f.title, f.description, f.release_year, f.rental_duration, f.rental_rate, f.length, f.replacement_cost, f.rating, c.category_id, c.name, l.language_id, l.name
                        FROM film f
                        JOIN film_category fc USING (film_id)
                        JOIN category c USING (category_id)
                        JOIN language l USING (language_id)
                        WHERE f.title LIKE %s;""", ("%" + title + "%",))

            titles = cur.fetchall()

            print("\n==========검색 결과===========")

            if not titles:
                print("해당 제목으로 영화를 찾을 수 없습니다.")
                return False
            
            for title in titles:
                print_data(self.print_type, title)
            return True
    
    # 영화 장르로 검색
    def read_film_category(self):
        with self.conn.cursor() as cur:
            print("========== 영화 장르 ==========")
            cur.execute("SELECT * FROM category;")
            categories = cur.fetchall()
            for category in categories:
                print(category[0], category[1])

            search_id = input("검색하려는 영화 장르를 숫자로 입력해주세요 : ")
            cur.execute("""SELECT f.film_id, f.title, f.description, f.release_year, f.rental_duration, f.rental_rate, f.length, f.replacement_cost, f.rating, c.category_id, c.name, l.language_id, l.name
                        FROM film f
                        JOIN film_category fc USING (film_id)
                        JOIN category c USING (category_id)
                        JOIN language l USING (language_id)
                        WHERE fc.category_id = %s;""", (search_id,))

            category_result = cur.fetchall()
            print("\n==========검색 결과===========")

            if not category_result:
                print("해당 장르의 영화를 찾을 수 없습니다.")
                return False
            
            for category_data in category_result:
                print_data(self.print_type, category_data)
            return True

    # 영화 언어로 검색
    def read_film_language(self):
        with self.conn.cursor() as cur:
            print("========== 영화 언어 ==========")
            cur.execute("SELECT * FROM language;")
            languages = cur.fetchall()
            for language in languages:
                print(language[0], language[1])

            search_id = input("검색하려는 영화 언어를 숫자로 입력해주세요 : ")
            cur.execute("""SELECT f.film_id, f.title, f.description, f.release_year, f.rental_duration, f.rental_rate, f.length, f.replacement_cost, f.rating, c.category_id, c.name, l.language_id, l.name
                        FROM film f
                        JOIN film_category fc USING (film_id)
                        JOIN category c USING (category_id)
                        JOIN language l USING (language_id)
                        WHERE l.language_id = %s;""", (search_id,))

            language_result = cur.fetchall()
            print("\n==========검색 결과===========")

            if not language_result:
                print("해당 언어의 영화를 찾을 수 없습니다.")
                return False
            
            for language_data in language_result:
                print_data(self.print_type, language_data)
            return True
    
    # 영화배우의 출연작 검색
    def read_actor(self):
        with self.conn.cursor() as cur:
            print("검색하려는 영화배우의 이름을 입력해주세요.")
            first_name = input("First Name : ")
            last_name = input("Last Name : ")
            cur.execute("""SELECT f.film_id, f.title, f.description, f.release_year, f.rental_duration, f.rental_rate, f.length, f.replacement_cost, f.rating, c.category_id, c.name, l.language_id, l.name
                        FROM actor a 
                        JOIN film_actor fa USING (actor_id)
                        JOIN film f USING (film_id)
                        JOIN film_category fc USING (film_id)
                        JOIN category c USING (category_id)
                        JOIN language l USING (language_id)
                        WHERE first_name = %s AND last_name = %s;""", (first_name, last_name,))
            
            actor_results = cur.fetchall()
            print("\n==========검색 결과===========")

            if not actor_results:
                print("해당 배우가 출연한 영화를 찾을 수 없습니다.")
                return False
            
            for actor in actor_results:
                print_data(self.print_type, actor)
            return True
        
    # 작품의 출연배우 검색
    def read_film_actor(self):
        with self.conn.cursor() as cur:
            film_id = input("검색하려는 영화의 film_id을 입력해주세요.")
            cur.execute("""SELECT a.first_name, a.last_name, f.title
                            FROM film f 
                            JOIN film_actor fa USING (film_id)
                            JOIN actor a USING (actor_id)
                            WHERE film_id=%s;""", (film_id,))
            
            actor_results = cur.fetchall()
            print("\n==========검색 결과===========")
            if not actor_results:
                print("해당 배우가 출연한 영화를 찾을 수 없습니다.")
                return False
            print("영화 {}에 출현한 배우 목록 : ".format(actor_results[0][2]))
            for actor in actor_results:
                print(actor[0], actor[1])
            return True

    def close(self):
        self.conn.close()
            
print("데이터베이스 연결에 필요한 사전 정보를 입력해주세요.")
DBNAME = input("DBNAME : ")
USER = input("USER : ")
PASSWORD = input("PASSWORD : ")
HOST = input("HOST : ")
PORT = input("PORT : ")

film_crud = filmCRUD(DBNAME, USER, PASSWORD, HOST, PORT)


while True:
    select = input(f"""\n원하는 기능을 선택하세요. (현재 출력 방식 : {film_crud.print_type})
                   
1. 영화 제목으로 검색하기
2. 영화 장르로 검색하기
3. 영화 언어로 검색하기
4. 영화 배우로 검색하기
5. 프로그램 종료
0. 출력 방식 변경
                   
>>> """)
    if select == "1":
        input_title = input("검색할 제목을 입력해주세요 : ")
        status = film_crud.read_film_title(input_title)

    elif select == "2":
        status = film_crud.read_film_category()
        
    elif select == "3":
        status = film_crud.read_film_language()

    elif select == "4":
        print("다음 중 검색 방식을 선택하여 숫자로 입력해주세요.")
        print("1) 특정 영화 배우가 출연한 영화 작품 검색하기")
        print("2) 특정 영화 작품에 출연한 배우 검색하기")
        actor_data = input(">>> ")
        if actor_data == "1":
            film_crud.read_actor()
        elif actor_data == "2":
            film_crud.read_film_actor()
        else:
            print("번호를 잘못 선택하셨습니다. 처음 메뉴로 돌아갑니다.")

    elif select == "5":
        print("프로그램을 종료합니다.")
        break

    elif select == "0":
        print("현재 출력 방식은 {} 입니다. 변경을 원한다면 아래 중 하나를 선택해주세요.".format(film_crud.print_type))
        print("1) Print in Line : 칼럼명을 출력하지 않고 한 줄에 data의 rows를 모두 출력")
        print("2) Print in Paragraph : 칼럼명을 출력하며, 각 칼럼마다 데이터 값이 어떤지 문단 단위로 함께 출력")
        print_input = input("숫자로 입력해주세요 >>> ")
        if print_input == "1":
            film_crud.print_type = "Print in Line"
        elif print_input == "2":
            film_crud.print_type = "Print in Paragraph"
        else:
            print("번호를 잘못 선택하셨습니다. 처음 메뉴로 돌아갑니다.")
    else:
        print("번호를 잘못 선택하셨습니다. 처음 메뉴로 돌아갑니다.")

film_crud.close()