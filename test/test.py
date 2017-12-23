# invocation: python -m test.test

from modules.pcgenerator import PCGenerator
import cairosvg

pattern='--x---\n--xxxx\n-xxxx-\nxxxx--\n---x--\n'
#pattern='xxxxx'
# machine = '12-stitch-br-sr'
# machine = '18-stitch-mk70'
# machine = '24-stitch-br-sr'
# machine = '30-stitch-km'
# machine = '40-stitch-deco'
# machine = '40-stitch-jac-4_5'
machine = '40-stitch-jac-5_08'
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
