from setuptools import setup, find_packages

setup(name='django-echelon',
    version=".".join(map(str, __import__("echelon").__version__)),
    description='Middleware to make user information always available',
    author='Dennis Kaarsemaker',
    author_email='dennis@kaarsemaker.net',
    url='http://github.com/seveas/django-echelon',
    packages=find_packages(exclude=["example"]),
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development"
    ],
)
