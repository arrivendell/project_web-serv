# Webito

Project made for ubuntu 13.10 or after, python 2.7

To install the dependency packages used in the project run :
sudo apt-get install python-dev libffi-dev mongodb python-pip

Then install the virtualenv for python (>=version 14.0.6)
pip install virtualenv 

you can run make in the project folder and you will see the virtual environment folders created, to laucnh the programm then just run :
./build/venv/bin/python src/run.py "config.json" 1
 
 from inside the project web_server folder