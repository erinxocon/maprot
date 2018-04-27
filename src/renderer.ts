// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// All of the Node.js APIs are available in this process.
import * as fs from "fs";

import * as csv from "csv-parse";

import * as path from "path";

import { Set } from "typescript-collections";

type ReferencePoints = { [key: string]: number };

const canvasRefPoints: ReferencePoints = {
    Fl1MinLat:42.3342467354753,
    Fl1MinY:3318,
    Fl1MaxLat:42.3348842080961,
    Fl1MaxY:1489,
    Fl1MinLong:-83.0400689277813,
    Fl1MinX:1022,
    Fl1MaxLong:-83.0390648307041,
    Fl1MaxX:3180,
    Fl3MinLat:42.334069717561,
    Fl3MinY:3375,
    Fl3MaxLat:42.3352552805179,
    Fl3MaxY:626,
    Fl3MinLong:-83.0424210422585,
    Fl3MinX:320,
    Fl3MaxLong:-83.0406844346077,
    Fl3MaxX:3239
}


//Convert longitude values to pixels with params from BaseCanvasSize{}
const CalculateBaseXPts = (mapData: any[],currentFloor: string, minLong: number, maxLong: number, minX: number, maxX: number ): any[] => {
	var LongSpan = Math.abs(maxLong - minLong);
	var PxSpan = maxX - minX;
    var LongPerPx = (LongSpan / PxSpan);
	for (var i=0; i<mapData.length; i++) {
		if (currentFloor===mapData[i].Floor) {
			var PtLong = mapData[i].Longitude;
            var DeltaLong = PtLong - minLong;
            var DeltaPx = (DeltaLong / LongPerPx);
			var BaseX = Math.round(DeltaPx + minX);
			mapData[i]["BaseX"]= BaseX;
		}
	}
	return mapData;
}

//Convert latitude values to pixels with params from CanvasRefPoints object
const CalculateBaseYPts = (mapData: any[], currentFloor: string, minLat: number, maxLat: number, minY: number, maxY:number): any[] => {
	var LatSpan = Math.abs(maxLat - minLat);
	var PxSpan = minY - maxY;
    var LatPerPx = (LatSpan/PxSpan);
	for (var i=0; i<mapData.length; i++) {
		if (currentFloor===mapData[i].Floor) {
			var PtLat = mapData[i].Latitude;
            var DeltaLat = PtLat - minLat;
            var DeltaPx = (DeltaLat / LatPerPx);
            //calc reversed for 0,0 at top left
            var BaseY = Math.round(minY - DeltaPx);
            mapData[i]["BaseY"]= BaseY;
        }
    }
	return mapData;
}

const GetFloors = (mapData: any[]) => {
	let floors: Set<string> = new Set<string>();
    mapData.forEach((element) => {
        floors.add(element.Floor);
    });

	return floors.toArray();
}

const ConvertLatLong = (mapData: Array<any>): any[] => {
    const floorList: string[] = GetFloors(mapData);
    console.log(floorList);
    let data: any[];
    floorList.forEach((element, i) => {
        console.log(element);
        const currentFloor: string = element;
        const MinimumLatitude = canvasRefPoints[`Fl${currentFloor}MinLat`];
        const MaximumLatitude = canvasRefPoints[`Fl${currentFloor}MaxLat`];
        const MinimumLongitude = canvasRefPoints[`Fl${currentFloor}MinLong`];
        const MaximumLongitude = canvasRefPoints[`Fl${currentFloor}MaxLong`];
        const MinimumX = canvasRefPoints[`Fl${currentFloor}MinX`];
        const MaximumX = canvasRefPoints[`Fl${currentFloor}MaxX`];
        const MinimumY = canvasRefPoints[`Fl${currentFloor}MinY`];
        const MaximumY = canvasRefPoints[`Fl${currentFloor}MaxY`];
        data = CalculateBaseXPts(mapData, currentFloor, MinimumLongitude, MaximumLongitude, MinimumX, MaximumX);
        data = CalculateBaseYPts(data, currentFloor, MinimumLatitude, MaximumLatitude, MinimumY, MaximumY);
    });

	return data;
}

// Use the writable stream api
const parser: csv.Parser = csv({ delimiter: ",", columns: true }, (err, data) => {
    if (err) {
        throw err
    }
    else {
        console.log(ConvertLatLong(data));
    }
})

fs.createReadStream(path.join(__dirname, "../greektown_Data.csv")).pipe(parser);