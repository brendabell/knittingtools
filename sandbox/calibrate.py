import svgwrite

diagram = svgwrite.Drawing(
	"calibrate.svg",
	size=('100mm', '100mm'),
	viewBox=('0 0 100 100'),
	preserveAspectRatio='none')

diagram.add(diagram.polygon(
	points=[(0,0),(100,0),(100,100),(0,100)],
	fill='white',
	stroke='black',
	stroke_width=.1))

diagram.add(diagram.polygon(
	points=[(10,10),(90,10),(90,90),(10,90)],
	fill='white',
	stroke='black',
	stroke_width=.1))

print '<?xml version="1.0" encoding="UTF-8" standalone="no"?>{}'.format(diagram.tostring())
