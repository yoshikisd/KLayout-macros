<?xml version="1.0" encoding="utf-8"?>
<klayout-macro>
 <description/>
 <version/>
 <category>pymacros</category>
 <prolog/>
 <epilog/>
 <doc/>
 <autorun>true</autorun>
 <autorun-early>false</autorun-early>
 <shortcut/>
 <show-in-menu>false</show-in-menu>
 <group-name/>
 <menu-path/>
 <interpreter>python</interpreter>
 <dsl-interpreter-name/>
 <text>import pya
import math
#------------------------------------------------- Square ASI -------------------------------------------------#    
class Square(pya.PCellDeclarationHelper):
  def __init__(self):
    # Important: initialize the super class
    super(Square, self).__init__()
    # declare the parameters
    self.param("l", self.TypeLayer, "Layer", default = pya.LayerInfo(1, 0))
    self.param("ii", self.TypeDouble, "Island-Island gap (nm)", default = 50)
    self.param("size_ASI", self.TypeDouble, "Bounding box size (um)", default = 10.0) 
    self.param("length", self.TypeDouble, "Length (nm)", default = 470)
    self.param("width", self.TypeDouble, "Width (nm)", default = 150)
    self.param("n_stadium", self.TypeInt, "Number of points", default = 40)
    self.param("stadium", self.TypeShape, "Stadium nanoisland", default = pya.Polygon([pya.DPoint(0,0),pya.DPoint(0.1,0),pya.DPoint(0,0.1)]))

  def display_text_impl(self):
    # Provide a descriptive text for the cell
    return "Square(gap="+('%.3f' % self.ii)+", W="+('%.3f' % self.width) + ", L="+('%.3f' % self.length) + ")"
  
  def coerce_parameters_impl(self):
    if self.size_ASI &lt;= 4:
      self.size_ASI = 4 
  
  def can_create_from_shape_impl(self):
    # Implement the "Create PCell from shape" protocol: we can use any shape which has a finite bounding box
    return self.shape.is_polygon()
  
  def parameters_from_shape_impl(self):
    # Implement the "Create PCell from shape" protocol: we set r and l from the shape's bounding box width and layer
    self.l = self.layout.get_info(self.layer)
  
  def transformation_from_shape_impl(self):
    # Implement the "Create PCell from shape" protocol: we use the center of the shape's bounding box to determine the transformation
    return pya.Trans(self.shape.bbox().center())
  
  def produce_impl(self):
    # fetch the parameters
    length_dbu = self.length / self.layout.dbu / 1000
    radius_dbu = self.width / self.layout.dbu /2 / 1000
    x_dbu = (length_dbu - 2*radius_dbu)/2
    ii_dbu = self.ii / self.layout.dbu / 1000
    rt2 = math.sqrt(2)
    a_dbu = 1/rt2*(radius_dbu*(4-2*rt2) + length_dbu*rt2 + 2*ii_dbu)
    size_ASI_dbu = self.size_ASI / self.layout.dbu
    # compute the stadium
    pts = []
    self.n_stadium = 12
    da = math.pi * 2 / self.n_stadium
    for i in range(round(self.n_stadium/2), self.n_stadium+1):
      pts.append(pya.Point.from_dpoint(pya.DPoint(radius_dbu * math.cos(i * da - math.pi/2) - x_dbu, radius_dbu * math.sin(i * da + math.pi/2))))
    pts.append(pya.Point.from_dpoint(pya.DPoint(-x_dbu, radius_dbu)))
    pts.append(pya.Point.from_dpoint(pya.DPoint(x_dbu, radius_dbu)))
    for i in range(self.n_stadium,self.n_stadium+round(self.n_stadium/2)+1):
      pts.append(pya.Point.from_dpoint(pya.DPoint(radius_dbu * math.cos(i * da - math.pi/2) + x_dbu, radius_dbu * math.sin(i * da + math.pi/2))))
    # Construct right-side half-dome
    pts.append(pya.Point.from_dpoint(pya.DPoint(x_dbu, -radius_dbu)))
    pts.append(pya.Point.from_dpoint(pya.DPoint(-x_dbu, -radius_dbu)))
    self.stadium = pya.Polygon(pts)
    # Determine the number of nanoislands needed to fill the bounding box
    n = math.ceil(size_ASI_dbu/a_dbu*math.sqrt(2)/2)
    # Create the array
    for j in range(1, n*2+1):
      for k in range(0, n*2):
        x_a = a_dbu*j
        y_a = a_dbu*k
        if (j+k) % 2 == 0:
           #tt = pya.Trans(0,0,a_dbu*(j-k)/2 + a_dbu*(j%2), a_dbu*(j+k)/2)
           tt = pya.Trans(0,0,a_dbu*(j-k)/2, a_dbu*(j+k)/2)
        else:
          # tt = pya.Trans(1,0,a_dbu*(j-k)/2 + a_dbu*(j%2), a_dbu*(j+k)/2)
          tt = pya.Trans(1,0,a_dbu*(j-k)/2, a_dbu*(j+k)/2)
        self.cell.shapes(self.l_layer).insert(tt.trans(self.stadium))
    self.cell.shapes(self.l_layer).transform(pya.ICplxTrans(1,45,0,0,0))

