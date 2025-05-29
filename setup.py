from os.path import join
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

libwcs_src = join('extern','libwcs')

cfiles = [
    'wcs_wrap.c',
    'wcs.c',
    'wcsinit.c',
    'hget.c',
    'hput.c',
    'iget.c',
    'wcscon.c',
    'lin.c',
    'zpxpos.c',
    'wcstrig.c',
    'tnxpos.c',
    'platepos.c',
    'worldpos.c',
    'distort.c',
    'dsspos.c',
    'wcslib.c',
    'poly.c',
    'proj.c',
    'sph.c',
    'cel.c'
]

class libwcs_ext(build_ext):
    
    def build_extension(self,ext):
        compile_args = {
            'msvc': ['/Wall','/Zc:__STDC__','/std:c17'],
            'unix': ['-Wall','-fPIC','-std=gnu17']
        }

        ext.extra_compile_args = compile_args[self.compiler.compiler_type]
        build_ext.build_extension(self,ext)

setup(
    cmdclass = {"build_ext": libwcs_ext},
    ext_modules = [
        Extension(
            'imgmarker.libwcs._wcs',
            [join(libwcs_src,f) for f in cfiles],
        )
    ]
)