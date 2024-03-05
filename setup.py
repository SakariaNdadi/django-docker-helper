from setuptools import setup, find_packages

setup(
    name='django-docker-helper',
    version='1.0.0',
    description='A Django package to simplify the creation of Dockerfile and docker-compose.yml files.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/SakariaNdadi/django-docker',
    author='Sakaria Ndadi',
    author_email='oipapi.ndadi@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='django docker docker-compose',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=4',
    ],
)

