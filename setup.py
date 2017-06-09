from setuptools import setup, find_packages
import politicalplaces

setup(
    name='django-political-map',
    version=politicalplaces.__version__,
    description='Django application to store geolocalized places and organize them according to political hierarchy.',
    author='20tab S.r.l.',
    author_email='info@20tab.com',
    #url='https://gitlab.20tab.com/20tab/django-political-map',
    url='https://github.com/20tab/django-political-map.git',
    license='MIT License',
    install_requires=[
        'googlemaps==2.5.0',
    ],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.html', '*.css', '*.js', '*.gif', '*.png', ],
    }
)
