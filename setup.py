from setuptools import setup
setup(
    name = 'autosollve',
    version = '1.1.0',
    packages = ['autosollve','json_data'],
    data_files=[('json_data', ['json_data/*.json'])],
    entry_points = {
        'console_scripts': [
            'autosollve = autosollve.__main__:main'
        ]
    })
