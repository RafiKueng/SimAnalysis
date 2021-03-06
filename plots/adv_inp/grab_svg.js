/*
 * Some function schnipplets that extract the working canvas
 *
 * intended to be run directly in the browser,
 * using the debug console
 */


//extracts svg
(function(){
    $("svg").attr({xmlns:"http://www.w3.org/2000/svg"});
    var b64 = btoa($("svg").parent().html());
    var link = "<a href-lang='image/svg+xml' href='data:image/svg+xml;base64,\n"+b64+"' download='file.svg'>KLICK</a>";
    $("<div>"+link+"</div>").dialog();
})();



    
mids = "
6915
6919
6937
6941
6975
6990
7022
7025    
"    
    
    
//extracts png 
(function(){

    console.log("in fn");

    var $parent = $('<div style="width:2048px;height:2048px;position:absolute;top:0;left:0;zindex:0;"></div>');

    var canvas = document.createElement('canvas');
    canvas.width = 2048;
    canvas.height = 2048;
    canvas.style.width  = '2048px';
    canvas.style.height = '2048px';

    //var f = 2; //scale factor for line widths ect..

    // new element sizes
    var scale = LMT.settings.display.zoompan.scale;
    var mapescales = {6915: 0.632, 6919: 1.642, 7022: 0.9865, 7025: 1.112, 6990: 1.3635, 6937: 1.1265, 6941: 0.9645, 6975: 2.145}; // derrived scaling factors from map extent (0.2 is default = fact 1)
    // using scales.py with:  {key: round(value/0.2, 6) for (key, value) in sc2.items()}
    
    var f = 0.20; // general relative scaling factor for points / contours
    
    //get total scale
    //var tsc = mapescales[LMT.GET.rid] / scale * f;
    var tsc = mapescales[LMT.GET.rid] * f;
    
    var cpnt = 4 * tsc ;
    var epnt = 7 * tsc;
    var line = 3 * tsc;
    
    $(".contourpath").each(function(){
        $(this).attr({"stroke-width": String(line)});
    });

    $(".contourpoint").each(function(){
        $(this).attr({"r": String(cpnt)});
    });
    
    $(".extremalpoint").each(function(){
        $(this).attr({"r": String(epnt)});
    });    
  
    // first add css to the svg!!
    // make a clone and add css to the clone
    //  http://code.google.com/p/canvg/issues/detail?id=143
    var clonedSVG = svg.root.cloneNode(true);

    var style = document.createElementNS(svg.ns, "style");

    //style.textContent += "<![CDATA[\n";
  
    //get stylesheet for svg
    for (var i=0;i<document.styleSheets.length; i++) {
    str = document.styleSheets[i].href;
    if (str.indexOf('lmt.v')>-1 || str.indexOf('lmt.90.')>-1){
        var rules = document.styleSheets[i].cssRules;
        for (var j=0; j<rules.length;j++){
            style.textContent += (rules[j].cssText + "\n");
            }
        break;
        }
    }
  
    //style.textContent += "]]>";

    clonedSVG.getElementsByTagName("defs")[0].appendChild(style);
    canvg(canvas, (new XMLSerializer()).serializeToString(clonedSVG), { ignoreMouse: true, ignoreAnimation: true });
    clonedSVG = null;

    // add elements to dom, so canvas gets drawn
    $parent.append(canvas);
    $('body').append($parent);

    $parent.css({'visibility': 'hidden'});

    svg.canvasout = canvas;
    svg.canvasoutprnt = $parent;
    
    // wait for the redraw to happen
    setTimeout(function(){
        var canvas = LMT.ui.svg.canvasout;
        var img = canvas.toDataURL();
        var scale = LMT.settings.display.zoompan.scale;
        var fname = LMT.GET.rid + "_" + scale +".png";
        
        var link = "<a href-lang='image/svg+xml' href='"+ img +"' download='"+ fname + "'>KLICK</a>";
       
        $("<div>"+link+"</div>").dialog();

    }, 200);
})();

























