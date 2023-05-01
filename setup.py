from setuptools import setup


setup(
    name='tina',
    py_modules=['tina'],
    version="1.0",
    install_requires=[
        'flask==2.3.2',
        'timeloop==1.0.2'
    ],
    description="Background Processing Server",
    author="sebastian.lettner24@gmail.com",
)
