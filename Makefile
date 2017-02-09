init:
	sudo pip install -r requirements.txt
	sudo pip install -e .

docker:
	pip install -r requirements.txt
	pip install -e .

test:
	rm -rf .test_build
	py.test tests

docs:
	cd docs; make html; cd ..

all: test docs
