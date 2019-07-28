from setuptools import setup


setup(name='metakernel_vanilla_python',
      version='0.8',
      description='A pseudocode kernel for Jupyter/IPython',
      long_description='A pseudocode kernel for Jupyter/IPython, written with MetaKernel',
      url='https://github.com/classroomtechtools/metakernel/tree/master/metakernel_vanilla_python',
      author='Adam Morris',
      author_email='classroomtechtools.ctt@gmail.com',
      py_modules=['metakernel_vanilla_python', 'lexer'],
      install_requires=['pygments'],
      classifiers = [
          'Framework :: IPython',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 3',
          'Topic :: System :: Shells',
      ],
      entry_points = {
        'pygments.lexers' : [
          'vanilla_python = lexer.vanilla_python_lexer:VanillaPythonLexer'
        ]
      }
)