#------------------------------------------------- Brickwork ASI -------------------------------------------------#    
class Brickwork(pya.PCellDeclarationHelper):
  def __init__(self):
    # Important: initialize the super class
    super(Brickwork, self).__init__()
    # declare the parameters
    self.param("l", self.TypeLayer, "Layer", default = pya.LayerInfo(1, 0))
    self.param("ii", self.TypeDouble, "Island-Island gap (nm)", default = 50)
    self.param("size_ASI", self.TypeDouble, "Bounding box size (um)", default = 10.0) 
    self.param("length", self.TypeDouble, "Length (nm)", default = 470)
    self.param("width", self.TypeDouble, "Width (nm)", default = 150)
    self.param("n_stadium", self.TypeInt, "Number of points", default = 40)
    self.param("stadium", self.TypeShape, "Stadium nanoisland", default = pya.Polygon([pya.DPoint(0,0),pya.DPoint(0.1,0),pya.DPoint(0,0.1)]))

  def display_text_impl(self):
    # Provide a descriptive text for the cell
    return "Brickwork(gap="+('%.3f' % self.ii)+", W="+('%.3f' % self.width) + ", L="+('%.3f' % self.length) + ")"
  
  def coerce_parameters_impl(self):
    if self.size_ASI &lt;= 4:
      self.size_ASI = 4 
  
  def can_create_from_shape_impl(self):
    # Implement the "Create PCell from shape" protocol: we can use any shape which has a finite bounding box
    return self.shape.is_polygon()
  
  def parameters_from_shape_impl(self):
    # Implement the "Create PCell from shape" protocol: we set r and l from the shape's bounding box width and layer
    self.l = self.layout.get_info(self.layer)
  
  def transformation_from_shape_impl(self):
    # Implement the "Create PCell from shape" protocol: we use the center of the shape's bounding box to determine the transformation
    return pya.Trans(self.shape.bbox().center())
  
  def produce_impl(self):
    # fetch the parameters
    length_dbu = self.length / self.layout.dbu / 1000
    radius_dbu = self.width / self.layout.dbu /2 / 1000
    x_dbu = (length_dbu - 2*radius_dbu)/2
    ii_dbu = self.ii / self.layout.dbu / 1000
    rt2 = math.sqrt(2)
    a_dbu = 1/rt2*(radius_dbu*(4-2*rt2) + length_dbu*rt2 + 2*ii_dbu)
    size_ASI_dbu = self.size_ASI / self.layout.dbu
    # compute the stadium
    pts = []
    self.n_stadium = 12
    da = math.pi * 2 / self.n_stadium
    for i in range(round(self.n_stadium/2), self.n_stadium+1):
      pts.append(pya.Point.from_dpoint(pya.DPoint(radius_dbu * math.cos(i * da - math.pi/2) - x_dbu, radius_dbu * math.sin(i * da + math.pi/2))))
    pts.append(pya.Point.from_dpoint(pya.DPoint(-x_dbu, radius_dbu)))
    pts.append(pya.Point.from_dpoint(pya.DPoint(x_dbu, radius_dbu)))
    for i in range(self.n_stadium,self.n_stadium+round(self.n_stadium/2)+1):
      pts.append(pya.Point.from_dpoint(pya.DPoint(radius_dbu * math.cos(i * da - math.pi/2) + x_dbu, radius_dbu * math.sin(i * da + math.pi/2))))
    # Construct right-side half-dome
    pts.append(pya.Point.from_dpoint(pya.DPoint(x_dbu, -radius_dbu)))
    pts.append(pya.Point.from_dpoint(pya.DPoint(-x_dbu, -radius_dbu)))
    self.stadium = pya.Polygon(pts) 
    # Determine the number of nanoislands needed to fill the bounding box
    n = math.ceil(size_ASI_dbu/a_dbu*math.sqrt(2)/2)
    # Redefine the lattice parameter in terms of the island-island spacing
    for j in range(0, n*2-1):
      for k in range(1, n*2):
        x_a = a_dbu*j
        y_a = a_dbu*k
        if not ((j == 0 and k == 1) or (j == n*2-2 and k == n*2-1)):
          if (j+k) % 2 == 0:
             #tt = pya.Trans(0,0,a_dbu*(j-k)/2 + a_dbu*(j%2), a_dbu*(j+k)/2)
             tt = pya.Trans(0,0,a_dbu*(j-k)/2, a_dbu*(j+k)/2)
          else:
            # tt = pya.Trans(1,0,a_dbu*(j-k)/2 + a_dbu*(j%2), a_dbu*(j+k)/2)
            tt = pya.Trans(1,0,a_dbu*(j-k)/2 + a_dbu*(j%2), a_dbu*(j+k)/2)
          self.cell.shapes(self.l_layer).insert(tt.trans(self.stadium))
    self.cell.shapes(self.l_layer).transform(pya.ICplxTrans(1,45,0,0,0))
    
