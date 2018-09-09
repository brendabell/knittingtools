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
