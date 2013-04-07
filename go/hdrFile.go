package main

import (
	"encoding/hex"
	"fmt"
)

type hdr struct {
	basePacket []byte
	packetSize int32
	packet     []byte
}

func (hr *hdr) generateDb() *hdrDb {
	var (
		i int32
	)
	fmt.Println(" = /> \n === Parsing DB === ")
	reader := NewHdrReader(hr.packet)
	version := reader.ReadInt16()
	fmt.Printf(" = DB version : %d (0x%x)\n", version, version)
	unknown1 := reader.ReadInt16()
	fmt.Printf(" = DB unknown1 : %d (0x%x)\n", unknown1, unknown1)
	hexRecordsLen := reader.ReadInt32()
	fmt.Printf(" = DB number of 0x10 records : %d (0x%x)\n", hexRecordsLen, hexRecordsLen)
	bRecordsLen := reader.ReadInt32()
	fmt.Printf(" = DB number of 0x0b records : %d (0x%x)\n", bRecordsLen, bRecordsLen)
	unknown2 := reader.ReadInt32()
	fmt.Printf(" = DB unknown2 : %d (0x%x)\n", unknown2, unknown2)
	unknown3 := reader.ReadInt32()
	fmt.Printf(" = DB unknown3 : %d (0x%x)\n", unknown3, unknown3)
	fmt.Printf(" = |    |=>\n")
	hexRecords := make([]hexRecord, hexRecordsLen)
	for i = 0; i < hexRecordsLen; i++ {
		hr := reader.ReadHexRecord()
		hexRecords[i] = hr
		fmt.Printf("   |0x10|= <%s, %s>\n", hr.Lat, hr.Lon)
	}
	bRecords := make([]bRecord, bRecordsLen)
	for i = 0; i < bRecordsLen; i++ {
		br := reader.ReadBRecord()
		bRecords[i] = br
		fmt.Printf("   |0x0B|= <%s, %s>\n", br.Lat, br.Lon)
	}
	return &hdrDb{version: version, unknown1: unknown1, hexRecords: hexRecordsLen, bRecords: bRecordsLen}
}

func NewHdrFromBuffer(buf []byte) *hdr {
	fmt.Println(" === Parsing HDR header === ")
	reader := NewHdrReader(buf)

	basePacket := reader.ReadPacket()
	fmt.Printf(" = HDR packet type: %s\n", hex.EncodeToString(basePacket))
	packetSize := reader.ReadInt32()
	fmt.Printf(" = HDR packet size: %x (%d)\n", packetSize, packetSize)
	packetSizeHundredth := reader.ReadInt32()
	fmt.Printf(" = HDR packet hundredth: %x (%d * 64 = %d ~ %d)\n", packetSizeHundredth, packetSizeHundredth, packetSizeHundredth*64, packetSize)
	reader.Seek(0x400, 0)

	retval := hdr{basePacket: basePacket, packetSize: packetSize, packet: reader.ReadAll()}
	return &retval
}


