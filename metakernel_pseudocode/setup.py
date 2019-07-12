from setuptools import setup


setup(name='metakernel_pseudocode',
      version='0.7',
      description='An IB Pseudocode kernel for Jupyter/IPython',
      long_description='An IB Pseudocode kernel for Jupyter/IPython, based on MetaKernel',
      url='https://github.com/classroomtechtools/metakernel/tree/master/metakernel_pseudocode',
      author='Adam Morris',
      author_email='classroomtechtools.ctt@gmail.com',
      py_modules=['metakernel_pseudocode'],
      install_requires=['metakernel', 'pygments', 'ib_pseudocode_python @ git+ssh://git@github.com/classroomtechtools/ib_pseudocode_python@master'],
      classifiers = [
          'Framework :: IPython',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 3',
          'Topic :: System :: Shells',
      ]
)
