from setuptools import setup, find_packages

setup(name='spider',
      version='0.1',
      description='spider package',
      author='taoting',
      author_email='335354289@qq.com',
      packages=find_packages(),
      install_requires=[  # 依赖列表
          'beautifulsoup4',
          'Faker',
          'lxml',
          'Pillow',
          'PyExecJS',
          'requests',
          'selenium',
          'xmltodict',
      ]
      )
