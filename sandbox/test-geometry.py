'''
All rights reserved (c) 2016-2018 Brenda A. Bell.

This file is part of the PCGenerator (see
https://github.com/brendabell/knittingtools).

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

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
