# invocation: python -m test.test

from modules.pcgenerator import PCGenerator
import cairosvg

# pattern='--x---\n--xxxx\n-xxxx-\nxxxx--\n---x--\n'
pattern="""------------------------
------------------------
------------------------
------------------------
----X-------------X-X---
---X-X --------X--X-X--X
----X-X---------X-X-X-X-
---X-X-X--------XXXXXXX-
X--XX-X-X-----X-XXXXXXX-
---XXX-X-X-----XXXXXXXXX
---XXXX-X-------XXXXXXX-
---XXXXX-X-------XXXXX--
---X-------X-------X----
--X-------XXX------X----
-X-------XXXXX-----X----
X------X-XXXXX-X---X----
X-----XXXXXXXXXXX--X----
------XXXXXXXXXXX--X---X
------XXXXXXXXXXX---X--X
-----XXXXXXXXXXXXX--X--X
----XXX-XX-X-XX-XXX-X--X
XX--XXXX---X---XXXX--X--
XXX-XXXXXX-X-XXXXXX---XX
-----XXXXX-X-XXXXX------
----XXXXX--X--XXXXX-----
XXXX--XX---X---XX--XXXX-
------------------------
------------------------
------------------------
------------------------
------XXX-XXX-------XXX-
-----XXXX-XXXX-----XXXXX
---XX-XXX-XXX-XX---XXXXX
--XXXX-XXXXX-XXXX---XXX-
-XXXXXX-XXX-XXXXXX--XXX-
XXXXXXXX-X-XXXXXXXX--X--
-------X-X-X---------X--
--------XXX----------X--
--XX-----XX----------X--
--XXX----XX---------X--X
--XXXX---X------XX--XXX-
---XXXX--X-----XXX-X----
---XXXX--X----XXXX-X---X
----XXXX-X---XXXX--XXX--
-----XXX--X-XXXXX-X---X-
-------XX-X-XXXX--X---X-
---------XXX------X-----
--------X--X-----X------
----XXXX----X---X-------
---XXXXX-----XXXXXXXXXX-
--XXXXXX----X----XXXXXXX
--XXXXX-----X-----XXXXXX
--XXXX-------XX-----XXXX
X-XXX----------XX----XXX
"""
#pattern='xxxxx'
# machine = '12-stitch-br-sr'
# machine = '18-stitch-mk70'
machine = '24-stitch-br-sr'
# machine = '30-stitch-km'
# machine = '40-stitch-deco'
# machine = '40-stitch-jac-4_5'
# machine = '40-stitch-jac-5_08'
# machine = '40-stitch-jac-5_0'
# machine = '60-stitch-ec1'
# generator = PCGenerator(None, pattern, machine, 20, True)
generator = PCGenerator(None, pattern, machine, 20, False, True)
result = generator.generate()
text_file = open("{}.svg".format(machine), "w")
text_file.write(result)
text_file.close()
png_file = open("{}.png".format(machine), "w")
cairosvg.svg2png(bytestring=result,write_to=png_file)
png_file.close()
