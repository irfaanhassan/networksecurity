'''
the setup.py file is essential part of packaging and distributing python 
projects .its is used by setuptools to definr the congig of your project
such as its metadata ,dependencies,req and more 
'''



from setuptools import find_packages,setup
from typing import List


def get_requirements()->List[str]:
    '''
    this function will return list of requirements
    '''
    requirement_lst:List[str]=[]
    try:
        with open('requirements.txt','r') as file:
            lines=file.readlines()
            for line in lines:
                requirement=line.strip()
                #ignore empty lines and -e
                if requirement and requirement!='-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("req.txt file not found")

    return requirement_lst

setup(
    name="Network Security",
    author="mohd irfaan hassan khan",
    version='0.0.1',
    author_email="irfaanhassan005@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)