from setuptools import setup, find_packages


setup(
    name='smparser',
    version='0.1.0',
    url='',
    description='A high-level Web Crawling and Web Scraping framework',
    long_description=open('README.md').read(),
    author='Rafael Alonso',
    maintainer='Rafael Alonso',
    maintainer_email='rafalonso.almeida@gmail.com',
    license='MIT',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Framework :: State Machine Parser',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'License :: MIT License',
    ],
    python_requires='>=3.7',
    install_requires=[
        'chardet==3.0.4',
        'pdfminer.six==20181108',
    ],
)