#------------------------------------------------- Kagome ASI -------------------------------------------------#    
class Kagome(pya.PCellDeclarationHelper):
  def __init__(self):
    # Important: initialize the super class
    super(Kagome, self).__init__()
    # declare the parameters
    self.param("l", self.TypeLayer, "Layer", default = pya.LayerInfo(1, 0))
    self.param("ii", self.TypeDouble, "Island-Island gap (nm)", default = 50)
    self.param("size_ASI", self.TypeDouble, "Bounding box size (um)", default = 10.0) 
    self.param("length", self.TypeDouble, "Length (nm)", default = 470)
    self.param("width", self.TypeDouble, "Width (nm)", default = 150)
    self.param("n_stadium", self.TypeInt, "Number of points", default = 40)
    self.param("stadium", self.TypeShape, "Stadium nanoisland", default = pya.Polygon([pya.DPoint(0,0),pya.DPoint(0.1,0),pya.DPoint(0,0.1)]))

  def display_text_impl(self):
    # Provide a descriptive text for the cell
    return "Kagome(gap="+('%.3f' % self.ii)+", W="+('%.3f' % self.width) + ", L="+('%.3f' % self.length) + ")"
  
  def coerce_parameters_impl(self):
    if self.size_ASI &lt;= 4:
      self.size_ASI = 4 
  
  def can_create_from_shape_impl(self):
    # Implement the "Create PCell from shape" protocol: we can use any shape which has a finite bounding box
    return self.shape.is_polygon()
  
  def parameters_from_shape_impl(self):
    # Implement the "Create PCell from shape" protocol: we set r and l from the shape's bounding box width and layer
    self.l = self.layout.get_info(self.layer)
  
  def transformation_from_shape_impl(self):
    # Implement the "Create PCell from shape" protocol: we use the center of the shape's bounding box to determine the transformation
    return pya.Trans(self.shape.bbox().center())
  
  def produce_impl(self):
    # Fetch the parameters
    self.n_stadium = 17
    length_dbu = self.length / self.layout.dbu / 1000
    radius_dbu = self.width / self.layout.dbu /2 / 1000
    x_dbu = (length_dbu - 2*radius_dbu)/2
    ii_dbu = self.ii / self.layout.dbu / 1000
    rt3 = math.sqrt(3)
    r = (1/rt3)*(length_dbu*(3/2) + ii_dbu*rt3 + radius_dbu*(2*rt3 - 3))
    a = r*2/rt3
    size_ASI_dbu = self.size_ASI / self.layout.dbu
    # Compute the stadium
    pts = []
    self.n_stadium = 12
    da = math.pi * 2 / self.n_stadium
    for i in range(round(self.n_stadium/2), self.n_stadium+1):
      pts.append(pya.Point.from_dpoint(pya.DPoint(radius_dbu * math.cos(i * da - math.pi/2) - x_dbu, radius_dbu * math.sin(i * da + math.pi/2))))
    pts.append(pya.Point.from_dpoint(pya.DPoint(-x_dbu, radius_dbu)))
    pts.append(pya.Point.from_dpoint(pya.DPoint(x_dbu, radius_dbu)))
    for i in range(self.n_stadium,self.n_stadium+round(self.n_stadium/2)+1):
      pts.append(pya.Point.from_dpoint(pya.DPoint(radius_dbu * math.cos(i * da - math.pi/2) + x_dbu, radius_dbu * math.sin(i * da + math.pi/2))))
    # Construct right-side half-dome
    pts.append(pya.Point.from_dpoint(pya.DPoint(x_dbu, -radius_dbu)))
    pts.append(pya.Point.from_dpoint(pya.DPoint(-x_dbu, -radius_dbu)))
    self.stadium = pya.Polygon(pts)
    # Compute the kagome ASI
    n = math.ceil(size_ASI_dbu/a)
    # Force the j range to comply with "2 + 4*n"
    n_j = 4*(math.ceil(n/4)+1)+2
    # Force the k range to scale with the j range
    n_k = 2*(math.ceil(n/2)+1)
    for j in range(0,n_j+1):
      for k in range(0,n_k+1):
        # For all even indices, construct vertical wiggle chain
        if j%2==0:
          if k%2==0 and k!=(n_k):
            tt = pya.ICplxTrans(1,-60*(-1)**(round(j/2)),0,a*(3/4*j),r*k)
          elif k%2!=0 and k!=(n_k):
            tt = pya.ICplxTrans(1,60*(-1)**(round(j/2)),0,a*(3/4*j),r*k)
        elif k%2==0:
          if math.ceil(j/2)%2==0 and k!=(n_k):
            tt = pya.ICplxTrans(1,0,0,a*(3/4*j),r*(k+1/2))
          elif math.ceil(j/2)%2!=0:
            if k!=(n_k):
              tt = pya.ICplxTrans(1,0,0,a*(3/4*j),r*(k-1/2))
            else:
              tt = pya.ICplxTrans(1,0,0,a*(3/4*j),r*(k-1/2))
        island = pya.Region(tt.trans(self.stadium))
        self.cell.shapes(self.l_layer).insert(island)

