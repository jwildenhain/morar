from setuptools import setup

setup(name='morar',
      version='0.1',
      url='http://github.com/swarchal/morar',
      description='Data management for CellProfiler',
      author='Scott Warchal',
      author_email='s.warchal@sms.ed.ac.uk',
      license='MIT',
      packages=['morar'],
      test_suite='nose.collector',
      tests_require=['nose'],
      install_requires=['pandas>=0.16',
                        'numpy>=1.0',
                        'scikit-learn>=0.16'],
      zip_safe=False)
