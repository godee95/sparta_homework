# import requests # requests 라이브러리 설치 필요
#
# r = requests.get('http://openapi.seoul.go.kr:8088/6d4d776b466c656533356a4b4b5872/json/RealtimeCityAir/1/99')
# rjson = r.json()
#
# # print(rjson['RealtimeCityAir']['row'])
#
# gus = rjson['RealtimeCityAir']['row']
#
# for gu in gus:
#     gu_name = gu['MSRSTE_NM']
#     gu_mise = gu['IDEX_MVL']
#     if gu_mise > 30:
#         print(gu_name, gu_mise)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20200303',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

# 코딩 시작
# print(soup)

# title = soup.select_one('#old_content > table > tbody > tr:nth-child(2) > td.title > div > a')
#
# print(title)
# print(title.text)
# print(title['href'])

# title 검사, 복사
#old_content > old_content > table > tbody > tr:nth-child(2) > td.title > div > a
#old_content > table > tbody > tr:nth-child(9)

# star 검사, 복사
#old_content > table > tbody > tr:nth-child(2) > td.point

# rank 검사, 복사
#old_content > table > tbody > tr:nth-child(3) > td:nth-child(1) > img

trs = soup.select('#old_content > table > tbody > tr')

for tr in trs:
    a_tag = tr.select_one('td.title > div > a')
    # print(a_tag)
    if a_tag is not None:
        rank = tr.select_one('td:nth-child(1) > img')['alt']
        star = tr.select_one('td.point').text
        title = a_tag.text

        doc = {
            'rank':rank,
            'title': title,
            'star': star
        }
        db.movies.insert_one(doc)

        # print(rank, title, star)

# 매트릭스 평점 가져오기
movie1 = db.movies.find_one({'title':'매트릭스'}, {'_id':False})
# print(movie1['star'])

# 매트릭스 평점과 같은 영화 제목들을 가져오기
target_star = movie1['star']
target_movies = list(db.movies.find({'star': target_star}, {'_id':False}))
# print(target_movies)
for movie2 in target_movies:
    print(movie2['title'])

# 매트릭스 영화의 평점을 0으로 만들기
db.movies.update_one({'title':'매트릭스'},{'$set':{'star':'0'}})

