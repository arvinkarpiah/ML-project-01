from setuptools import find_packages,setup




setup(
name='mlproject01',
version='0.0.1',
author='Arvin',
author_email='arvin.karpiah@ucalgary.ca',
packages=find_packages(),
install_requires=get_requirements('requirement.txt')

)

