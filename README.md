# Weather Forecast Api :sunrise:

This application regularly polls an open weather api and stores the information about a particular point's forecast for the next 72 hours. It does this hourly and builds up a list of all the forecast's predictions for the temperature at that location at that time. There's a single endpoint you can hit to get the highest and lowest forecasts given based on that location and time.

## Getting app up an running

Assuming you've got a decent Docker installed this will print out version information:
```bash
docker --version
```

Now from the root of the repo run the following:
```bash
docker build --tag weather_image .
docker run -d --name weather_container -p 80:80 weather_image
```

Open a browser window and test the api by going to the urls below:
```python
# Working Endpoint
http://0.0.0.0/?latitude=41.8826&longitude=-87.6233&date=2024-09-05&utc_hour=4

# Missing a query string parameter
http://0.0.0.0/?latitude=41.8826&longitude=-87.6233&date=2024-09-05

# No data at these coordinates
http://0.0.0.0/?latitude=40&longitude=-88&date=2024-09-05&utc_hour=4
```

You can now stop your docker container:
```bash
docker stop weather_container
```

Pat yourself on the back! The internet is hard and you did a thing! :tada:

## Run tests and linter

* This assumes you have Python 3.11 and pip installed on your local machine
To check what you've got installed run these commands:
```bash
python --version
pip --version
```

```bash
pip install -r requirements.txt # installs required libraries
pylint --recursive=y . # this lints the code
pytest # this runs the unit tests
```

## Todo:
- Add support for nearby latitude/longitude searches
- Add caching in case weather api goes down
- Implement more robust database architecture
- Add unit tests
