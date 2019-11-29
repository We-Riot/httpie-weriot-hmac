from setuptools import setup

setup(
    name='httpie-weriot-hmac',
    description='WeRiot HMAC Auth plugin for HTTPie.',
    long_description='WeRiot HMAC implementation for httpie',
    version='0.1.0',
    author='David De Sousa',
    author_email='davidesousa@gmail.com',
    license='MIT',
    url='https://github.com/We-Riot/httpie-weriot-hmac',
    download_url='https://github.com/We-Riot/httpie-weriot-hmac',
    py_modules=['httpie_weriot_hmac'],
    zip_safe=False,
    entry_points={
        'httpie.plugins.auth.v1': [
            'httpie_weriot_hmac = httpie_weriot_hmac:WeriotHmacPlugin'
        ]
    },
    install_requires=[
        'httpie>=1.0.3'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Environment :: Plugins',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities'
    ],
)
