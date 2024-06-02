from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing, PolyLine

d = Drawing(14, 14)
p = PolyLine([(2, 2), (12, 12), (12, 2), (2, 12)])

d.add(p)
renderPDF.drawToFile(d, 'polyline.pdf', 'A simple polyline')
