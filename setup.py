from setuptools import setup
setup(
    name = 'autosollvevv',
    version = '1.1.0',
    packages = ['autosollvevv'],
    data_files=[('json_data', ['json_data/*.json'])],
    entry_points = {
        'console_scripts': [
            'autosollvevv = autosollvevv.__main__:main'
        ]
    })
