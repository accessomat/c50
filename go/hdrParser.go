package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"os"
)

func usage() {
	fmt.Println("usage: hdrParser -i [inputfile]")
	flag.PrintDefaults()
	os.Exit(2)
}

func main() {
	var (
		input *string = flag.String("i", "C50_DB_EUK_V2092.HDR", "Input file")
	)
	fmt.Println("HDR file parser")
	flag.Usage = usage
	flag.Parse()

	inBuffer, err := ioutil.ReadFile(*input)
	if err != nil {
		panic(err)
	}

	hdrInstance := NewHdrFromBuffer(inBuffer)

	db := hdrInstance.generateDb()

	db.filterUnparsed()
}
