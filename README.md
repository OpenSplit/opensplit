# OpenSplit

Visit [opensplit.de](https://opensplit.de) to use this app.


# Start
Make sure you have Docker and docker-compose installed. 
```
docker-compose up
```
Your new Django installation should now be reachable at [localhost:8000](http://localhost:8000)


## Install new dependencies
```
echo "libraryname" >> requirements.txt
docker-compose exec web pip install -r requirements.txt
```

## Run Django commands with manage.py
```
docker-compose exec web ./manage.py <command>
```
