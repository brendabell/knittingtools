import svgwrite


# machine specs
specs = {
	'12-stitch-br-sr': {
		# total width of the cut card
		'card_width': 142,
		# number of overlapping blank rows at the top of the card
		'blank_rows': 2,
		# height of one row on the card in mm
		'row_height': 5.0,
		# width of one stitch on the card in mm
		'stitch_width': 9.0,
		# diameter of a pattern hole in mm
		'pattern_hole_diameter': 3.5,
		# diameter of the overlapping pattern holes in mm
		'overlap_hole_diameter': 3.5,
		# offset of the first pattern hole from the left edge of the card in mm
		'pattern_hole_xoffset': 22.5 + (3.5 / 2),
		# diameter of a clip hole in mm
		'clip_hole_diameter': 3.5,
		# offset of a clip hole from the left/right edge of the card in mm
		'clip_hole_xoffset': 5.0 + (3.5 / 2),
		# offset of a clip hole from the top/bottom edges of the card in mm
		'clip_hole_yoffset': 5.0,
		# diameter of a tractor hole in mm
		'tractor_hole_diameter': 3.0,
		# offset of a tractor hole from the left/right edge of the card in mm
		'tractor_hole_xoffset': 12.5 + (3.0 / 2),
		# offset of a tractor hole from the top/bottom edge of the card in mm
		'tractor_hole_yoffset': 2.5,
		# stitches per row
		'stitches': 12,
		# offset of the card corners
		'corner_offset': 2,
	},
	'18-stitch-mk70': {
		'card_width': 142,
		'blank_rows': 2,
		'row_height': 5.0,
		'stitch_width': 6.0,
		'pattern_hole_diameter': 3.5,
		'overlap_hole_diameter': 3.5,
		'pattern_hole_xoffset': 17.5 + (3.5 / 2),
		'clip_hole_diameter': 3.5,
		'clip_hole_xoffset': 5.0 + (3.5 / 2),
		'clip_hole_yoffset': 5.0,
		'tractor_hole_diameter': 3.0,
		'tractor_hole_xoffset': 12.5 + (3.0 / 2),
		'tractor_hole_yoffset': 2.5,
		'stitches': 18,
		'corner_offset': 2,
	},
	'24-stitch-br-sr': {
		'card_width': 142,
		'blank_rows': 2,
		'row_height': 5.0,
		'stitch_width': 4.5,
		'pattern_hole_diameter': 3.5,
		'overlap_hole_diameter': 3.5,
		'pattern_hole_xoffset': 17.5 + (3.5 / 2),
		'clip_hole_diameter': 3.5,
		'clip_hole_xoffset': 5.0 + (3.5 / 2),
		'clip_hole_yoffset': 5.0,
		'tractor_hole_diameter': 3.0,
		'tractor_hole_xoffset': 12.0 + (3.0 / 2),
		'tractor_hole_yoffset': 2.5,
		'stitches': 24,
		'corner_offset': 2,
	},
	'30-stitch-km': {
		'card_width': 142,
		'blank_rows': 2,
		'row_height': 5.0,
		'stitch_width': 3.6,
		'pattern_hole_diameter': 2.7,
		'overlap_hole_diameter': 2.7,
		'pattern_hole_xoffset': 17.5 + (2.7 / 2),
		'clip_hole_diameter': 3.5,
		'clip_hole_xoffset': 5.0 + (3.5 / 2),
		'clip_hole_yoffset': 5.0,
		'tractor_hole_diameter': 3.0,
		'tractor_hole_xoffset': 12.0 + (3.0 / 2),
		'tractor_hole_yoffset': 2.5,
		'stitches': 30,
		'corner_offset': 2,
	},
	'40-stitch-deco': {
		'card_width': 243,
		'blank_rows': 3,
		'row_height': (100.0 / 19.0),
		'stitch_width': 5.0,
		'pattern_hole_diameter': 3.7,
		'overlap_hole_diameter': 3.7,
		'pattern_hole_xoffset': 22.15 + (3.7 / 2),
		'clip_hole_diameter': 3.5,
		'clip_hole_xoffset': 2.0 + (3.5 / 2),
		'clip_hole_yoffset': 5.5,
		'tractor_hole_diameter': 3.0,
		'tractor_hole_xoffset': 12.5 + (3.0 / 2),
		'tractor_hole_yoffset': 5.5,
		'stitches': 40,
		'corner_offset': 0,
	},
}


