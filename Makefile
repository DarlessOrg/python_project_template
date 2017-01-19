init:
	sudo pip install -r requirements.txt
	sudo pip install -e .

test:
	py.test tests

docs:
	cd docs; make html; cd ..

all: test docs
