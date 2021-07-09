import codecs, sys
try:
  fromenc, toenc, fromfile, tofile = sys.argv[1:5]
except:
  print "Usage:\n  recode.py fromenc toenc fromfile tofile"
  sys.exit(0)

inp = codecs.open(fromfile, "rb", fromenc)
outp = codecs.open(tofile, "wb", toenc)
outp.write(inp.read())