def calibrate():

	diagram = svgwrite.Drawing(
		"calibrate.svg",
		size=(
			'100mm',
			'100mm'),
		viewBox=(
			'0 0 100 100'),
		preserveAspectRatio='none')
	diagram.add(
		diagram.polygon(
			[(10,10), (90,10), (90,90), (10,90), (10,10)],
			fill='white',
			stroke='red',
			stroke_width=.1))
	return '<?xml version="1.0" encoding="UTF-8" standalone="no"?>{}'.format(diagram.tostring())


class Layout:

	def __init__(self, machine_id, stitches, rows, horz_repeat, vert_repeat, is_blank):

		self.card_width = specs[machine_id]['card_width']
		self.blank_rows = specs[machine_id]['blank_rows']
		self.row_height = specs[machine_id]['row_height']
		self.stitch_width = specs[machine_id]['stitch_width']
		self.pattern_hole_diameter = specs[machine_id]['pattern_hole_diameter']
		self.overlap_hole_diameter = specs[machine_id]['overlap_hole_diameter']
		self.pattern_hole_xoffset = specs[machine_id]['pattern_hole_xoffset']
		self.clip_hole_diameter = specs[machine_id]['clip_hole_diameter']
		self.clip_hole_xoffset = specs[machine_id]['clip_hole_xoffset']
		self.clip_hole_yoffset = specs[machine_id]['clip_hole_yoffset']
		self.tractor_hole_diameter = specs[machine_id]['tractor_hole_diameter']
		self.tractor_hole_xoffset = specs[machine_id]['tractor_hole_xoffset']
		self.tractor_hole_yoffset = specs[machine_id]['tractor_hole_yoffset']
		self.corner_offset = specs[machine_id]['corner_offset']

		self.card_stitches = stitches
		self.card_rows = rows

		if is_blank:
			self.pattern_hole_diameter = .5

		if self.card_rows > 200 or self.card_stitches > specs[machine_id]['stitches']:
			raise ValueError(
				"Your pattern seems to exceed 200 rows and/or {} stitches. "
				"Are you sure you uploaded the right text file?".format(specs[machine_id]['stitches']))

		self.horz_repeat = horz_repeat
		self.vert_repeat = vert_repeat

		self.card_height = ((self.blank_rows * 2) + (self.card_rows * self.vert_repeat)) * self.row_height


