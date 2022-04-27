from setuptools import setup

setup(name='hand_hygiene',
      version='1.0',
      description='Library for Hand Hygiene Device for Children',
      author='Ethan Bonpin and Ruhejami Mustari',
      author_email=['eb3326@nyu.edu', 'rm4966@nyu.edu']
      url='https://github.com/RuhejamiM/hand-hygiene-device',
      install_requires=[],
	  py_modules=['hand-hygiene'],
     )

# install_requires=['pygame>=2.1.2', 'adafruit-circuitpython-rgb-display', 'fonts-dejavu', 'python3-pil'] (move back to setup after testing is complete)