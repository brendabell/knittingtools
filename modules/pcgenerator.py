import svgwrite

# default values

# number of overlapping blank rows at the top of the card
blank_rows = 2

# width of the side margin in mm
side_margin = 17.0

# height of one row on the card in mm
row_height = 5.0

# width of one stitch on the card in mm
stitch_width = 4.5
#stitch_width = 9.0

# radius of a pattern hole in mm
pattern_hole_radius = 3.5

# radius of a clip hole in mm
clip_hole_radius = 3.0

# radius of a sprocket hole in mm
sprocket_hole_radius = 3.5

# drawing stroke width
stroke_width='.1'

# fill color
fill_color = 'white'

# stroke_color
stroke_color = 'black'

card_width = 0
card_height = 0
card_rows = 0
card_stitches = 0

class PCGenerator:

	def __init__(self, data, cell_height, cell_width, horz_repeat, vert_repeat):
		global row_height
		global stitch_width

		self.data = data.split()
		self.horz_repeat = horz_repeat
		self.vert_repeat = vert_repeat
		row_height = cell_height
		stitch_width = cell_width

	def generate(self):
		global card_rows
		global card_stitches
		global card_width
		global card_height

		card_rows = len(self.data)
		card_stitches = len(self.data[0])
		if card_rows > 200 or card_stitches > 30:
			raise ValueError(
				"Your pattern seems to exceed 200 rows and/or 30 stitches. "
				"Are you sure you uploaded the right text file?")

		card_width = (side_margin * 2) + (card_stitches * self.horz_repeat * stitch_width)
		card_height = ((blank_rows * 2) + (card_rows * self.vert_repeat)) * row_height

		diagram = self.create_card()

		objects = []
		self.draw_pattern(diagram, self.data, objects)
		self.draw_blank_lines(diagram, objects)
		self.draw_clip_holes(diagram, objects)
		self.draw_sprocket_holes(diagram, objects)

		# sort the list to optimize cutting
		sorted_objects = sorted(objects, key=lambda x: (float(x.attribs['cy']), float(x.attribs['cx'])))
		for i in sorted_objects:
			diagram.add(i)

		return diagram.tostring()

	def create_card(self):
		global card_width
		global card_height
		
		diagram = svgwrite.Drawing(
			"punchcard.svg",
			size=(
				'{0}mm'.format(card_width),
				'{0}mm'.format(card_height)),
			viewBox=(
				'0 0 {0} {1}'.format(card_width, card_height)),
			preserveAspectRatio='none')
		
		shape_points = [
			(2, 0),
			(card_width-2, 0),
			(card_width-1, 1),
			(card_width-1, 20),
			(card_width, 22),
			(card_width, card_height-22),
			(card_width-1, card_height-20),
			(card_width-1, card_height-1),
			(card_width-2, card_height),
			(2, card_height),
			(1, card_height-1),
			(1, card_height-20),
			(0, card_height-22),
			(0, 22),
			(1, 20),
			(1, 1)]
		diagram.add(diagram.polygon(
			points=shape_points,
			fill=fill_color,
			stroke=stroke_color,
			stroke_width=stroke_width))
			
		return diagram

	def draw_pattern(self, diagram, lines, objects):
		global card_rows
		global card_stitches
		global fill_color
		global pattern_hole_radius
		global row_color
		global row_height
		global side_margin
		global stitch_width
		global stroke_color
		global stroke_width
		
		# main body of card
		yoffset = 10.0 + (row_height / 2)
		for row_repeat in range(self.vert_repeat):
			for rows in range(card_rows):
				xoffset = side_margin + (stitch_width / 2)
				for stitch_repeat in range(self.horz_repeat):
					for stitches in range(card_stitches):
						if lines[rows][stitches].upper() == 'X':
							objects.append(diagram.circle(
								center=(xoffset, yoffset),
								fill=fill_color,
								r = (pattern_hole_radius / 2),
								stroke=stroke_color,
								stroke_width=stroke_width))
						xoffset += stitch_width
				yoffset += row_height

	def draw_blank_lines(self, diagram, objects):
		global blank_rows
		global card_stitches
		global fill_color
		global pattern_hole_radius
		global row_height
		global side_margin
		global stitch_width
		global stroke_color
		global stroke_width
		
		# blank rows at top
		yoffset = row_height / 2
		for rows in range(blank_rows):
			xoffset = side_margin + (stitch_width / 2)
			for stitch_repeat in range(self.horz_repeat):
				for stitches in range(card_stitches):
					objects.append(diagram.circle(
						center=(xoffset, yoffset),
						fill=fill_color,
						r = (pattern_hole_radius / 2),
						stroke=stroke_color,
						stroke_width=stroke_width))
					xoffset += stitch_width
			yoffset += row_height

		# blank rows at bottom
		yoffset = (card_height - (row_height * blank_rows)) + (row_height / 2)
		for rows in range(blank_rows):
			xoffset = side_margin + (stitch_width / 2)
			for stitch_repeat in range(self.horz_repeat):
				for stitches in range(card_stitches):
					objects.append(diagram.circle(
						center=(xoffset, yoffset),
						fill=fill_color,
						r = (pattern_hole_radius / 2),
						stroke=stroke_color,
						stroke_width=stroke_width))
					xoffset += stitch_width
			yoffset += row_height

	def draw_clip_holes(self, diagram, objects):
		global card_height
		global clip_hole_radius
		global fill_color
		global row_height
		global side_margin
		global stitch_width
		global stroke_color
		global stroke_width
		
		left_xoffset = side_margin + (stitch_width / 2) - 6.0
		right_xoffset = (card_width - side_margin - (stitch_width / 2)) + 6.0
		yoffset = row_height / 2

		while yoffset < card_height:
			# clip holes on left
			objects.append(diagram.circle(
				center=(left_xoffset, yoffset),
				fill=fill_color,
				r = (clip_hole_radius / 2),
				stroke=stroke_color,
				stroke_width=stroke_width))
			# clip holes on right
			objects.append(diagram.circle(
				center=(right_xoffset, yoffset),
				fill=fill_color,
				r = (clip_hole_radius / 2),
				stroke=stroke_color,
				stroke_width=stroke_width))
			yoffset += row_height

	def draw_sprocket_holes(self, diagram, objects):
		
		left_xoffset = 6.5
		right_xoffset = card_width - 6.5
		yoffset = row_height
		for row_repeat in range(self.vert_repeat):
			for rows in range(((card_rows * self.vert_repeat) + (blank_rows * 2)) / 2):
				# sprocket holes on left
				objects.append(diagram.circle(
					center=(left_xoffset, yoffset),
					fill=fill_color,
					r = (sprocket_hole_radius / 2),
					stroke=stroke_color,
					stroke_width=stroke_width))
				# sprocket holes on left
				objects.append(diagram.circle(
					center=(right_xoffset, yoffset),
					fill=fill_color,
					r = (sprocket_hole_radius / 2),
					stroke=stroke_color,
					stroke_width=stroke_width))
				yoffset += (row_height * 2)