class PCGenerator:

	def __init__(self, handler, data, machine_id, vert_repeat, is_blank = False):

		self.handler = handler
		self.data = data.split()
		self.layout = Layout(
			machine_id,
			len(self.data[0]),
			len(self.data),
			specs[machine_id]['stitches'] / len(self.data[0]),
			vert_repeat,
			is_blank
		)

	def generate(self):

		diagram = self.create_card()

		objects = []
		self.draw_pattern(diagram, self.data, objects)
		self.draw_blank_lines(diagram, objects)
		self.draw_clip_holes(diagram, objects)
		self.draw_tractor_holes(diagram, objects)

		# sort the list to optimize cutting
		sorted_objects = sorted(objects, key=lambda x: (float(x.attribs['cy']), float(x.attribs['cx'])))
		for i in sorted_objects:
			diagram.add(i)

		return '<?xml version="1.0" encoding="UTF-8" standalone="no"?>{}'.format(diagram.tostring())

	def create_card(self):

		diagram = svgwrite.Drawing(
			"punchcard.svg",
			size=(
				'{0}mm'.format(self.layout.card_width),
				'{0}mm'.format(self.layout.card_height)),
			viewBox=(
				'0 0 {0} {1}'.format(self.layout.card_width, self.layout.card_height)),
			preserveAspectRatio='none')

		diagram.add(diagram.polygon(
			points=self.get_card_shape(),
			fill='white',
			stroke='black',
			stroke_width=.1))

		return diagram

	def draw_pattern(self, diagram, lines, objects):

		# main body of card
		yoffset = (self.layout.blank_rows * self.layout.row_height) + (self.layout.row_height / 2)
		for row_repeat in range(self.layout.vert_repeat):
			for rows in range(self.layout.card_rows):
				xoffset = self.layout.pattern_hole_xoffset
				for stitch_repeat in range(self.layout.horz_repeat):
					for stitches in range(self.layout.card_stitches):
						if lines[rows][stitches].upper() == 'X':
							objects.append(diagram.circle(
								center=(xoffset, yoffset),
								fill='white',
								r = (self.layout.pattern_hole_diameter / 2),
								stroke='black',
								stroke_width=.1))
						xoffset += self.layout.stitch_width
				yoffset += self.layout.row_height

	def draw_blank_lines(self, diagram, objects):

		# blank rows at top
		yoffset = self.layout.row_height / 2
		for rows in range(self.layout.blank_rows):
			xoffset = self.layout.pattern_hole_xoffset
			for stitch_repeat in range(self.layout.horz_repeat):
				for stitches in range(self.layout.card_stitches):
					objects.append(diagram.circle(
						center=(xoffset, yoffset),
						fill='white',
						r = (self.layout.overlap_hole_diameter / 2),
						stroke='black',
						stroke_width=.1))
					xoffset += self.layout.stitch_width
			yoffset += self.layout.row_height

		# blank rows at bottom
		yoffset = (self.layout.card_height - (self.layout.row_height * self.layout.blank_rows)) + (self.layout.row_height / 2)
		for rows in range(self.layout.blank_rows):
			xoffset = self.layout.pattern_hole_xoffset
			for stitch_repeat in range(self.layout.horz_repeat):
				for stitches in range(self.layout.card_stitches):
					objects.append(diagram.circle(
						center=(xoffset, yoffset),
						fill='white',
						r = (self.layout.overlap_hole_diameter / 2),
						stroke='black',
						stroke_width=.1))
					xoffset += self.layout.stitch_width
			yoffset += self.layout.row_height

	def draw_clip_holes(self, diagram, objects):

		self.draw_side_holes(
			diagram,
			objects,
			self.layout.clip_hole_xoffset,
			self.layout.clip_hole_yoffset,
			self.layout.clip_hole_diameter)

	def draw_tractor_holes(self, diagram, objects):

		self.draw_side_holes(
			diagram,
			objects,
			self.layout.tractor_hole_xoffset,
			self.layout.tractor_hole_yoffset,
			self.layout.tractor_hole_diameter)

	def draw_side_holes(self, diagram, objects, xoffset, yoffset, diameter):

		left_xoffset = xoffset
		right_xoffset = self.layout.card_width - left_xoffset

		while yoffset < self.layout.card_height:
			# holes on left
			objects.append(diagram.circle(
				center=(left_xoffset, yoffset),
				fill='white',
				r = (diameter / 2),
				stroke='black',
				stroke_width=.1))
			# holes on right
			objects.append(diagram.circle(
				center=(right_xoffset, yoffset),
				fill='white',
				r = (diameter / 2),
				stroke='black',
				stroke_width=.1))
			yoffset += self.layout.row_height

	def get_card_shape(self):

		corner_diameter =  self.layout.corner_offset + 1

		#	   a..................b
		#	  p                    c
		#	  .                    .
		#	  o                    d
		#	 n                      e
		#	 .                      .
		#	 .                      .
		#	 .                      .
		#	 .                      .
		#	 .                      .
		#	 m                      f
		#	  l                    g
		#	  .                    .
		#	  k                    h
		#	   j..................i

		a = (corner_diameter, 0)
		b = (self.layout.card_width - corner_diameter, 0)
		c = (self.layout.card_width - self.layout.corner_offset, 1)
		d = (self.layout.card_width - self.layout.corner_offset, 20)
		e = (self.layout.card_width, 22)
		f = (self.layout.card_width, self.layout.card_height - 22)
		g = (self.layout.card_width - self.layout.corner_offset, self.layout.card_height - 20)
		h = (self.layout.card_width - self.layout.corner_offset, self.layout.card_height - 1)
		i = (self.layout.card_width - corner_diameter, self.layout.card_height)
		j = (corner_diameter, self.layout.card_height)
		k = ( self.layout.corner_offset, self.layout.card_height - 1)
		l = ( self.layout.corner_offset, self.layout.card_height - 20)
		m = (0, self.layout.card_height - 22)
		n = (0, 22)
		o = ( self.layout.corner_offset, 20)
		p = ( self.layout.corner_offset, 1)

		return [a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p]
