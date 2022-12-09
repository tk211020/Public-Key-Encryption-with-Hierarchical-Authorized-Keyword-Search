DC=docker-compose
CT=vm

all: build exec

build: 
	$(DC) up -d --build

exec: 
	$(DC) exec $(CT) bash

start:
	$(DC) up -d; $(MAKE) exec

stop:
	$(DC) stop

clean: 
	$(DC) down

rebuild: clean all

