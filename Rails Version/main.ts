/*************************/
//Data Files
/*************************/
var data = {}

/*************************/
//Constants
/*************************/
var rows = 0;
var cols = 0;
const process = require('process');

function isInArray(value, array) {
    return array.hasOwnProperty(value);
}

function intToSeatId(i, j) {
    const character = String.fromCharCode(97 + i);
    return `${character}${j+1}`;
}

function isAvailable(i, j, noOfSeats) {
    for (var foo = 0; foo < noOfSeats; foo++) {
        const colIndex = foo + j;
        if (!isInArray(intToSeatId(i, colIndex), data['seats'])) {
            return false;
        }
        if (data['seats'][intToSeatId(i, colIndex)]['status'] != 'AVAILABLE') {
            return false;
        }
    }
    return true;
}

function closestToTheMiddle(availables) {
    var currentFavorite = [];
    var currentLowestDistance = cols+1;

    for (var i = 0; i < availables.length; i++) {
        const current = availables[i];
        const distFromMiddle = Math.abs(data['venue']['layout']['columns']/2 - current[1]);
        
        if (distFromMiddle < currentLowestDistance) {
            currentFavorite = current;
            currentLowestDistance = distFromMiddle;
        }
    }

    return currentFavorite;
}

function findBestAvailableSeat(noOfSeats) {
    for (var i = 0; i < rows; i++) {
        var availables = [];
        for (var j = 0; j < rows; j++) {
            if (isAvailable(i, j, noOfSeats)) {
                availables.push([i, j]);
            }
        }

        if (availables.length > 0) {
            return closestToTheMiddle(availables);
        }
    }
}

function printBestAvailableSeats(bestAvailableSeat, noOfSeats) {
    var string = "";
    for (var i = 0; i < noOfSeats; i++) {
        if (noOfSeats >= cols/2+0.51) {
            string = string + `${intToSeatId(bestAvailableSeat[0], bestAvailableSeat[1]+i)} `
        }
        else
        {
            string = string + `${intToSeatId(bestAvailableSeat[0], bestAvailableSeat[1]-i)} `
        }
    }

    console.log(string);
}

function main(noOfSeats = 1, movietitle = '') {
    if (movietitle == '') {
        console.log('Error: Please provide movie title');
        return 1; 
    }

    var fs = require('fs');
    data = JSON.parse(fs.readFileSync(`movies/${movietitle}.json`, 'utf8'));

    rows = data['venue']['layout']['rows'];
    cols = data['venue']['layout']['columns'];

    if (noOfSeats > cols) {
        console.log('Error: Number of seats requested exceeds number of seats available in a row');
        return 1;
    }

    const bestAvailableSeat = findBestAvailableSeat(noOfSeats);

    if (bestAvailableSeat == undefined) {
        console.log('Error: Could not find seat. This may be because no appropriate seats are available');
        return 1;
    }

    printBestAvailableSeats(bestAvailableSeat, noOfSeats);
    
    return 0;
}

main(process.argv[2], process.argv[3])