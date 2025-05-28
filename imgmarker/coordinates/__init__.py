
import numpy as np

class Angle(float):
    def __init__(self,dd):
        super().__init__()

    def __add__(self, value):
        return Angle(super().__add__(value))
    
    def __sub__(self, value):
        return Angle(super().__sub__(value))
    
    def __mul__(self, value):
        return Angle(super().__mul__(value))
    
    @property
    def hms(self):
        sign = np.sign(self)
        m, s = np.divmod(np.abs(self)*240, 60)
        h, m = np.divmod(m, 60)
        return sign*h, sign*m, sign*s

    @property
    def dms(self):
        sign = np.sign(self)
        m, s = np.divmod(np.abs(self)*3600, 60)
        d, m = np.divmod(m, 60)
        return sign*d, sign*m, sign*s

    def hms_str(self):
        h, m, s = self.hms
        sign_str = '+' if self >= 0 else '-'
        return rf'{sign_str}{np.abs(h):02.0f}h {np.abs(m):02.0f}m {np.abs(s):05.2f}s'