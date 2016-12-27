from pcgenerator import PCGenerator
pattern='-x--\n-xxx\nxxx-\n--x-\n'
machine = '12-stitch-br-sr'
#machine = '24-stitch-br-sr'
#machine = '40-stitch-deco'
generator = PCGenerator(None, pattern, machine, 10)
result = generator.generate()
text_file = open("{}.svg".format(machine), "w")
text_file.write(result)
text_file.close()