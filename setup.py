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
            
        compiler_type = self.compiler.compiler_type

        if compiler_type == 'msvc':
            ext.extra_compile_args = ['/W0','/Zc:__STDC__']
        if compiler_type == 'unix':
            ext.extra_compile_args = ['-Wall','-fPIC','-Wstrict-prototypes']

        #print(self.compiler.compiler_type)
        #self.compiler.compile(cfiles)
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