from setuptools import setup, find_packages

setup(name='ApiPytestAutomation',
      version='1.0',
      description="API Pytest automation framework solution",
      author='Sviatoslav Bordovski',
      author_email='sbordovski@gmail.com',
      packages=find_packages(),
      zip_safe=False,
      install_requires=[
          "pytest==6.2.4",
          "pytest-html==2.1.1",
          "requests==2.23.0",
          "requests-oauthlib==1.3.0",
          "PyMySQL==0.9.3",
          "WooCommerce==2.1.1",
      ]
      )
