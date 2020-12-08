# TeamWave Hiring Assignment
### Name: Jainal Gosaliya

## Installation

- ### Easy Method
Just a Simple command to start up the cluster of Django and Redis
```
docker-compose up
```

- ###  Manual Method
1. First Make sure Redis is installed and running on `host = localhost` and `port = 6379`
> To check if redis is running type redis-cli and type ping. If it returns pong than redis is running
2. Install project dependencies
```
pip install -r requirements.txt
```
3. Open file `GLOBALS.py` and on line 15 change `REDIS_HOST = "redis"` to `REDIS_HOST = "localhost"`
## Usage
To use this project it is simple.
There are 2 API both are for search.

Endpoint for both request: http://127.0.0.1:8000/search/

1. Search Stackoverflow using `GET REQUEST`.
```
curl --location --request GET 'http://127.0.0.1:8000/search/?q=python%20not%20found&page=1''
```
There are 2 query params to this
- page
>For Pagination can be 1, 2, 3 etc (int) 
- q
> Query to search can be any search query

2. Search Stackoverflow using `POST REQUEST`
```
curl --location --request POST 'http://127.0.0.1:8000/search/' \

--form 'page="1"' \

--form 'query="python not found"'
```
This is a form request that takes 2 parameter
- page
>For Pagination can be 1, 2, 3 etc (int) 
- query
> Query to search can be any search query

**I am also attaching postman project files that can be imported in postman to directly test this project from postman. Just import `team-wave.json` to postman.**

## Working

So, whats my approach and how stuff works under the hood?
1. User will search a question using a get or post request on django app (from postman/curl)

2. In backend I will check first if this query already exists in cache. For cache i have used redis to store results. As, Redis is a high performant in-memory database, it can be used for frequent getting and setting data. I will than return those cached results from redis to client in response

If query doesn't exists in redis than I will call the stackoverflow API and serve results from there and store this new query data in redis.

3. I have also paginated the result and then served them (max 10 result per page).
Good thing to know is I have also stored individual pages in cache. So if any page exists for a query in cache i will send from redis.

4. For rate limiting I am first getting the client ip and then storing per minute and per day request count in redis.
If per minute or per day request exceeds the given criteria than i am returning 429 **Limit Exceeded** status code.

For eg.

key for Client ip 127.0.0.1

In the backend I will see how many requests came for Client as per the guidelines provided - "Search limit per min(5) and per day(100)"

If it exceeds the guidelines, i will return 429 **Limit Exceeded** status code.

## Extras
- If you open the file GLOBALS.py you can see the customization that can be applied to this project.
With just changing parameters there, one can simply change how the stackoverflow API returns request.
Also, due to this modularity in coding one can simply change different parameters such as 
redis host, rate limiting criteria, pagination per page count etc without changing the main business logic of the project/
- In extras I would like to point you to the extra efforts put by mine in containerizing the project for easy usage.