#------------------------------------------------- Quadrupole ASI -------------------------------------------------#        
class Quadrupole(pya.PCellDeclarationHelper):
  def __init__(self):
    # Important: initialize the super class
    super(Quadrupole, self).__init__()
    # declare the parameters
    self.param("l", self.TypeLayer, "Layer", default = pya.LayerInfo(1, 0))
    self.param("ii", self.TypeInt, "Island-Island spacing (nm)", default = 50)
    self.param("b", self.TypeDouble, "Trident-Trident spacing (nm)", default = 50)
    self.param("size_ASI", self.TypeDouble, "Bounding box size (um)", default = 10.0) 
    self.param("length", self.TypeDouble, "Length (nm)", default = 470.0)
    self.param("width", self.TypeDouble, "Width (nm)", default = 150.0)
    self.param("n_stadium", self.TypeInt, "Points to create stadium", default = 40)
    self.param("stadium", self.TypeShape, "Stadium nanoisland", default = pya.Polygon([pya.DPoint(0,0),pya.DPoint(0.1,0),pya.DPoint(0,0.1)]))

  def display_text_impl(self):
    # Provide a descriptive text for the cell
    return "Quadrupole(gap="+('%.3f' % self.ii)+", W="+('%.3f' % self.width) + ", L="+('%.3f' % self.length) + ")"
  
  def coerce_parameters_impl(self):
    if self.size_ASI &lt;= 4:
      self.size_ASI = 4 
      
  def can_create_from_shape_impl(self):
    # Implement the "Create PCell from shape" protocol: we can use any shape which has a finite bounding box
    return self.shape.is_polygon()
  
  def parameters_from_shape_impl(self):
    # Implement the "Create PCell from shape" protocol: we set r and l from the shape's bounding box width and layer
    self.l = self.layout.get_info(self.layer)
  
  def transformation_from_shape_impl(self):
    # Implement the "Create PCell from shape" protocol: we use the center of the shape's bounding box to determine the transformation
    return pya.Trans(self.shape.bbox().center())
  
  def produce_impl(self):
    # Fetch the parameters
    length_dbu = self.length / self.layout.dbu / 1000
    radius_dbu = self.width / self.layout.dbu /2 / 1000
    x_dbu = (length_dbu - 2*radius_dbu)/2
    a_dbu = (self.ii + self.width) / self.layout.dbu / 1000
    b_dbu = self.b / self.layout.dbu / 1000
    size_ASI_dbu = self.size_ASI / self.layout.dbu
    # Compute the stadium
    pts = []
    self.n_stadium = 12
    da = math.pi * 2 / self.n_stadium
    for i in range(round(self.n_stadium/2), self.n_stadium+1):
      pts.append(pya.Point.from_dpoint(pya.DPoint(radius_dbu * math.cos(i * da - math.pi/2) - x_dbu, radius_dbu * math.sin(i * da + math.pi/2))))
    pts.append(pya.Point.from_dpoint(pya.DPoint(-x_dbu, radius_dbu)))
    pts.append(pya.Point.from_dpoint(pya.DPoint(x_dbu, radius_dbu)))
    for i in range(self.n_stadium,self.n_stadium+round(self.n_stadium/2)+1):
      pts.append(pya.Point.from_dpoint(pya.DPoint(radius_dbu * math.cos(i * da - math.pi/2) + x_dbu, radius_dbu * math.sin(i * da + math.pi/2))))
    # Construct right-side half-dome
    pts.append(pya.Point.from_dpoint(pya.DPoint(x_dbu, -radius_dbu)))
    pts.append(pya.Point.from_dpoint(pya.DPoint(-x_dbu, -radius_dbu)))
    self.stadium = pya.Polygon(pts)
    # Compute the trident unit cell
    tt = pya.Trans(0,0,0,a_dbu*(-1/2))
    trident = pya.Region(tt.trans(self.stadium))
    tt = pya.Trans(0,0,0,a_dbu*(1/2))
    trident = trident + pya.Region(tt.trans(self.stadium))
    # Construct the trident ASI
    halfWidth = length_dbu/2
    halfHeight = (radius_dbu + a_dbu)
    #a_dbu = (halfWidth + halfHeight + b_dbu)
    a = length_dbu/2+self.ii/2+radius_dbu*2+b_dbu
    n = math.ceil(size_ASI_dbu/a/math.sqrt(2))
    for j in range(0,n*2-1):
      for k in range(0,n*2):
        # If the trident is to the left/right
        if (j+k) % 2 == 0:
           tt = pya.Trans(0,0,a*(j-k)/2 + a*(j%2), a*(j+k)/2)
        else:
           tt = pya.Trans(1,0,a*(j-k-1)/2, a*(j+k-1)/2 + a * (j%2))
        self.cell.shapes(self.l_layer).insert(trident,tt)
    self.cell.shapes(self.l_layer).transform(pya.ICplxTrans(1,45,0,0,0))

