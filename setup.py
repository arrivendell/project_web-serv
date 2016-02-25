from setuptools import setup, find_packages

setup(name='webito',
      version='1.0',
      description='Webito',
      long_description='Simple http-based api',
      author='Adrien Duffy',
      url="https://github.com/golgoth/project_web-serv-IZ",
      packages=find_packages(),
  	  include_package_data=True,
  	  install_requires=["mongoengine", "flask", "bcrypt", "flask-login", "flask-principal", "flask-wtf"],
      author_email='adrien.duffy@gmail.com'
     )