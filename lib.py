import struct
import numpy
from collections import namedtuple

# ===============================================================
# Math
# ===============================================================

# Vertex3Type = numpy.dtype([('x', 'f4'), ('y', 'f4'), ('z', 'f4')])
# Vertex2Type = numpy.dtype([('x', 'f4'), ('y', 'f4')])

class V3(object):
  def __init__(self, x, y = None, z = None):
    if (type(x) == numpy.matrix):
      self.x, self.y, self.z = x.tolist()[0]
    else:
      self.x = x
      self.y = y
      self.z = z

  def __repr__(self):
    return "V3(%s, %s, %s)" % (self.x, self.y, self.z)

  def __mul__(self, k):
    return V3(self.x * k, self.y * k, self.z * k)

  def __add__(self, v):
    if type(v) == int or type(v) == float:
          return V3(self.x + v, self.y + v, self.z + v)
    else:
      return V3(self.x + v.x, self.y + v.y, self.z + v.z)
  
  def __sub__(self, v):
    if type(v) == int or type(v) == float:
      return V3(self.x - v, self.y - v, self.z - v)
    else:
      return V3(self.x - v.x, self.y - v.y, self.z - v.z)
  
  def norm(self):
    l = (self.x**2 + self.y**2 + self.z**2)**0.5
    return V3(self.x/l, self.y/l, self.z/l)

class V2(object):
  def __init__(self, x, y = None):
    if (type(x) == numpy.matrix):
      self.x, self.y = x.tolist()[0]
    else:
      self.x = x
      self.y = y

  def __repr__(self):
    return "V2(%s, %s)" % (self.x, self.y)

# V2 = namedtuple('Point2', ['x', 'y'])
# V3 = namedtuple('Point3', ['x', 'y', 'z'])

def sum(v0, v1):
  """
    Input: 2 size 3 vectors
    Output: Size 3 vector with the per element sum
  """
  return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)

def sub(v0, v1):
  """
    Input: 2 size 3 vectors
    Output: Size 3 vector with the per element substraction
  """
  return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)

def mul(v0, k):
  """
    Input: 2 size 3 vectors
    Output: Size 3 vector with the per element multiplication
  """
  return V3(v0.x * k, v0.y * k, v0.z *k)

def dot(v0, v1):
  """
    Input: 2 size 3 vectors
    Output: Scalar with the dot product
  """
  if type(v1) == int or type(v1) == float:
    return V3(v0.x * v1, v0.y * v1, v0.z * v1)
  else:
    return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

def cross(v0, v1):
  """
    Input: 2 size 3 vectors
    Output: Size 3 vector with the cross product
  """
  return V3(
    v0.y * v1.z - v0.z * v1.y,
    v0.z * v1.x - v0.x * v1.z,
    v0.x * v1.y - v0.y * v1.x,
  )

def length(v0):
  """
    Input: 1 size 3 vector
    Output: Scalar with the length of the vector
  """
  return (v0.x**2 + v0.y**2 + v0.z**2)**0.5

def norm(v0):
  """
    Input: 1 size 3 vector
    Output: Size 3 vector with the normal of the vector
  """
  v0length = length(v0)

  if not v0length:
    return V3(0, 0, 0)

  return V3(v0.x/v0length, v0.y/v0length, v0.z/v0length)

def bbox(*vertices):
  """
    Input: n size 2 vectors
    Output: 2 size 2 vectors defining the smallest bounding rectangle possible
  """
  xs = [ vertex.x for vertex in vertices ]
  ys = [ vertex.y for vertex in vertices ]
  xs.sort()
  ys.sort()

  return V2(int(xs[0]), int(ys[0])), V2(int(xs[-1]), int(ys[-1]))


def barycentric(A, B, C, P):
  """
    Input: 3 size 2 vectors and a point
    Output: 3 barycentric coordinates of the point in relation to the triangle formed
            * returns -1, -1, -1 for degenerate triangles
  """
  bary = cross(
    V3(C.x - A.x, B.x - A.x, A.x - P.x),
    V3(C.y - A.y, B.y - A.y, A.y - P.y)
  )

  if abs(bary.z) < 1:
    return -1, -1, -1   # this triangle is degenerate, return anything outside

  return (
    1 - (bary.x + bary.y) / bary.z,
    bary.y / bary.z,
    bary.x / bary.z
  )


def allbarycentric(A, B, C, bbox_min, bbox_max):
  barytransform = numpy.linalg.inv([[A.x, B.x, C.x], [A.y,B.y,C.y], [1, 1, 1]])
  grid = numpy.mgrid[bbox_min.x:bbox_max.x, bbox_min.y:bbox_max.y].reshape(2,-1)
  grid = numpy.vstack((grid, numpy.ones((1, grid.shape[1]))))
  barycoords = numpy.dot(barytransform, grid)
  # barycoords = barycoords[:,numpy.all(barycoords>=0, axis=0)]
  barycoords = numpy.transpose(barycoords)
  return barycoords


# ===============================================================
# Utils
# ===============================================================


def char(c):
  """
  Input: requires a size 1 string
  Output: 1 byte of the ascii encoded char
  """
  return struct.pack('=c', c.encode('ascii'))

def word(w):
  """
  Input: requires a number such that (-0x7fff - 1) <= number <= 0x7fff
         ie. (-32768, 32767)
  Output: 2 bytes

  Example:
  >>> struct.pack('=h', 1)
  b'\x01\x00'
  """
  return struct.pack('=h', w)

def dword(d):
  """
  Input: requires a number such that -2147483648 <= number <= 2147483647
  Output: 4 bytes

  Example:
  >>> struct.pack('=l', 1)
  b'\x01\x00\x00\x00'
  """
  return struct.pack('=l', d)

def color(r, g, b):
  """
  Input: each parameter must be a number such that 0 <= number <= 255
         each number represents a color in rgb
  Output: 3 bytes

  Example:
  >>> bytes([0, 0, 255])
  b'\x00\x00\xff'
  """
  return bytes([b, g, r])


# ===============================================================
# BMP
# ===============================================================

def writebmp(filename, width, height, pixels):
  f = open(filename, 'bw')

  # File header (14 bytes)
  f.write(char('B'))
  f.write(char('M'))
  f.write(dword(14 + 40 + width * height * 3))
  f.write(dword(0))
  f.write(dword(14 + 40))

  # Image header (40 bytes)
  f.write(dword(40))
  f.write(dword(width))
  f.write(dword(height))
  f.write(word(1))
  f.write(word(24))
  f.write(dword(0))
  f.write(dword(width * height * 3))
  f.write(dword(0))
  f.write(dword(0))
  f.write(dword(0))
  f.write(dword(0))

  # Pixel data (width x height x 3 pixels)
  for x in range(height):
    for y in range(width):
      f.write(pixels[x][y].toBytes())
  f.close()

#reflejo de un vector respecto a un plano
def reflect(I, N):
  return I - N * 2 * dot(I, N)
