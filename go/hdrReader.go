package main

import (
	"bytes"
	"encoding/binary"
	"fmt"
)

type hdrReader struct {
	*bytes.Reader // Anonymous fields are awesome
}

func NewHdrReader(buffer []byte) hdrReader{
	return hdrReader{Reader: bytes.NewReader(buffer)}
}

func (hr *hdrReader) ReadPacket() []byte {
	var packet []byte = make([]byte, 7)
	hr.Reader.Read(packet)
	return packet
}

func (hr *hdrReader) ReadInt8() (ret int8) {
	binary.Read(hr.Reader, binary.LittleEndian, &ret)
	return
}

func (hr *hdrReader) ReadInt16() (ret int16) {
	binary.Read(hr.Reader, binary.LittleEndian, &ret)
	return 
}

func (hr *hdrReader) ReadInt32() (ret int32) {
	binary.Read(hr.Reader, binary.LittleEndian, &ret)
	return
}

func (hr *hdrReader) ReadTude() string {
	var tmp int32 = hr.ReadInt32()
	var ret string = fmt.Sprintf("%d", tmp)
	if tmp > 0 {
		ret = fmt.Sprintf("%s.%s", ret[:2], ret[2:])
	}
	// TODO: else return an error
	return ret
}

func (hr *hdrReader) ReadAll() []byte {
	var unread []byte = make([]byte, hr.Reader.Len())
	hr.Reader.Read(unread);
	return unread;
}

func (hr *hdrReader) ReadHexRecord() hexRecord {
	enum := hr.ReadInt16()
	azim1 := hr.ReadInt8() * 2
	azim2 := hr.ReadInt8() * 2
	lat := hr.ReadTude()
	lon := hr.ReadTude()
	unk := hr.ReadInt32()

	return hexRecord{enum: enum, azim1: azim1, azim2: azim2, Lat: lat, Lon: lon, unk: unk}
}

func (hr *hdrReader) ReadBRecord() bRecord {
	return bRecord{
		enum: hr.ReadInt16(), 
		azim: hr.ReadInt8() * 2, 
		Lat: hr.ReadTude(), 
		Lon: hr.ReadTude()}
}
