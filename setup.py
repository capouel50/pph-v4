from setuptools import setup, find_packages

setup(
    name='PPH',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'djangorestframework==3.14.0',
        'djangorestframework-simplejwt==5.2.2',
        'gunicorn==21.2.0',
        'idna==3.4',
        'itsdangerous==2.1.2',
        'oauthlib==3.2.2',
        'packaging==23.2',
        'Pillow==10.0.0',
        'pycparser==2.21',
        'PyJWT==2.8.0',
        'pyodbc==4.0.39',
        'python-decouple==3.8',
        'python3-openid==3.2.0',
        'pytz==2023.3',
        'requests==2.31.0',
        'requests-oauthlib==1.3.1',
        'six==1.16.0',
        'sqlparse==0.4.4',
        'tzdata==2023.3',
        'urllib3==2.0.4',
        'whitenoise==6.6.0',
    ],
    entry_points={
        'console_scripts': [
            'PPH=PPH:main',
        ],
    },
)

