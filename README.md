# mfpoj

A simple online judge system.

## First step

Clone the repo to your computer:
```
git clone git@github.com:KuribohG/mfpoj.git
```

Clone the submodule:
```
git submodule update --init --recursive
```

Satisfy prerequisities:
```
sudo pip3 install $(cat requirements.txt)
```

Install `lorunner`:
```
sudo python3 lorunner/setup.py build
sudo python3 lorunner/setup.py install
```

Then run command line:
```
python3 manage.py makemigrations oj
python3 manage.py sqlmigrate oj 0001
python3 manage.py migrate
```

If you want to create a super user:
```
python3 manage.py createsuperuser
```

To run server on your computer:
```
python3 manage.py runserver
```