#------------------------------------------------- Trident ASI -------------------------------------------------#        
class Trident(pya.PCellDeclarationHelper):
  def __init__(self):
    # Important: initialize the super class
    super(Trident, self).__init__()
    # declare the parameters
    self.param("l", self.TypeLayer, "Layer", default = pya.LayerInfo(1, 0))
    self.param("ii", self.TypeInt, "Island-Island spacing (nm)", default = 50)
    self.param("b", self.TypeDouble, "Trident-Trident spacing (nm)", default = 50)
    self.param("size_ASI", self.TypeDouble, "Bounding box size (um)", default = 10.0) 
    self.param("length", self.TypeDouble, "Length (nm)", default = 470.0)
    self.param("width", self.TypeDouble, "Width (nm)", default = 150.0)
    self.param("n_stadium", self.TypeInt, "Points to create stadium", default = 40)
    self.param("stadium", self.TypeShape, "Stadium nanoisland", default = pya.Polygon([pya.DPoint(0,0),pya.DPoint(0.1,0),pya.DPoint(0,0.1)]))

  def display_text_impl(self):
    # Provide a descriptive text for the cell
    return "Trident(gap="+('%.3f' % self.ii)+", W="+('%.3f' % self.width) + ", L="+('%.3f' % self.length) + ")"
  
  def coerce_parameters_impl(self):
    if self.size_ASI &lt;= 4:
      self.size_ASI = 4 
      
  def can_create_from_shape_impl(self):
    # Implement the "Create PCell from shape" protocol: we can use any shape which has a finite bounding box
    return self.shape.is_polygon()
  
  def parameters_from_shape_impl(self):
    # Implement the "Create PCell from shape" protocol: we set r and l from the shape's bounding box width and layer
    self.l = self.layout.get_info(self.layer)
  
  def transformation_from_shape_impl(self):
    # Implement the "Create PCell from shape" protocol: we use the center of the shape's bounding box to determine the transformation
    return pya.Trans(self.shape.bbox().center())
  
  def produce_impl(self):
    # Fetch the parameters
    length_dbu = self.length / self.layout.dbu / 1000
    radius_dbu = self.width / self.layout.dbu /2 / 1000
    x_dbu = (length_dbu - 2*radius_dbu)/2
    a_dbu = (self.ii + self.width) / self.layout.dbu / 1000
    b_dbu = self.b / self.layout.dbu / 1000
    size_ASI_dbu = self.size_ASI / self.layout.dbu
    # Compute the stadium
    pts = []
    self.n_stadium = 12
    da = math.pi * 2 / self.n_stadium
    for i in range(round(self.n_stadium/2), self.n_stadium+1):
      pts.append(pya.Point.from_dpoint(pya.DPoint(radius_dbu * math.cos(i * da - math.pi/2) - x_dbu, radius_dbu * math.sin(i * da + math.pi/2))))
    pts.append(pya.Point.from_dpoint(pya.DPoint(-x_dbu, radius_dbu)))
    pts.append(pya.Point.from_dpoint(pya.DPoint(x_dbu, radius_dbu)))
    for i in range(self.n_stadium,self.n_stadium+round(self.n_stadium/2)+1):
      pts.append(pya.Point.from_dpoint(pya.DPoint(radius_dbu * math.cos(i * da - math.pi/2) + x_dbu, radius_dbu * math.sin(i * da + math.pi/2))))
    # Construct right-side half-dome
    pts.append(pya.Point.from_dpoint(pya.DPoint(x_dbu, -radius_dbu)))
    pts.append(pya.Point.from_dpoint(pya.DPoint(-x_dbu, -radius_dbu)))
    self.stadium = pya.Polygon(pts)
    # Compute the trident unit cell
    trident = pya.Region(self.stadium)
    for i in range(-1,2):
      tt = pya.Trans(0,0,0,a_dbu*i)
      trident = trident+pya.Region(tt.trans(self.stadium))
    # Construct the trident ASI
    halfWidth = length_dbu/2
    halfHeight = (radius_dbu + a_dbu)
    a = halfWidth + halfHeight + b_dbu
    n = math.ceil(size_ASI_dbu/a*math.sqrt(2)/2)
    for j in range(0,n*2-1):
      for k in range(0,n*2):
        # If the trident is to the left/right
        if (j+k) % 2 == 0:
           tt = pya.Trans(0,0,a*(j-k)/2 + a*(j%2), a*(j+k)/2)
        else:
           tt = pya.Trans(1,0,a*(j-k-1)/2, a*(j+k-1)/2 + a * (j%2))
        self.cell.shapes(self.l_layer).insert(trident,tt)
    self.cell.shapes(self.l_layer).transform(pya.ICplxTrans(1,45,0,0,0))
    
