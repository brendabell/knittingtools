import svgwrite

tractor_hole_diameter = 2.5
tractor_hole_xoffset = 4.5
tractor_hole_yoffset = 0.0
tractor_hole_yspacing = 5.25

pattern_hole_diameter = 3.0
pattern_hole_xoffset = 24.0
pattern_hole_yoffset = 23.5
pattern_hole_xspacing = 4.5
pattern_hole_yspacing = 5.25

diagram = svgwrite.Drawing(
	"test.svg",
	size=('200mm', '220mm'),
	viewBox=('0 0 200 220'),
	preserveAspectRatio='none')

diagram.add(diagram.polygon(
	points=[(10,10),(190,10),(190,210),(10,210),(10,10)],
	fill='white',
	stroke='black',
	stroke_width=.1))

x = 10 + tractor_hole_xoffset
y = 10 + tractor_hole_yoffset
for i in range(30):
    fill='green' if i == 0 else 'white'
    diagram.add(
        diagram.circle(
            center=(x,y),
            fill=fill,
            r = (tractor_hole_diameter / 2),
            stroke='black',
            stroke_width=.1))
    y = y + tractor_hole_yspacing

x = 10 + pattern_hole_xoffset
for i in range(30):
    fill='red' if i == 0 else 'white'
    y = 10 + pattern_hole_yoffset
    for j in range(30):
        fill2='blue' if j == 0 else fill
        diagram.add(
            diagram.circle(
                center=(x,y),
                fill=fill2,
                r = (pattern_hole_diameter / 2),
                stroke='black',
                stroke_width=.1))
        y = y + pattern_hole_yspacing
    x = x + pattern_hole_xspacing

print '<?xml version="1.0" encoding="UTF-8" standalone="no"?>{}'.format(diagram.tostring())
