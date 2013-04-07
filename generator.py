import argparse
import operator
import struct

#1337
hdr_version = "\x39\x05"

speed_translate_table = {
				5 : 0x01, 
				10: 0x02,
				20: 0x04,
				40: 0x08,
				80: 0x10,
			}

class entry():
	def __init__(self, lat, lon, azimut, typestr, speed):
		self.lat = lat
		self.lon = lon
		self.azimut = azimut
		self.typestr = typestr
		self.speed = speed

	def __str__(self):
		return "(%s,%s) -> %s :: %s >> %s"%(self.lat, self.lon, self.azimut, self.typestr, self.speed)

	def toBin(self):
		retval = ""
		lon = int(self.lon[:2] + self.lon[3:])
		lat = int(self.lat[:2] + self.lat[3:])
		#print "%s --> %d"%(self.lon, lon)

		calcSpeedBitFlag = 0x00
		calcSpeed = int(self.speed)

		speeds = speed_translate_table.keys()
		speeds.sort()
		speeds.reverse()
		for s in speeds:
			if calcSpeed >= s:
				calcSpeedBitFlag |= speed_translate_table[s]
				calcSpeed -= s
		#print "self.speed = (%s) calcSpeedEnum = (%s)"%(self.speed,hex(calcSpeedBitFlag))
		definition_translation_table = {"GatsoRed":(0x00, 0x60), "SpeedRedCam":(0x00,0x60), "FixSpeedCam":(0x00,0x50), "SpeedCam":(0x00, 0x50)}
		if self.typestr in definition_translation_table.keys():
			retval += chr(definition_translation_table[self.typestr][0] | calcSpeedBitFlag)
			retval += chr(definition_translation_table[self.typestr][1])
			retval += struct.pack("B", (int(self.azimut) / 2) + 1)
			retval += struct.pack("II", lon, lat)
			return retval
		else: 
			print self.typestr
			return ""	

def generateEntries(lines):
	entries = []
	print "file"
	for line in lines[1:]:
		print ""
		#print ">> line >> " + line
		line = line.split(',')
		e = entry(line[2],line[1],line[6],line[7],line[4])
		#print str(e)
		entries.append(e)
		if int(line[5]) == 2:
			e = entry(line[2],line[1],str((int(line[6])+180) % 360),line[7],line[4])
			entries.append(e)

	return entries


def main():
	parser = argparse.ArgumentParser(description='Generate hdr file')
	parser.add_argument('-i', default="GatsoCam30_12_12_csv.csv", dest='input')
	parser.add_argument('-o', default="output.hdr", dest='output')

	args = parser.parse_args()

	print "input: " + args.input
	print "output: " + args.output

	lines = open(args.input,"r").readlines()

	entries = generateEntries(lines)


	entries.sort(key=operator.attrgetter('lat'))
	for e in entries:
		print "== " + str(e)

	hdr_header = b"\x24\x01\x02\x00\x00\x10\x00" #packet magic

	payload_size = 0x14 + 0x10 + (0xa * len(entries))
	payload_percent = payload_size / 64


	hdr_header += struct.pack("II",payload_size, payload_percent)
	hdr_header += "\x00" * 0x3f1

	hdr_header += hdr_version

	hdr_const = "\x00\x01"
	hdr_header += hdr_const

	hdr_header += struct.pack("I",1) # number of hex entries
	hdr_header += struct.pack("I",len(entries)) # number of b entries
	hdr_header += "\x16\x80\x1A\x00\x2C\x00\x46\x00"
	hdr_header += "\x00" * 0x10


	hdr_header += "\x14\x50\x7F\x38\xBA\x17\x80\x9C\x61\x2A\x00"

	for e in entries:
		hdr_header += e.toBin()
	open(args.output,"wb").write(hdr_header)

main()
