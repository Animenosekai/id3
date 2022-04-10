from os import path

from setuptools import setup

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    readme_description = f.read()

setup(
    name="id3",
    packages=["id3"],
    version="1.0",
    license="MIT License",
    description="The most easy way to add ID3 tags to your music.",
    author="Anime no Sekai",
    author_email="niichannomail@gmail.com",
    url="https://github.com/Animenosekai/id3",
    download_url="https://github.com/Animenosekai/id3/archive/v1.0.tar.gz",
    keywords=['id3', 'song', 'songs', 'music', 'mp3', 'metadata', 'spotify'],
    install_requires=['inquirer==2.8.0', 'translatepy==2.3', 'requests==2.26.0', 'eyed3==0.9.6'],
    classifiers=['Development Status :: 5 - Production/Stable', 'License :: OSI Approved :: MIT License', 'Programming Language :: Python :: 3'],
    long_description=readme_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    python_requires='>=3.8, <4',
    entry_points={
        'console_scripts': [
            'id3 = id3.__main__:main'
        ]
    },
    package_data={
        'id3': ['LICENSE'],
    },
)