#------------------------------------------------- Pinwheel ASI -------------------------------------------------#    
class Pinwheel(pya.PCellDeclarationHelper):
  def __init__(self):
    # Important: initialize the super class
    super(Pinwheel, self).__init__()
    # declare the parameters
    self.param("l", self.TypeLayer, "Layer", default = pya.LayerInfo(1, 0))
    self.param("ii", self.TypeDouble, "Island-Island gap (nm)", default = 50)
    self.param("size_ASI", self.TypeDouble, "Bounding box size (um)", default = 10.0) 
    self.param("length", self.TypeDouble, "Length (nm)", default = 470)
    self.param("width", self.TypeDouble, "Width (nm)", default = 150)
    self.param("n_stadium", self.TypeInt, "Number of points", default = 40)
    self.param("stadium", self.TypeShape, "Stadium nanoisland", default = pya.Polygon([pya.DPoint(0,0),pya.DPoint(0.1,0),pya.DPoint(0,0.1)]))

  def display_text_impl(self):
    # Provide a descriptive text for the cell
    return "Pinwheel(gap="+('%.3f' % self.ii)+", W="+('%.3f' % self.width) + ", L="+('%.3f' % self.length) + ")"
  
  def coerce_parameters_impl(self):
    if self.size_ASI &lt;= 4:
      self.size_ASI = 4 
  
  def can_create_from_shape_impl(self):
    # Implement the "Create PCell from shape" protocol: we can use any shape which has a finite bounding box
    return self.shape.is_polygon()
  
  def parameters_from_shape_impl(self):
    # Implement the "Create PCell from shape" protocol: we set r and l from the shape's bounding box width and layer
    self.l = self.layout.get_info(self.layer)
  
  def transformation_from_shape_impl(self):
    # Implement the "Create PCell from shape" protocol: we use the center of the shape's bounding box to determine the transformation
    return pya.Trans(self.shape.bbox().center())
  
  def produce_impl(self):
    # fetch the parameters
    length_dbu = self.length / self.layout.dbu / 1000
    radius_dbu = self.width / self.layout.dbu /2 / 1000
    x_dbu = (length_dbu - 2*radius_dbu)/2
    a_dbu = self.ii / self.layout.dbu / 1000 + length_dbu / 2 + radius_dbu
    size_ASI_dbu = self.size_ASI / self.layout.dbu
    # compute the stadium
    pts = []
    self.n_stadium = 12
    da = math.pi * 2 / self.n_stadium
    for i in range(round(self.n_stadium/2), self.n_stadium+1):
      pts.append(pya.Point.from_dpoint(pya.DPoint(radius_dbu * math.cos(i * da - math.pi/2) - x_dbu, radius_dbu * math.sin(i * da + math.pi/2))))
    pts.append(pya.Point.from_dpoint(pya.DPoint(-x_dbu, radius_dbu)))
    pts.append(pya.Point.from_dpoint(pya.DPoint(x_dbu, radius_dbu)))
    for i in range(self.n_stadium,self.n_stadium+round(self.n_stadium/2)+1):
      pts.append(pya.Point.from_dpoint(pya.DPoint(radius_dbu * math.cos(i * da - math.pi/2) + x_dbu, radius_dbu * math.sin(i * da + math.pi/2))))
    # Construct right-side half-dome
    pts.append(pya.Point.from_dpoint(pya.DPoint(x_dbu, -radius_dbu)))
    pts.append(pya.Point.from_dpoint(pya.DPoint(-x_dbu, -radius_dbu)))
    self.stadium = pya.Polygon(pts)   
    # Determine the number of nanoislands needed to fill the bounding box
    n = math.ceil(size_ASI_dbu/a_dbu*math.sqrt(2)/2)
    # Create the array
    for j in range(0, n*2-1):
      for k in range(0, n*2):
        x_a = a_dbu*j
        y_a = a_dbu*k
        if (j+k) % 2 == 0:
          tt = pya.Trans(0,0,(x_a-y_a)/2 + a_dbu*(j%2),(x_a+y_a)/2)
        else:
          tt = pya.Trans(1,0,(x_a-y_a+a_dbu)/2,(x_a+y_a+a_dbu)/2 + a_dbu * (j%2))
        self.cell.shapes(self.l_layer).insert(tt.trans(self.stadium))
    self.cell.shapes(self.l_layer).transform(pya.ICplxTrans(1,45,0,0,0))


class ASI(pya.Library):
  def __init__(self):
    # Set the description
    self.description = "Artificial spin ices"
    # Create the PCell declarations
    self.layout().register_pcell("Square", Square())
    self.layout().register_pcell("Brickwork", Brickwork())
    self.layout().register_pcell("Kagome", Kagome())
    self.layout().register_pcell("Quadrupole", Quadrupole())
    self.layout().register_pcell("Trident", Trident())
    self.layout().register_pcell("Pinwheel", Pinwheel())
    self.register("ASI")

# Instantiate and register the library
ASI()

</text>
</klayout-macro>
