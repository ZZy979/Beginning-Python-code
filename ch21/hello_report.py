from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing, String

d = Drawing(100, 100)
s = String(50, 50, "Hello, world!", textAnchor='middle')

d.add(s)

renderPDF.drawToFile(d, 'hello.pdf', 'A simple PDF file')
