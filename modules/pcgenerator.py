import svgwrite
import json


machine_config = None


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

	def __init__(self, machine_id, stitches, rows, horz_repeat, vert_repeat, is_blank, is_solid_fill):

		global machine_config

		self.machine_id = machine_id
		self.card_width = machine_config['card_width']
		self.card_stitches = stitches
		self.row_height = machine_config['row_height']
		self.stitch_width = machine_config['stitch_width']
		self.pattern_hole_diameter = machine_config['pattern_hole_diameter']
		self.pattern_hole_xoffset = machine_config['pattern_hole_xoffset']
		self.pattern_hole_yoffset = machine_config['pattern_hole_yoffset']
		self.clip_hole_diameter = machine_config['clip_hole_diameter']
		self.clip_hole_xoffset = machine_config['clip_hole_xoffset']
		self.clip_hole_yoffset = machine_config['clip_hole_yoffset']
		self.tractor_hole_diameter = machine_config['tractor_hole_diameter']
		self.tractor_hole_xoffset = machine_config['tractor_hole_xoffset']
		self.tractor_hole_yoffset = machine_config['tractor_hole_yoffset']
		self.overlapping_rows = machine_config['overlapping_rows']
		self.overlapping_row_xoffset = machine_config['overlapping_row_xoffset']
		self.overlapping_row_yoffset = machine_config['overlapping_row_yoffset']
		self.corner_offset = machine_config['corner_offset']
		self.half_hole_at_bottom = machine_config['half_hole_at_bottom']
		if machine_config['force_solid_fill']:
			self.solid_fill = True
		else:
			self.solid_fill = is_solid_fill

		self.card_rows = rows

		if self.card_rows > 200 or self.card_stitches > machine_config['stitches']:
			raise ValueError(
				"Your pattern seems to exceed 200 rows and/or {} stitches. "
				"Are you sure you uploaded the right text file?".format(machine_config['stitches']))

		self.horz_repeat = horz_repeat
		self.vert_repeat = vert_repeat
		self.is_blank = is_blank

		self.card_height = (self.pattern_hole_yoffset * 2) + (((self.card_rows * self.vert_repeat) - 1) * self.row_height)


class PCGenerator:

	def __init__(self, handler, data, machine_id, vert_repeat, is_blank = False, is_solid_fill = False):

		global machine_config

		self.handler = handler
		with open("data/{}.json".format(machine_id)) as json_config:
			machine_config = json.loads(json_config.read())
		if is_blank:
			self.data = ['x' * machine_config['stitches']]
		else:
			self.data = data.split()
		self.layout = Layout(
			machine_id,
			len(self.data[0]),
			len(self.data),
			machine_config['stitches'] / len(self.data[0]),
			vert_repeat,
			is_blank,
			is_solid_fill)

	def generate(self):

		diagram = self.create_card()

		objects = []
		if (self.layout.overlapping_rows and
				self.layout.overlapping_row_xoffset and
				self.layout.overlapping_row_yoffset):
			self.draw_overlapped_lines(diagram, objects)
		if (self.layout.clip_hole_diameter and
				self.layout.clip_hole_xoffset):
			self.draw_clip_holes(diagram, objects)
		if (self.layout.tractor_hole_diameter and
				self.layout.tractor_hole_xoffset):
			self.draw_tractor_holes(diagram, objects)

		if self.layout.is_blank:
			self.layout.pattern_hole_diameter = .5
		self.draw_pattern(diagram, self.data, objects)

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

		if self.layout.solid_fill:
			fill = 'red'
		else:
			fill = 'white'

		# main body of card
		yoffset = self.layout.pattern_hole_yoffset
		for row_repeat in range(self.layout.vert_repeat):
			for rows in range(self.layout.card_rows):
				xoffset = self.layout.pattern_hole_xoffset
				for stitch_repeat in range(self.layout.horz_repeat):
					for stitches in range(self.layout.card_stitches):
						try:
							if lines[rows][stitches].upper() == 'X':
								objects.append(diagram.circle(
									center=(xoffset, yoffset),
									fill=fill,
									r = (self.layout.pattern_hole_diameter / 2),
									stroke='black',
									stroke_width=.1))
						except IndexError as error:
							msg = (
								"<em>Encountered bad input character row {} stitch {}</em><br><br>"
								"* Make sure you don't have a space or blank where you intended to enter a dash or X.<br>"
								"* Also look for a line that's too short... i.e., a line that only has 23 pattern "
								"characters for a 24-stitch pattern.<br>")
							raise RuntimeError(msg.format(rows+1, stitches+1))
						xoffset += self.layout.stitch_width
				yoffset += self.layout.row_height

	def draw_overlapped_lines(self, diagram, objects):

		# overlapping rows at top
		yoffset = self.layout.overlapping_row_yoffset
		for rows in range(self.layout.overlapping_rows):
			xoffset = self.layout.overlapping_row_xoffset
			for stitch_repeat in range(self.layout.horz_repeat):
				for stitches in range(self.layout.card_stitches):
					objects.append(diagram.circle(
						center=(xoffset, yoffset),
						fill='white',
						r = (self.layout.pattern_hole_diameter / 2),
						stroke='black',
						stroke_width=.1))
					xoffset += self.layout.stitch_width
			yoffset += self.layout.row_height

		# overlapping rows at bottom
		# yoffset = (self.layout.card_height - (self.layout.row_height * self.layout.overlapping_rows)) + (self.layout.row_height / 2)
		yoffset = self.layout.card_height - self.layout.overlapping_row_yoffset
		for rows in range(self.layout.overlapping_rows):
			xoffset = self.layout.overlapping_row_xoffset
			for stitch_repeat in range(self.layout.horz_repeat):
				for stitches in range(self.layout.card_stitches):
					objects.append(diagram.circle(
						center=(xoffset, yoffset),
						fill='white',
						r = (self.layout.pattern_hole_diameter / 2),
						stroke='black',
						stroke_width=.1))
					xoffset += self.layout.stitch_width
			yoffset -= self.layout.row_height

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

		while yoffset <= self.layout.card_height:
			if not self.layout.half_hole_at_bottom:
				break

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
