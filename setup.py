from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='django-political-map',
    version="1.2.0",
    description='Django application to store geolocalized places and organize them according to political hierarchy.',
    author='Gabriel Giaccari, 20tab S.r.l.',
    author_email='info@20tab.com',
    url='https://github.com/20tab/django-political-map.git',
    license='MIT License',
    install_requires=[
        'googlemaps==3.0.2',
    ],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.html', '*.css', '*.js', '*.gif', '*.png', ],
    }
)
