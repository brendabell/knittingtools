# invocation: python -m test.test

from modules.pcgenerator import PCGenerator
import cairosvg

#pattern='--x---\n--xxxx\n-xxxx-\nxxxx--\n---x--\n'
pattern='-x\nx-\n'
#machine = '12-stitch-br-sr'
#machine = '18-stitch-mk70'
#machine = '24-stitch-br-sr'
machine = '40-stitch-deco'
generator = PCGenerator(None, pattern, machine, 10)
result = generator.generate()
text_file = open("{}.svg".format(machine), "w")
text_file.write(result)
text_file.close()
png_file = open("{}.png".format(machine), "w")
cairosvg.svg2png(bytestring=result,write_to=png_file)
png_file.close()
