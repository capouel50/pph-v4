from setuptools import setup, find_packages

setup(
    name='PPH',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        "amqp==5.2.0"
        "anyio==4.2.0"
        "asgiref==3.7.2"
        "async-timeout==4.0.3"
        "attrs==23.2.0"
        "autobahn==23.6.2"
        "Automat==22.10.0"
        "beautiful==0.0.2"
        "beautifulsoup4==4.12.3"
        "billiard==4.2.0"
        "celery==5.3.6"
        "certifi==2023.7.22"
        "cffi==1.15.1"
        "channels==4.0.0"
        "channels-redis==4.2.0"
        "charset-normalizer==3.2.0"
        "click==8.1.7"
        "click-didyoumean==0.3.0"
        "click-plugins==1.1.1"
        "click-repl==0.3.0"
        "colorama==0.4.6"
        "constantly==23.10.4"
        "cryptography==42.0.2"
        "daphne==4.0.0"
        "defusedxml==0.7.1"
        "distro==1.9.0"
        "dj-database-url==0.5.0"
        "dj-rest-auth==4.0.1"
        "Django==5.0.2"
        "django-allauth==0.54.0"
        "django-cors-headers==4.2.0"
        "django-redis==5.4.0"
        "django-rest-knox==4.2.0"
        "django-webpack-loader==3.0.0"
        "djangorestframework==3.14.0"
        "djangorestframework-simplejwt==5.2.2"
        "et-xmlfile==1.1.0"
        "gunicorn==21.2.0"
        "h11==0.14.0"
        "honcho==1.1.0"
        "httptools==0.6.1"
        "hyperlink==21.0.0"
        "idna==3.4"
        "incremental==22.10.0"
        "itsdangerous==2.1.2"
        "JPype1==1.5.0"
        "kombu==5.3.5"
        "msgpack==1.0.7"
        "numpy==1.26.3"
        "oauthlib==3.2.2"
        "openpyxl==3.1.2"
        "packaging==23.2"
        "pandas==2.2.0"
        "pdfminer.six==20221105"
        "pdfplumber==0.10.3"
        "pillow==10.2.0"
        "prompt-toolkit==3.0.43"
        "psycopg2==2.9.9"
        "pyasn1==0.5.1"
        "pyasn1-modules==0.3.0"
        "pycparser==2.21"
        "PyJWT==2.8.0"
        "pyodbc==5.0.1"
        "pyOpenSSL==24.0.0"
        "PyPDF2==3.0.1"
        "pypdfium2==4.26.0"
        "pyserial==3.5"
        "python-dateutil==2.8.2"
        "python-decouple==3.8"
        "python-dotenv==1.0.1"
        "python3-openid==3.2.0"
        "pytz==2023.3"
        "PyYAML==6.0.1"
        "redis==5.0.1"
        "requests==2.31.0"
        "requests-oauthlib==1.3.1"
        "service-identity==24.1.0"
        "signals==0.0.2"
        "six==1.16.0"
        "sniffio==1.3.0"
        "soupsieve==2.5"
        "sqlparse==0.4.4"
        "tabula-py==2.9.0"
        "Twisted==23.10.0"
        "twisted-iocpsupport==1.0.4"
        "txaio==23.1.1"
        "typing_extensions==4.9.0"
        "tzdata==2023.3"
        "urllib3==2.0.4"
        "uvicorn==0.27.0.post1"
        "vine==5.1.0"
        "waitress==2.1.2"
        "watchdog==4.0.0"
        "watchfiles==0.21.0"
        "wcwidth==0.2.13"
        "websockets==12.0"
        "whitenoise==6.6.0"
        "zope.interface==6.1"
    ],
    entry_points={
        'console_scripts': [
            'PPH=PPH:main',
        ],
    },
)
