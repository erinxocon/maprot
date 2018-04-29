import * as tempy from "tempy";

// Converts from radians to degrees.
Math.toDegrees = function(radians: number): number {
    return radians * 180 / Math.PI;
};