from setuptools import setup, find_packages

# Implement entry-points?
# http://stackoverflow.com/questions/774824/

setup(
    name='seasonal_jpop_scraper',
    version='17.14.01.0001',
    description='Takes livechart.me and puts data into mongodb',
    author='Michael Nguyen',
    author_email='michaelnguyenm@gmail.com',
    url='https://www.michaelmnguyen.me/',
    test_suite='tests',
    packages=find_packages(exclude=('tests'))
)
