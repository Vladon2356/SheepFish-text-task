build_containers:
	docker-compose -f docker-compose.yml up --build --remove-orphans

start_containers:
	docker-compose -f docker-compose.yml up

stop_containers:
	docker-compose -f docker-compose.yml down

remove_containers:
	docker-compose -f docker-compose.yml down -v


create_admin:
	python manage.py shell -c "from django.contrib.auth import get_user_model; get_user_model().objects.create_superuser('admin', 'admin@gmail.com', 'admin')"