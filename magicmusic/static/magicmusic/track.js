var numOfRows = 88;
var highestKey = 108;
var numofNotes = 0; //numofnotes on page;


function initCanvasTable() {
    var initialColumns = 200;

    // add table header
    for (var i = highestKey; i > highestKey - numOfRows; i--) {
        var thName = getThName(i);
        $('#working-table').append($('<tr>')
            .append($('<th>')
                .attr('class', 'border')
                .text(getThDisplayName(i)))
            .attr('class', 'border')
            .attr('id', thName)
        );
    }
    addColumns(initialColumns);

    // should be move to another listener
    // var parser = require('note-parser');
    // console.log(parser.build(parser.midi('60')));

}

function addNode(row, column) {


}

function addColumns(numOfColumns) {
    for (var i = highestKey; i > highestKey - numOfRows; i--) {
        // add num of columns to the row
        var thName = getThName(i);
        for (var j = 0; j < numOfColumns; j++) {
            $('#' + thName).append($('<td>').attr('class', 'border').attr('id', thName + '-' + j));
        }
    }
}

function getThDisplayName(i) {
    return miditopitch(i);
}

function getThName(i) {
    return miditopitch(i).replace('#','Sharp');
}

function setClickactions() {
    $('td').mousedown(function (e) {
        var tdid = e.target.id;
        // should parse tdid to get the desired postion
        var offset = tdid.split("-")[1];
        var trid = $('#' + tdid).parent().attr('id');

        var leftMargin = $('#' + trid).find('th').outerWidth();
        var cellWidth = $('#' + tdid).outerWidth();
        var cellHeight = $('#' + tdid).outerHeight();
        var dataX = offset * cellWidth;

        // append a new drag
        $('#' + trid).append($('<td>')
            .append($('<div>')
                .attr('class', 'resize-drag')
                .attr('data-x', dataX)
                .attr('id', 'note-' + numOfRows))
            .attr('class', 'overlay resize-container'));

        // recalibrate the left margin
        $('.overlay').css('left', leftMargin)
            .css('width', cellWidth)
            .css('height', cellHeight);


        // trigger interact.js event
        var drag_object = document.getElementById('note-' + numOfRows);
        drag_object.style.webkitTransform = drag_object.style.transform =
            'translate(' + dataX + 'px, ' + 0 + 'px)';

        // keep this at last! we are count the number of notes and naming them
        numOfRows++;
    });

    // $('.resize-drag').contextmenu(function (event) {
    //     alert("right click");
    // });

}


// init a timestamp marking newest posts and comments
$(document).ready(function () {
    initCanvasTable();
    setClickactions();
});


function miditopitch(mididata) {
    var midinotes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
    //document.getElementById("midi").innerHTML = 1;
    midinote = midinotes[mididata % 12];
    midioctave = Math.floor(mididata / 12) - 1;
    var midipitch = midinote.toString() + midioctave.toString();
    return midipitch;
    // document.getElementById("midi").innerHTML = midipitch;
}

function pitchtooctave(pitchdata) {
    var pitchnotes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
    // document.getElementById("pitch").innerHTML = pitchnotes;
    var len = pitchdata.length - 2;
    // document.getElementById("pitch").innerHTML = len;
    switch (pitchdata.charAt(0)) {
        case 'C':
            pitchnote = len;
            break;
        case 'D':
            pitchnote = 2 + len;
            break;
        case 'E':
            pitchnote = 4;
            break;
        case 'F':
            pitchnote = 5 + len;
            break;
        case 'G':
            pitchnote = 7 + len;
            break;
        case 'A':
            pitchnote = 9 + len;
            break;
        case 'B':
            pitchnote = 11;
    }
    // document.getElementById("pitch").innerHTML = pitchnote;
    pitchoctave = pitchdata.charCodeAt(len + 1) - 47;
    // document.getElementById("pitch").innerHTML = pitchoctave;
    var pitchmidi = pitchoctave * 12 + pitchnote;
    return pitchmidi;
    // document.getElementById("pitch").innerHTML = pitchmidi;
}


function escapeSharp(input) {
    return input.replace('#', '\\#');
}


// from interact.js
interact('.resize-drag')
    .draggable({
        onmove: window.dragMoveListener,
        restrict: {
            restriction: 'parent',
            elementRect: {top: 0, left: 0, bottom: 1, right: 1}
        },
    })
    .resizable({
        // resize from all edges and corners
        edges: {left: true, right: true, bottom: false, top: false},

        // keep the edges inside the parent
        restrictEdges: {
            outer: 'self',
            endOnly: true,
        },

        // minimum size
        restrictSize: {
            min: {width: 5, height: 45},
        },

        inertia: true,
    })
    .on('resizemove', function (event) {
        var target = event.target,
            x = (parseFloat(target.getAttribute('data-x')) || 0),
            y = (parseFloat(target.getAttribute('data-y')) || 0);

        // update the element's style
        target.style.width = event.rect.width + 'px';
        target.style.height = event.rect.height + 'px';

        // translate when resizing from top or left edges
        x += event.deltaRect.left;
        y += event.deltaRect.top;

        target.style.webkitTransform = target.style.transform =
            'translate(' + x + 'px,' + y + 'px)';

        target.setAttribute('data-x', x);
        target.setAttribute('data-y', y);
        target.textContent = Math.round(event.rect.width) + '\u00D7' + Math.round(event.rect.height);
    });