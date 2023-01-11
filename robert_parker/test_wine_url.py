import requests

url = 'https://pl.ww-test.winewebb.com/content-manager/collection-types/api::robert-parker.robert-parker?page=1&pageSize=100&sort=fullName:ASC'
json_data = requests.get(url, headers={
    'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTcsImlhdCI6MTY3MTE4NjM1MiwiZXhwIjoxNjczNzc4MzUyfQ.4TsWbjhfmrbhzpO9OU5sHcjhlnNmMRzkDmRA22Rc3yI'}).json()
pass