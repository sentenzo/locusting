run:
	locust -f .\locust_files --class-picker

lint:
	black .
	isort .