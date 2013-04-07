package main

type hdrDb struct {
	version    int16
	unknown1   int16
	hexRecords int32
	bRecords   int32
}

func (db *hdrDb) getVersion() int16 {
	return db.version
}

func (*hdrDb) filterUnparsed() {
	// TODO implement filter
	//for 
}

type hexRecord struct {
	unk          int32
	enum         int16
	azim1, azim2 int8
	Lat, Lon     string
}

type bRecord struct {
	enum     int16
	Lat, Lon string
	azim     int8
}


