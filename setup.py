from setuptools import setup, find_packages

setup(
    name='lvm-manager',
    version='0.1',
    description='',
    author='',
    author_email='jordan@dreamhost.com',
    install_requires=[
        'datetime',
        'cliff-tablib',
        'argparse',
        'pbr',
        'python-dateutil',
        'cliff',
    ],
    namespace_packages=['manager'],
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(exclude=['ez_setup']),
    entry_points={
        'console_scripts': [
            'lvm-manager = manager.app:main'
        ],
        'manager': [
            'create = manager.commands.create:Create',
            'extend_disk = manager.commands.extend:Extend'
        ],
    }
)
