# mfpoj

A simple online judge system.

## First step

Clone the repo to your computer:
```
git clone git@github.com:KuribohG/mfpoj.git
cd mfpoj
```

Clone the submodule:
```
git submodule update --init --recursive
```

Satisfy prerequisites:
```
sudo pip3 install $(cat requirements.txt)
```

Install `lorunner`:
```
cd lorunner
sudo python3 setup.py build
sudo python3 setup.py install
cd ..
```

Then run command line:
```
python3 manage.py makemigrations oj
python3 manage.py makemigrations contest
python3 manage.py sqlmigrate oj 0001
python3 manage.py sqlmigrate contest 0001
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

## FAQ

If PermissionError when adding testcases:
```
cd /
sudo chmod -R 777 var
```

If OperationalError:
```
python3 manage.py makemigrations oj
python3 manage.py makemigrations contest
python3 manage.py sqlmigrate oj 0001
python3 manage.py sqlmigrate contest 0001
python3 manage.py migrate
```
