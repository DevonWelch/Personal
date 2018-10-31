/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

var app = {

    // Application Constructor
    initialize: function() {
        this.bindEvents();
        //connect to server
        //ip: 54.213.88.10

        //load returned json into array
    },
    // Bind Event Listeners
    //
    // Bind any events that are required on startup. Common events are:
    // 'load', 'deviceready', 'offline', and 'online'.
    bindEvents: function() {
        //document.addEventListener('deviceready', this.onDeviceReady, false);
        $(document).ready(this.onDeviceReady());
    },
    // deviceready Event Handler
    //
    // The scope of 'this' is the event. In order to call the 'receivedEvent'
    // function, we must explicitly call 'app.receivedEvent(...);'
    onDeviceReady: function() {

        /*localStorage['admobid'] = {};
        if( /(android)/i.test(navigator.userAgent) ) { // for android & amazon-fireos
            localStorage['admobid'] = {
                banner: 'ca-app-pub-4128736147147651/5241761323', // or DFP format "/6253334/dfp_example_ad"
                interstitial: 'ca-app-pub-xxx/yyy'
            };
        } else if(/(ipod|iphone|ipad)/i.test(navigator.userAgent)) { // for ios
            localStorage['admobid'] = {
                banner: 'ca-app-pub-4128736147147651/5241761323', // or DFP format "/6253334/dfp_example_ad"
                interstitial: 'ca-app-pub-xxx/kkk'
            };
        } else { // for windows phone
            localStorage['admobid'] = {
                banner: 'ca-app-pub-4128736147147651/5241761323', // or DFP format "/6253334/dfp_example_ad"
                interstitial: 'ca-app-pub-xxx/kkk'
            };
        }

        if(window.AdMob) window.AdMob.createBanner( {
            adId: localStorage['admobid'].banner, 
            position: window.AdMob.AD_POSITION.BOTTOM_CENTER, 
            autoShow: true } );*/

        localStorage['docs'] = ''
        //$.post("http://knowvia-dev.us-west-2.elasticbeanstalk.com/docs", {}, function(ret) {
        $.post("http://localhost:9200/docs", {}, function(ret) {
            //var form = $("#docs-form");
            for (i=0; i < ret.length; i ++) {
                $("#docs-form").append('<input type="checkbox" name="' + ret[i] + '" checked id="' + ret[i] + '"> ' + ret[i] + '</input>');
                localStorage['docs'] += ret[i] + ',';
            }
            localStorage['docs'] = localStorage['docs'].slice(0,-1);
            $("#docs-form").append('<input type="submit" value="Save">');
        });

        //console.log('test');
        //$("#test-img").attr("src", 'img/my-navigate.png');
        var options = { timeout: 30000, enableHighAccuracy: true };
        watchID = navigator.geolocation.watchPosition(this.onLocationSuccess, this.onError, options);
        var map = document.getElementById('googleMap');
        $( ".selector" ).pagecontainer({
            defaults: true
        });

        var PIXEL_RATIO = (function () {
            var ctx = $("#mainCanvas").get(0).getContext("2d"),
                dpr = window.devicePixelRatio || 1,
                bsr = ctx.webkitBackingStorePixelRatio ||
                      ctx.mozBackingStorePixelRatio ||
                      ctx.msBackingStorePixelRatio ||
                      ctx.oBackingStorePixelRatio ||
                      ctx.backingStorePixelRatio || 1;

            return dpr / bsr;
        })();

        createHiDPICanvas = function(w, h, ratio) {
            if (!ratio) { ratio = PIXEL_RATIO; }
            var can = $("#mainCanvas").get(0);
            can.width = w * ratio;
            can.height = h * ratio;
            can.style.width = w + "px";
            can.style.height = h + "px";
            can.getContext("2d").setTransform(ratio, 0, 0, ratio, 0, 0);
            can.getContext("2d").scale(1/window.devicePixelRatio,1/window.devicePixelRatio);
            return can;
        }
        can = createHiDPICanvas(Math.min(window.innerWidth, window.innerHeight), Math.min(window.innerWidth, window.innerHeight));
        c = can.getContext("2d");
        //c.moveTo(can.width/2, can.height/2 + 50);
        c.moveTo(can.width/2, can.height/2);
        c.beginPath();
        c.strokeStyle = "red";
        var a = 1;
        var b = 1;
        //c.arc(can.width/2, can.height/2, 50, 0, Math.PI*2);
        for (i = 0; i < 720; i++) {
            angle = 0.1 * i;
            x = can.width/2 + (a + b * angle) * Math.cos(angle);
            y = can.height/2 + (a + b * angle) * Math.sin(angle);
            c.lineTo(x, y);
        }
        c.stroke();
        //map.style="width:" + window.innerWidth.toString() + "px;height:" + window.innerHeight.toString() - 30 + "px;"
        //var stng_btn = document.getElementById("settings-button");
        //stng_btn.left = window.innerWidth - 10;
        //var watch = document.getElementById('wid');
        //watch.innerHTML = watchID;
        app.receivedEvent('deviceready');
    },

    onLocationSuccess: function(position) {
        /*var lat = document.getElementById('lat');
        var lon = document.getElementById('lon');
        var hdng = document.getElementById('hdng');

        lat.innerHTML = positions.coords.latitude;
        lon.innerHTML = positions.coords.longitude;
        hdng.innerHTML = positions.coords.heading;*/

        console.log(position.coords);

        lat = position.coords.latitude;
        lon = position.coords.longitude;
        hdng = position.coords.heading;
        spd = position.coords.speed;

        var watch = document.getElementById('wid1');
        watch.innerHTML = lat.toString() + ', ' + lon.toString();
        //var watch2 = document.getElementById('wid2');
        //watch2.innerHTML = hdng.toString() + ', ' + spd.toString();
        localStorage.setItem('lat', lat);
        localStorage.setItem('lon', lon);
        localStorage.setItem('hdng', hdng);
        localStorage.setItem('spd', spd);

        //don't need to store it, can just do teh call right here

        //after call, update the canvas form here, too.

        //shoudl keep an array of teh current points in memory,
        //and when the returned array is different that's when
        //it is known that an arrow should be added and/or removed

        //use heading to know how much to rotate the canvas
        var x = 1;
    },

    // Show an alert if there is a problem getting the geolocation
    //
    onError: function(error) {
        alert('code: '    + error.code    + '\n' +
              'message: ' + error.message + '\n');
    },


    // Update DOM on a Received Event
    receivedEvent: function(id) {
        //var parentElement = document.getElementById(id);
        //var listeningElement = parentElement.querySelector('.listening');
        //var receivedElement = parentElement.querySelector('.received');

        //listeningElement.setAttribute('style', 'display:none;');
        //receivedElement.setAttribute('style', 'display:block;');

        //$(".app").css("background", "");

        //initialize canvas
        //change background image to none

        //arrows: ../img/512/navigate.png OR arrow-up-a.png

        //centre: ../img/512/happy.png OR earth.png

        //display arrows with text pointing to nearby things

        //start navigator.geolocation.watchPosition

        console.log('Received Event: ' + id);
    }
};

function wrap_text(text, t_or_b, x, y, orig_x, orig_y, ctx, text_size, j) {
    //console.log(ctx.canvas.width);
    text = text.trim();
    var w;
    var h;
    if (j != 'n') {
        var boundaries;
        var justify;
        ctx.translate(-orig_x, 0);
        if (t_or_b == 't') {
            console.log(text);
            index = text.indexOf(' ', 0);
            if (index == -1) {
                second_text = '';
                first_text = text;
            } else {
                first_text = text.slice(0, index);
                second_text = text.slice(index + 1);
            }
            if (j == 'l') {
                ctx.fillText(first_text, 5, y);
                ctx.translate(orig_x, 0);
                if (second_text != "") {
                    var [boundaries, justify] = wrap_text(second_text, 't', x, y + text_size, orig_x, orig_y, ctx, text_size, 'l');
                    if (5 + ctx.measureText(first_text)['width'] > boundaries['r']) {
                        boundaries['r'] = 5 + ctx.measureText(first_text)['width'];
                    }
                } else {
                    boundaries = {'l': 5, 't': orig_y + y - text_size, 'r': 5 + ctx.measureText(first_text)['width'], 'b': orig_y + y};
                    justify = "l";
                }
            } else {
                ctx.fillText(first_text, ctx.canvas.width - 5, y);
                ctx.translate(orig_x, 0);
                if (second_text != "") {
                    var [boundaries, justify] = wrap_text(second_text, 't', x, y + text_size, orig_x, orig_y, ctx, text_size, 'r');
                    if ((ctx.canvas.width - 5) - ctx.measureText(first_text)['width'] < boundaries['l']) {
                        boundaries['l'] = (ctx.canvas.width - 5) - ctx.measureText(first_text)['width'];
                    }
                } else {
                    boundaries = {'l': (ctx.canvas.width - 5) - ctx.measureText(first_text)['width'], 't': orig_y + y - text_size, 'r': ctx.canvas.width - 5, 'b': orig_y + y};
                    justify = "r";
                }
            }
        } else {
            index = text.lastIndexOf(' ', text.length-1);
            if (index == -1) {
                first_text = '';
                second_text = text;
            } else {
                first_text = text.slice(0, index);
                second_text = text.slice(index + 1);
            }
            if (j == 'l') {
                ctx.fillText(second_text, 5, y);
                ctx.translate(orig_x, 0);
                if (first_text != "") {
                    var [boundaries, justify] = wrap_text(first_text, 'b', x, y - text_size, orig_x, orig_y, ctx, text_size, 'l');
                    if (5 + ctx.measureText(second_text)['width'] > boundaries['r']) {
                        boundaries['r'] = 5 + ctx.measureText(second_text)['width'];
                    }
                } else {
                    boundaries = {'l': 5, 't': orig_y + y - text_size, 'r': 5 + ctx.measureText(second_text)['width'], 'b': orig_y + y};
                    justify = "l";
                }
            } else {
                ctx.fillText(second_text, ctx.canvas.width - 5, y);
                ctx.translate(orig_x, 0);
                if (first_text != "") {
                    var [boundaries, justify] = wrap_text(first_text, 'b', x, y - text_size, orig_x, orig_y, ctx, text_size, 'r');
                    if ((ctx.canvas.width - 5) - ctx.measureText(second_text)['width'] < boundaries['l']) {
                        boundaries['l'] = (ctx.canvas.width - 5) - ctx.measureText(second_text)['width'];
                    }
                } else {
                    boundaries = {'l': (ctx.canvas.width - 5) - ctx.measureText(second_text)['width'], 't': orig_y + y - text_size, 'r': ctx.canvas.width - 5, 'b': orig_y + y};
                    justify = "r";
                }
            }
        }
        return [boundaries, justify];
    }
    if ((ctx.measureText(text)['width']/2 <= ctx.canvas.width - orig_x) && (ctx.measureText(text)['width']/2 <= orig_x)) {
        ctx.fillText(text, x, y);
        return [{'l': orig_x - ctx.measureText(text)['width']/2, 't': orig_y + y - text_size, 'r': orig_x + ctx.measureText(text)['width']/2, 'b': orig_y + y}, 'n'];
    } else {
        //console.log(orig_x);
        if (t_or_b == 't') {
            var small = false;
            var prev_index = text.length - 1;
            var first_text;
            var second_text;
            var justify = 'n';
            while (!small && prev_index != -1) {
                //console.log(prev_index);
                //console.log(small);
                //console.log(text);
                //console.log(first_text);
                //console.log(ctx.measureText(first_text)['width']);
                //console.log(ctx.canvas.width - orig_x);
                //console.log(orig_x);
                prev_index = text.lastIndexOf(' ', prev_index-1);
                first_text = text.slice(0, prev_index);
                second_text = text.slice(prev_index + 1);
                if ((ctx.measureText(first_text)['width']/2 <= ctx.canvas.width - orig_x) && (ctx.measureText(first_text)['width']/2 <= orig_x) && (prev_index != -1)) {
                    //console.log('here');
                    small = true;
                    var [boundaries, justify] = wrap_text(second_text, 't', x, y + text_size, orig_x, orig_y, ctx, text_size, 'n');
                    if (justify == 'l') {
                        ctx.translate(-orig_x, 0);
                        ctx.fillText(first_text, 5, y);
                        ctx.translate(orig_x, 0);
                        if (5 + ctx.measureText(first_text)['width'] > boundaries['r']) {
                            boundaries['r'] = 5 + ctx.measureText(first_text)['width'];
                        }
                    } else if (justify == 'r') {
                        ctx.translate(-orig_x, 0);
                        ctx.fillText(first_text, ctx.canvas.width - 5, y);
                        ctx.translate(orig_x, 0);
                        if (ctx.canvas.width - 5 - ctx.measureText(first_text)['width'] < boundaries['l']) {
                            boundaries['l'] = ctx.canvas.width - 5 - ctx.measureText(first_text)['width'];
                        }
                    } else {
                        if (orig_x - ctx.measureText(first_text)['width']/2 < boundaries['l']) {
                            boundaries['l'] = orig_x - ctx.measureText(first_text)['width']/2;
                            boundaries['r'] = orig_x + ctx.measureText(first_text)['width']/2;
                        }
                        ctx.fillText(first_text, x, y);
                    }
                    boundaries['t'] = orig_y + y - text_size;
                    return [boundaries, justify];
                }
            }
            if (prev_index == -1) {
                
                var justify;
                var boundaries;
                //index = text.lastIndexOf(' ', text.length-1);
                index = text.indexOf(' ', 0);
                if (index == -1) {
                    second_text = '';
                    first_text = text;
                } else {
                    first_text = text.slice(0, index);
                    second_text = text.slice(index + 1);
                }
                ctx.translate(-orig_x, 0);
                if (ctx.measureText(first_text)['width']/2 > orig_x) {
                    ctx.textAlign = "start";
                    //ctx.fillText(second_text, ctx.measureText(first_text)['width']/2 - (ctx.canvas.width/2 - orig_x), y);
                    ctx.fillText(first_text, 5, y);
                    ctx.translate(orig_x, 0);
                    if (second_text != "") {
                        var [boundaries, justify] = wrap_text(second_text, 't', x, y + text_size, orig_x, orig_y, ctx, text_size, 'l');
                        if (5 + ctx.measureText(first_text)['width'] > boundaries['r']) {
                            boundaries['r'] = 5 + ctx.measureText(first_text)['width'];
                        }
                    } else {
                        var boundaries = {'l': 5, 't': orig_y + y - text_size, 'r': 5 + ctx.measureText(first_text)['width'], 'b': orig_y + y};
                        justify = "l";
                    }
                } else {
                    ctx.textAlign = "end";
                    //ctx.fillText(second_text, ctx.measureText(first_text)['width']/2 - orig_x, y);
                    ctx.fillText(first_text, ctx.canvas.width - 5, y);
                    ctx.translate(orig_x, 0);
                    if (second_text != "") {
                        var [boundaries, justify] = wrap_text(second_text, 't', x, y + text_size, orig_x, orig_y, ctx, text_size, 'r');
                        if ((ctx.canvas.width - 5) - ctx.measureText(first_text)['width'] < boundaries['l']) {
                            boundaries['l'] = (ctx.canvas.width - 5) - ctx.measureText(first_text)['width'];
                        }
                    } else {
                        var boundaries = {'l': (ctx.canvas.width - 5) - ctx.measureText(first_text)['width'], 't': orig_y + y - text_size, 'r': ctx.canvas.width - 5, 'b': orig_y + y};
                        justify = "r";
                    }
                }
                console.log(boundaries);
                console.log(justify);
                return [boundaries, justify];
            }


            //run through indexes of spaces form end of string, find first that makes first 
            //chunk small enough, call warp_text on second chunk

            //draw first text then call wrap_text

            //need to handle no spaces, or not small enough
        } else {
            var small = false;
            var prev_index = 0;
            var first_text;
            var second_text;
            var justify = 'n';
            //console.log(y);
            //console.log(text);
            while (!small && prev_index != -1) {
                //console.log(prev_index);
                prev_index = text.indexOf(' ', prev_index+1);
                first_text = text.slice(0, prev_index);
                second_text = text.slice(prev_index + 1);
                if ((ctx.measureText(second_text)['width']/2 <= ctx.canvas.width - orig_x) && (ctx.measureText(second_text)['width']/2 <= orig_x) && (prev_index != -1)) {
                    //console.log('here');
                    small = true;
                    var [boundaries, justify] = wrap_text(first_text, 'b', x, y - text_size, orig_x, orig_y, ctx, text_size, 'n');
                    if (justify == 'l') {
                        ctx.translate(-orig_x, 0);
                        ctx.fillText(second_text, 5, y);
                        ctx.translate(orig_x, 0);
                        if (5 + ctx.measureText(second_text)['width'] > boundaries['r']) {
                            boundaries['r'] = 5 + ctx.measureText(second_text)['width'];
                        }
                    } else if (justify == 'r') {
                        ctx.translate(-orig_x, 0);
                        ctx.fillText(second_text, ctx.canvas.width - 5, y);
                        ctx.translate(orig_x, 0);
                        if (ctx.canvas.width - 5 - ctx.measureText(second_text)['width'] < boundaries['l']) {
                            boundaries['l'] = ctx.canvas.width - 5 - ctx.measureText(second_text)['width'];
                        }
                    } else {
                        if (orig_x - ctx.measureText(second_text)['width']/2 < boundaries['l']) {
                            boundaries['l'] = orig_x - ctx.measureText(second_text)['width']/2;
                            boundaries['r'] = orig_x + ctx.measureText(second_text)['width']/2;
                        }
                        ctx.fillText(second_text, x, y);
                    }
                    //console.log(boundaries['t']);
                    boundaries['b'] = orig_y + y;
                    //console.log(orig_y);
                    //console.log(boundaries['t']);
                    //console.log(boundaries['b']);
                    
                    return [boundaries, justify];
                }
            }
            if (prev_index == -1) {
                var justify;
                var boundaries;
                //index = text.indexOf(' ', 0);
                index = text.lastIndexOf(' ', text.length-1);
                if (index == -1) {
                    first_text = '';
                    second_text = text;
                } else {
                    first_text = text.slice(0, index);
                    second_text = text.slice(index + 1);
                }
                ctx.translate(-orig_x, 0);
                if (ctx.measureText(second_text)['width']/2 > orig_x) {
                    ctx.textAlign = "start";
                    //ctx.fillText(second_text, ctx.measureText(second_text)['width']/2 - (ctx.canvas.width/2 - orig_x), y);
                    ctx.fillText(second_text, 5, y);
                    ctx.translate(orig_x, 0);
                    if (first_text != "") {
                        var [boundaries, justify] = wrap_text(first_text, 'b', x, y - text_size, orig_x, orig_y, ctx, text_size, 'l');
                        if (5 + ctx.measureText(second_text)['width'] > boundaries['r']) {
                            boundaries['r'] = 5 + ctx.measureText(second_text)['width'];
                        }
                    } else {
                        boundaries = {'l': 5, 't': orig_y + y - text_size, 'r': 5 + ctx.measureText(second_text)['width'], 'b': orig_y + y};
                        justify = "l";
                    }
                } else {
                    ctx.textAlign = "end";
                    //ctx.fillText(second_text, ctx.measureText(second_text)['width']/2 - orig_x, y);
                    ctx.fillText(second_text, ctx.canvas.width - 5, y);
                    ctx.translate(orig_x, 0);
                    if (first_text != "") {
                        var [boundaries, justify] = wrap_text(first_text, 'b', x, y - text_size, orig_x, orig_y, ctx, text_size, 'r');
                        if ((ctx.canvas.width - 5) - ctx.measureText(second_text)['width'] < boundaries['l']) {
                            boundaries['l'] = (ctx.canvas.width - 5) - ctx.measureText(second_text)['width'];
                        }
                    } else {
                        boundaries = {'l': (ctx.canvas.width - 5) - ctx.measureText(second_text)['width'], 't': orig_y + y - text_size, 'r': ctx.canvas.width - 5, 'b': orig_y + y};
                        //console.log((ctx.canvas.width - 5) - ctx.measureText(second_text));
                        //console.log(boundaries);
                        justify = "r";
                    }
                }
                //console.log(boundaries);
                console.log(justify);
                console.log(text);
                return [boundaries, justify];
            }
            //run through indexes of spaces form end of string, find first that makes first 
            //chunk small enough, call warp_text on second chunk

            //call wrap_text, then draw text
        }
    }
}

function draw_title(angle, title, canvas, max_dist, dist, more, text_size, offsetX, offsetY) {
    var ctx = canvas.getContext("2d");
    //ctx.scale(window.devicePixelRatio,window.devicePixelRatio);
    //canvas.getContext('2d').scale(2,2);
    // save the current co-ordinate system 
    // before we screw with it
    ctx.save(); 

    var angle;
    var mult;
    var x;
    var y;
    var boundaries;

    if (more > 0) {
        //var temp_title = title + ' and ' + more + ' more';
        var temp_title = title + ' +' + more;
    } else {
        var temp_title = title;
    }

    [ctx, mult, x, y, angle] = move_context(canvas, ctx, angle, max_dist, dist);
    //console.log(mult);
    ctx.translate((canvas.width/10)*mult, 0);
    ctx.rotate(-angle);

    if (title != 0) {
        ctx.textAlign = "center";
        ctx.fillStyle = "grey";
        ctx.font = (text_size*window.devicePixelRatio).toString() + "px Times New Roman";
        //ctx.fillStyle = "grey";
        if (Math.sin(angle) < 0) {
            //ctx.fillText(title, 0, -5);
            //boundaries = wrap_text(title, 'b', 0, -5, x + (Math.cos(-angle)*(canvas.width/10)*mult), y + (Math.sin(-angle)*(canvas.width/10)*mult), ctx);
            boundaries = wrap_text(temp_title, 'b', 0 + offsetX, -5 + offsetY, x + (Math.cos(-angle)*(canvas.width/10)*mult) + offsetX, y - (Math.sin(-angle)*(canvas.width/10)*mult), ctx, text_size*window.devicePixelRatio, 'n')[0];
        } else {
            //ctx.fillText(title, 0, 10);
            //boundaries = wrap_text(title, 't', 0, 10, x + (Math.cos(-angle)*(canvas.width/10)*mult), y + (Math.sin(-angle)*(canvas.width/10)*mult), ctx);
            boundaries = wrap_text(temp_title, 't', 0 + offsetX, 15 + offsetY, x + (Math.cos(-angle)*(canvas.width/10)*mult) + offsetX, y - (Math.sin(-angle)*(canvas.width/10)*mult), ctx, text_size*window.devicePixelRatio, 'n')[0];
        }
        console.log(boundaries);
        console.log(temp_title);
        ctx.textAlign = "center";
    }
    boundaries['t'] = boundaries['t'] + 2*window.devicePixelRatio;
    boundaries['b'] = boundaries['b'] + 2*window.devicePixelRatio;

    ctx.restore(); 
    /*ctx.beginPath();
    ctx.strokeStyle = "red";
    ctx.rect(boundaries['l'], boundaries['t'], boundaries['r'] - boundaries['l'], boundaries['b'] - boundaries['t']);
    ctx.stroke();
    ctx.closePath();*/
    return {'title': title, 'boundaries': boundaries, 'offsetX': offsetX, 'offsetY': offsetY};
}

function move_context(canvas, ctx, angle, max_dist, dist) {
    /*if (localStorage.getItem('hdng') != 'NaN' && localStorage.getItem('hdng') != none) {
        angle = angle + localStorage.getItem('hdng');
        console.log(angle);
        console.log(localStorage.getItem('hdng'));
    }*/
 
    var x = ((Math.cos(angle)/(Math.PI/2.0))+1)*canvas.width/2.0;
    var y = ((Math.sin(angle)/(Math.PI/2.0))+1)*canvas.height/2.0;
    if (Math.cos(angle) > 0) {
        y = canvas.height - y;
        angle = -angle;
    }
    //x = ((x-(canvas.width/2.0))*(dist/max_dist))+(canvas.width/2.0)
    //y = ((y-(canvas.height/2.0))*(dist/max_dist))+(canvas.height/2.0)
    var mult = ((max_dist - dist) / max_dist) * 0.5 + 0.5; 

    // move to the middle of where we want to draw our image
    ctx.translate(x, y);
 
    // rotate around that point, converting our 
    // angle from degrees to radians 
    ctx.rotate(angle);
    //console.log(mult);
    return [ctx, mult, x, y, angle];
}

function draw_rotated_image(angle, canvas, title, max_dist, dist) {
    title = title || 0;
    var ctx = canvas.getContext("2d");
    //ctx.scale(window.devicePixelRatio,window.devicePixelRatio);
    //canvas.getContext('2d').scale(2,2);
    // save the current co-ordinate system 
    // before we screw with it
    ctx.save(); 

    /*if (localStorage.getItem('hdng') != 'NaN' && localStorage.getItem('hdng') != none) {
        angle = angle + localStorage.getItem('hdng');
        console.log(angle);
        console.log(localStorage.getItem('hdng'));
    }
 
    var x = ((Math.cos(angle)/(Math.PI/2.0))+1)*canvas.width/2.0;
    var y = ((Math.sin(angle)/(Math.PI/2.0))+1)*canvas.height/2.0;
    if (Math.cos(angle) > 0) {
        y = canvas.height - y;
        angle = -angle;
    }
    var mult = ((max_dist - dist) / max_dist) * 0.5 + 0.5; 

    // move to the middle of where we want to draw our image
    ctx.translate(x, y);
 
    // rotate around that point, converting our 
    // angle from degrees to radians 
    ctx.rotate(angle);*/

    var mult;
    var x;
    var y;

    [ctx, mult, x, y, angle] = move_context(canvas, ctx, angle, max_dist, dist);
    //console.log(mult);

    //ctx.drawImage(image, -(image.width/2), -(image.height/2));

    /*if (Math.cos(angle) >= 0) {
        ctx.fillStyle = "red";
    } else {
        ctx.fillStyle = "black";
    }*/

    //redo using canvas
    ctx.fillStyle = "black";
    ctx.beginPath();
    ctx.moveTo(0,0);
    ctx.lineTo((-canvas.width/20)*mult, (canvas.width/20)*mult);
    ctx.lineTo((canvas.width/10)*mult, 0);
    ctx.lineTo((-canvas.width/20)*mult, (-canvas.width/20)*mult);
    ctx.closePath();
    ctx.fill();
    ctx.beginPath();

    if (Math.cos(angle) < 0) {
        ctx.strokeStyle = "#F0F0F0";
        ctx.moveTo((canvas.width/10)*mult+0.5, 1+0.5);
        ctx.lineTo((-canvas.width/20)*mult+0.5, (canvas.width/20)*mult+1+0.5);
        ctx.stroke();
        ctx.moveTo(-1+0.5,0+0.5);
        ctx.lineTo((-canvas.width/20)*mult-1+0.5, (-canvas.width/20)*mult+0.5);
        ctx.stroke();
        ctx.beginPath();
        ctx.strokeStyle = "#333333";
        ctx.moveTo((canvas.width/10)*mult+0.5, -1+0.5);
        ctx.lineTo((-canvas.width/20)*mult+0.5, -((canvas.width/20)*mult+1)+0.5);
        ctx.stroke();
        ctx.moveTo(-1+0.5,0+0.5);
        ctx.lineTo((-canvas.width/20)*mult-1+0.5, (canvas.width/20)*mult+0.5);
        ctx.stroke();
    } else {
        ctx.strokeStyle = "#333333";
        ctx.moveTo((canvas.width/10)*mult, 1);
        ctx.lineTo((-canvas.width/20)*mult, (canvas.width/20)*mult+1);
        ctx.stroke();
        ctx.moveTo(-1,0);
        ctx.lineTo((-canvas.width/20)*mult-1, (-canvas.width/20)*mult);
        ctx.stroke();
        ctx.beginPath();
        ctx.strokeStyle = "#F0F0F0";
        ctx.moveTo((canvas.width/10)*mult, -1);
        ctx.lineTo((-canvas.width/20)*mult, -((canvas.width/20)*mult+1));
        ctx.stroke();
        ctx.moveTo(-1,0);
        ctx.lineTo((-canvas.width/20)*mult-1, (canvas.width/20)*mult);
        ctx.stroke();
    }

    ctx.closePath();

    /*ctx.translate((canvas.width/10)*mult, 0);
    ctx.rotate(-angle);

    if (title != 0) {
        ctx.textAlign = "center";
        ctx.fillStyle = "grey";
        ctx.font = "15px Arial";
        //ctx.fillStyle = "grey";
        if (Math.sin(angle) < 0) {
            //ctx.fillText(title, 0, -5);
            wrap_text(title, 'b', 0, -5, x + (Math.cos(angle)*(canvas.width/10)*mult), ctx);
        } else {
            //ctx.fillText(title, 0, 10);
            wrap_text(title, 't', 0, 10, x + (Math.cos(angle)*(canvas.width/10)*mult), ctx);
        }
    }*/


    //ctx.drawImage(image, x, y);
 
    var rX = x + ((((-canvas.width/20)*mult)) * Math.cos(angle)) - (((canvas.width/20)*mult) * Math.sin(angle)); 
    var rY = y + ((((-canvas.width/20)*mult)) * Math.sin(angle)) + (((canvas.width/20)*mult) * Math.cos(angle)); 
    var lX = x + ((((-canvas.width/20)*mult)) * Math.cos(angle)) - (((-canvas.width/20)*mult) * Math.sin(angle)); 
    var lY = y + ((((-canvas.width/20)*mult)) * Math.sin(angle)) + (((-canvas.width/20)*mult) * Math.cos(angle)); 
    
    // and restore the co-ords to how they were when we began
    ctx.restore(); 
    //return {'pos': {'x': x, 'y': y}, 'angle': angle};
    return {'pos': {'x': x, 'y': y}, 'lbp': {'x': lX, 'y': lY}, 'rbp': {'x': rX, 'y': rY}};
}

function angle_too_close(angle1, angle2, tolerance) {
    var test = (Math.abs((angle1 % (Math.PI*2)) - (angle2 % (Math.PI * 2))));
    return (test < tolerance);
    //return (Math.abs((angle1 % (Math.PI*2)) - (angle2 % (Math.PI * 2)))) < tolerance;
}

function convert_to_url(title) {
    return "https://en.wikipedia.org/wiki/" + title.replace(' ', '_');
}

function draw_geo(geo_point, canvas, dist) {
    //return 0;
    //var img=document.getElementById("test-img");
    //console.log(geo_point['_source']['geo']);
    var angle = get_angle(lat, lon, geo_point['_source']['geo']['lat'], geo_point['_source']['geo']['lon']);
    var too_close = false;
    //if angle is too close to another already determined angle, skip drawing and add to overflow object under detrmined angle's key. 
    //return -1, and where this is called, cehck to see if return value is -1; if it is, increase i by one
    //then, when that geo_point's text is drawn, check if it is a key in the overflow object, and if it is, add "and x more" after its title 
    var i = 0;
    if (Math.cos(angle) < 0) {
        //angle = -angle;
        while (i < geo_list.length && !too_close) {
        //for (i = 0; i < geo_list.length; i ++) {
            if (angle_too_close(angle, geo_list[i]['angle'], 0.1 * 1920 / canvas.width)) {
                too_close = true;
                if (Object.keys(overflow).indexOf(geo_list[i]['title']) != -1) {
                    overflow[geo_list[i]['title']][geo_point['_source']['title']] = {'geo': geo_point['_source']['geo'], 'info': geo_point['_source']['info']};
                    //overflow[geo_list[i]['title']].push(geo_point['_source']['title']);
                } else {
                    //overflow[geo_list[i]['title']] = [geo_list[i]['title'], geo_point['_source']['title']];
                    temp_obj1 = {'geo': geo_list[i]['geo'], 'info': geo_list[i]['info']};
                    temp_obj2 = {'geo': geo_point['_source']['geo'],'info': geo_point['_source']['info']};
                    /*temp_key1 = geo_list[i]['title'];
                    console.log()
                    temp_key2 = geo_point['_source']['title'];
                    overflow[geo_list[i]['title']] = {temp_key1: temp_obj1, temp_key2: temp_obj2};*/
                    //temp_obj3 = {};
                    //temp_obj[{geo_list[i]['title'].toString(): temp_obj1, geo_point['_source']['title']: temp_obj2};
                    overflow[geo_list[i]['title']] = {};
                    overflow[geo_list[i]['title']][geo_list[i]['title']] = temp_obj1;
                    overflow[geo_list[i]['title']][geo_point['_source']['title']] = temp_obj2;
                    //overflow[geo_list[i]['title']] = {geo_list[i]['title']: {'geo': geo_list[i]['geo'], 'info': geo_list[i]['info']}, geo_point['_source']['title']: {'geo': geo_point['_source']['geo'], 'info': geo_point['_source']['first_para']}};
                }
                txt = '#' + i.toString();
                console.log(txt);
                $(txt).after('<tr><td><a href="#info-page" data-transition="slideup" onClick="loadInfo(this.text)" style="padding-left: 20px">\t' + geo_point['_source']['title'] + '</a><button class="ui-button" data-inline="true" data-icon="arrow-u-r" id="' + geo_point['_source']['title'] + '" onClick="mapLoad(this.id)">map</button></td></tr>');
            }
            i ++;
        }
        //angle = -angle;
    } else {
        while (i < geo_list.length && !too_close) {
        //for (i = 0; i < geo_list.length; i ++) {
            if (angle_too_close(angle, geo_list[i]['angle'], 0.1 * 1920 / canvas.width)) {
                too_close = true;
                if (Object.keys(overflow).indexOf(geo_list[i]['title']) != -1) {
                    overflow[geo_list[i]['title']][geo_point['_source']['title']] = {'geo': geo_point['_source']['geo'], 'info': geo_point['_source']['info']};
                    //overflow[geo_list[i]['title']].push(geo_point['_source']['title']);
                } else {
                    //overflow[geo_list[i]['title']] = [geo_list[i]['title'], geo_point['_source']['title']];
                    temp_obj1 = {'geo': geo_list[i]['geo'], 'info': geo_list[i]['info']};
                    temp_obj2 = {'geo': geo_point['_source']['geo'],'info': geo_point['_source']['info']};
                    /*temp_key1 = geo_list[i]['title'];
                    console.log()
                    temp_key2 = geo_point['_source']['title'];
                    overflow[geo_list[i]['title']] = {temp_key1: temp_obj1, temp_key2: temp_obj2};*/
                    //temp_obj3 = {};
                    //temp_obj[{geo_list[i]['title'].toString(): temp_obj1, geo_point['_source']['title']: temp_obj2};
                    overflow[geo_list[i]['title']] = {};
                    overflow[geo_list[i]['title']][geo_list[i]['title']] = temp_obj1;
                    overflow[geo_list[i]['title']][geo_point['_source']['title']] = temp_obj2;
                    //overflow[geo_list[i]['title']] = {geo_list[i]['title'] + '': {'geo': geo_list[i]['geo'], 'info': geo_list[i]['info']}, geo_point['_source']['title']: {'geo': geo_point['_source']['geo'],'info': geo_point['_source']['first_para']}};
                }
                txt = '#' + i.toString();
                console.log(txt);
                $(txt).after('<tr><td><a href="#info-page" data-transition="slideup" onClick="loadInfo(this.text)" style="padding-left: 20px">\t' + geo_point['_source']['title'] + '</a><button class="ui-button" data-inline="true" data-icon="arrow-u-r" id="' + geo_point['_source']['title'] + '" onClick="mapLoad(this.id)">map</button></td></tr>');
            }
            i ++;
        }
    }

    if (too_close) {
        return -1;
    }

    
    $('#list-table').append('<tr id="' + (geo_list.length).toString() + '"><td><a href="#info-page" data-transition="slideup" onClick="loadInfo(this.text)">' + geo_point['_source']['title'] + '</a><button class="ui-button" data-inline="true" data-icon="arrow-u-r" id="' + geo_point['_source']['title'] + '" onClick="mapLoad(this.id)">map</button></td></tr>');
    $('#list-table').trigger('create');
    var ret = draw_rotated_image(angle, canvas, geo_point['_source']['title'], dist, geo_point['sort']);
    return {'pos': ret['pos'], 'geo': geo_point['_source']['geo'], 'title': geo_point['_source']['title'], 'angle': angle, 'sort': geo_point['sort'][0], 'lbp': ret['lbp'], 'rbp': ret['rbp'], 'info': geo_point['_source']['info'], 'offsetX' : 0, 'offsetY': 0};
    //$("#test-img").attr("src", 'img/512/navigate.png');
    //var ctx = canvas.getContext("2d");
    //ctx.drawImage('img/512/navigate.png', 0, 0);
}

function get_angle(d_lat, d_lon, o_lat, o_lon) {
    var arc_angle = ((o_lon - d_lon)/Math.sqrt(Math.pow((o_lon - d_lon),2) + Math.pow((o_lat - d_lat),2)));
    //console.log(arc_angle);
    angle = Math.asin(arc_angle);
    //angle = Math.acos(arc_angle);
    //console.log(angle);
    //console.log(d_lat);
    //console.log(o_lat);
    /*if (Math.asin(arc_angle) < 0) {
        angle = -angle;
    }*/

    if ((angle >= 0) && (o_lat < d_lat)) {
        angle = Math.PI - angle;
    } else if ((angle < 0) && (o_lat >= d_lat)) {
        angle = Math.PI - angle;
    } else if ((angle < 0) && (o_lat < d_lat)) {
        angle = (2*Math.PI) + angle;
    }
    //console.log(angle);
    //return -((Math.PI*3/2)-angle);
    return (Math.PI*1/2)-angle;
}

function changeSettings() {
    var temp_docs = $('docs-form').serializeArray();
    console.log(temp_docs)
    return false;
}

//var canvas = $("#mainCanvas").get(0);

var canvas=document.getElementById("mainCanvas");
canvas.addEventListener("click", arrowClick, false);
canvas.addEventListener("click", textClick, false);
canvas.addEventListener("click", dataRefresh, false);
//canvas.addEventListener("click", testAlert, false);

function dataRefresh(event) {
    var canvas = $("#mainCanvas").get(0);
    if (Math.sqrt(Math.pow((canvas.width/2 - (event.offsetX * window.devicePixelRatio)), 2) + Math.pow((canvas.height/2 - (event.offsetY * window.devicePixelRatio)), 2)) < 100) {
        var data = {
            lat:  lat,
            lon: lon,
            dist: dist,
            num: num * 3,
            docs: localStorage['docs']
        };
        //console.log(data);
        $("#list-table tr").remove();
        //$.post("http://knowvia-dev.us-west-2.elasticbeanstalk.com/nearby", data, function(ret) {
        $.post("http://localhost:9200/nearby", data, function(ret) {

            geo_list = [];
            text_list = [];
            overflow = {};
            moveTextList = [[],[],[],[],[],[],[],[],[],[]];

            $("#heading").text("N");

            $("#ret-json").text(JSON.stringify(ret));

            var j = 0;
            var i;
            var canvas = $("#mainCanvas").get(0);

            var ctx = canvas.getContext("2d");
                    
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            ctx.moveTo(canvas.width/2, canvas.height/2);
            ctx.beginPath();
            ctx.strokeStyle = "red";
            var a = 1;
            var b = 1;

            for (i = 0; i < 720; i++) {
                angle = 0.1 * i;
                x = canvas.width/2 + (a + b * angle) * Math.cos(angle);
                y = canvas.height/2 + (a + b * angle) * Math.sin(angle);
                ctx.lineTo(x, y);
            }
            ctx.stroke();

            console.log(num);
            var k = 0;
            console.log(ret);
            while (j < num && k < ret.length) {
                var drawn = draw_geo(ret[k], canvas, dist);
                if (drawn != -1) {
                    geo_list.push(drawn);
                } else {
                    j --;
                }
                k ++;
                j ++;
            }
            for (i = 0; i < geo_list.length; i++) {
                if (Object.keys(overflow).indexOf(geo_list[i]['title']) != -1) {
                    text_list.push(draw_title(geo_list[i]['angle'], geo_list[i]['title'], canvas, dist, geo_list[i]['sort'], Object.keys(overflow[geo_list[i]['title']]).length - 1, 15, geo_list[i]['offsetX'], geo_list[i]['offsetY']));
                } else {
                    text_list.push(draw_title(geo_list[i]['angle'], geo_list[i]['title'], canvas, dist, geo_list[i]['sort'], 0, 15, geo_list[i]['offsetX'], geo_list[i]['offsetY']));
                }
                geo_list[i]['tb'] = text_list[i]['boundaries'];
            }
            localStorage.setItem('json', ret);
            fixScreen(canvas);
        });
    }
}

function checkText() {
    var moving = false;
    for (i = 0; i < text_list.length; i++) {
        for (k = i + 1; k < text_list.length; k ++) {
            //if (((text_list[i]['boundaries']['l'] < text_list[k]['boundaries']['r']) || (text_list[k]['boundaries']['l'] < text_list[i]['boundaries']['r'])) && ((text_list[i]['boundaries']['t'] < text_list[k]['boundaries']['b']) || (text_list[k]['boundaries']['t'] < text_list[i]['boundaries']['b']))) {
            if ((((text_list[k]['boundaries']['t'] < text_list[i]['boundaries']['b']) && (text_list[k]['boundaries']['t'] > text_list[i]['boundaries']['t'])) || ((text_list[k]['boundaries']['b'] < text_list[i]['boundaries']['b']) && (text_list[k]['boundaries']['b'] > text_list[i]['boundaries']['t']))) && (((text_list[k]['boundaries']['l'] < text_list[i]['boundaries']['r']) && (text_list[k]['boundaries']['l'] > text_list[i]['boundaries']['l'])) || ((text_list[k]['boundaries']['r'] < text_list[i]['boundaries']['r']) && (text_list[k]['boundaries']['r'] > text_list[i]['boundaries']['l'])))) {
                console.log('here');
                console.log(i);
                console.log(k);
                moveTextList[i].push(k);
                moving = true;
            } else {
                console.log('here2');
            }
        }
    }
    return moving;
}

function moveText(textIndex1, textIndex2) {
    //move text

    var canvas = $("#mainCanvas").get(0);

    //move in least overlapping direction, slightly in most overlapping direction.
    //if one text's x or y boundaries completely envelop the other's compare centers
    //check to make sure no text will go offscreen

    //overlaps are negative if there is overlap

    //((((text_list[k]['boundaries']['t'] < text_list[i]['boundaries']['b']) && (text_list[k]['boundaries']['t'] > text_list[i]['boundaries']['t'])) || ((text_list[k]['boundaries']['b'] < text_list[i]['boundaries']['b']) && (text_list[k]['boundaries']['b'] > text_list[i]['boundaries']['t']))) && (((text_list[k]['boundaries']['l'] < text_list[i]['boundaries']['r']) && (text_list[k]['boundaries']['l'] > text_list[i]['boundaries']['l'])) || ((text_list[k]['boundaries']['r'] < text_list[i]['boundaries']['r']) && (text_list[k]['boundaries']['r'] > text_list[i]['boundaries']['l']))));

    //k is top left
    /*if (((text_list[k]['boundaries']['t'] < text_list[i]['boundaries']['b']) && (text_list[k]['boundaries']['t'] > text_list[i]['boundaries']['t'])) && ((text_list[k]['boundaries']['l'] < text_list[i]['boundaries']['r']) && (text_list[k]['boundaries']['l'] > text_list[i]['boundaries']['l']))) {
    //the right side of text2 is to the right of the left side of text1
        l_overlap = text_list[textIndex1]['boundaries']['l'] - text_list[textIndex2]['boundaries']['r'];

        //the left side of text2 is to the left of the right side of text1
        r_overlap = text_list[textIndex2]['boundaries']['l'] - text_list[textIndex1]['boundaries']['r'];

        //the top of text2 is above the bottom of text1
        t_overlap = text_list[textIndex1]['boundaries']['t'] - text_list[textIndex2]['boundaries']['b'];

        //the bottom of text2 is below the top of text1
        b_overlap = text_list[textIndex2]['boundaries']['t'] - text_list[textIndex1]['boundaries']['b'];
    } 
    //k is top right
    else if (((text_list[k]['boundaries']['t'] < text_list[i]['boundaries']['b']) && (text_list[k]['boundaries']['t'] > text_list[i]['boundaries']['t'])) && ((text_list[k]['boundaries']['r'] < text_list[i]['boundaries']['r']) && (text_list[k]['boundaries']['r'] > text_list[i]['boundaries']['l']))) {

    }

    //k is bottom right
    else if (((text_list[k]['boundaries']['b'] < text_list[i]['boundaries']['b']) && (text_list[k]['boundaries']['b'] > text_list[i]['boundaries']['t'])) && ((text_list[k]['boundaries']['l'] < text_list[i]['boundaries']['r']) && (text_list[k]['boundaries']['l'] > text_list[i]['boundaries']['l']))) {

    }

    else if (((text_list[k]['boundaries']['b'] < text_list[i]['boundaries']['b']) && (text_list[k]['boundaries']['b'] > text_list[i]['boundaries']['t'])) && ((text_list[k]['boundaries']['r'] < text_list[i]['boundaries']['r']) && (text_list[k]['boundaries']['r'] > text_list[i]['boundaries']['l']))) {

    }*/
    //the right side of text2 is to the right of the left side of text1
    l_overlap = text_list[textIndex1]['boundaries']['l'] - text_list[textIndex2]['boundaries']['r'];

    //the left side of text2 is to the left of the right side of text1
    r_overlap = text_list[textIndex2]['boundaries']['l'] - text_list[textIndex1]['boundaries']['r'];

    //the top of text2 is above the bottom of text1
    t_overlap = text_list[textIndex1]['boundaries']['t'] - text_list[textIndex2]['boundaries']['b'];

    //the bottom of text2 is below the top of text1
    b_overlap = text_list[textIndex2]['boundaries']['t'] - text_list[textIndex1]['boundaries']['b'];

    if (l_overlap > 0) {
        l_overlap -= 1000000;
    }

    if (r_overlap > 0) {
        r_overlap -= 1000000;
    }

    if (t_overlap > 0) {
        t_overlap -= 1000000;
    }

    if (b_overlap > 0) {
        b_overlap -= 1000000;
    }

    //move vertically
    if (Math.max(l_overlap, r_overlap) < Math.max(t_overlap, b_overlap)) {
        //move text2 down, text1 up
        if (t_overlap < b_overlap) {
            console.log('2 down');
            if ((text_list[textIndex1]['boundaries']['t'] > 5) && (text_list[textIndex2]['boundaries']['b'] < (canvas.width - 5))) {
                //text_list[textIndex1]['boundaries']['t'] = text_list[textIndex1]['boundaries']['t'] - 1*window.devicePixelRatio;
                text_list[textIndex1]['offsetY'] = text_list[textIndex1]['offsetY'] - 1*window.devicePixelRatio;
                geo_list[textIndex1]['offsetY'] = geo_list[textIndex1]['offsetY'] - 1*window.devicePixelRatio;
                //text_list[textIndex2]['boundaries']['b'] = text_list[textIndex2]['boundaries']['b'] + 1*window.devicePixelRatio;
                text_list[textIndex2]['offsetY'] = text_list[textIndex2]['offsetY'] + 1*window.devicePixelRatio;
                geo_list[textIndex2]['offsetY'] = geo_list[textIndex2]['offsetY'] + 1*window.devicePixelRatio;
            } else if (text_list[textIndex1]['boundaries']['t'] > 6) {
                //text_list[textIndex1]['boundaries']['t'] = text_list[textIndex1]['boundaries']['t'] - 2*window.devicePixelRatio;
                text_list[textIndex1]['offsetY'] = text_list[textIndex1]['offsetY'] - 2*window.devicePixelRatio;
                geo_list[textIndex1]['offsetY'] = geo_list[textIndex1]['offsetY'] - 2*window.devicePixelRatio;
            } else if (text_list[textIndex2]['boundaries']['b'] < (canvas.width - 6)) {
                //text_list[textIndex2]['boundaries']['b'] = text_list[textIndex2]['boundaries']['b'] + 2*window.devicePixelRatio;
                text_list[textIndex2]['offsetY'] = text_list[textIndex2]['offsetY'] + 2*window.devicePixelRatio;
                geo_list[textIndex2]['offsetY'] = geo_list[textIndex2]['offsetY'] + 2*window.devicePixelRatio;
            }
        } else {
            console.log('2 up');
            if ((text_list[textIndex2]['boundaries']['t'] > 5) && (text_list[textIndex1]['boundaries']['b'] < (canvas.width - 5))) {
                //text_list[textIndex2]['boundaries']['t'] = text_list[textIndex2]['boundaries']['t'] - 1*window.devicePixelRatio;
                text_list[textIndex2]['offsetY'] = text_list[textIndex2]['offsetY'] - 1*window.devicePixelRatio;
                geo_list[textIndex2]['offsetY'] = geo_list[textIndex2]['offsetY'] - 1*window.devicePixelRatio;
                //text_list[textIndex1]['boundaries']['b'] = text_list[textIndex1]['boundaries']['b'] + 1*window.devicePixelRatio;
                text_list[textIndex1]['offsetY'] = text_list[textIndex1]['offsetY'] + 1*window.devicePixelRatio;
                geo_list[textIndex1]['offsetY'] = geo_list[textIndex1]['offsetY'] + 1*window.devicePixelRatio;
            } else if (text_list[textIndex2]['boundaries']['t'] > 6) {
                //text_list[textIndex2]['boundaries']['t'] = text_list[textIndex2]['boundaries']['t'] - 2*window.devicePixelRatio;
                text_list[textIndex2]['offsetY'] = text_list[textIndex2]['offsetY'] - 2*window.devicePixelRatio;
                geo_list[textIndex2]['offsetY'] = geo_list[textIndex2]['offsetY'] - 2*window.devicePixelRatio;
            } else if (text_list[textIndex1]['boundaries']['b'] < (canvas.width - 6)) {
                //text_list[textIndex1]['boundaries']['b'] = text_list[textIndex1]['boundaries']['b'] + 2*window.devicePixelRatio;
                text_list[textIndex1]['offsetY'] = text_list[textIndex1]['offsetY'] + 2*window.devicePixelRatio;
                geo_list[textIndex1]['offsetY'] = geo_list[textIndex1]['offsetY'] + 2*window.devicePixelRatio;
            }
        }
    } else {
        //move text2 right, text1 left
        console.log(l_overlap);
        console.log(r_overlap);
        if (l_overlap < r_overlap) {
            console.log('2 right');
            if ((text_list[textIndex1]['boundaries']['l'] > 5) && (text_list[textIndex2]['boundaries']['r'] < (canvas.width - 5))) {
                //text_list[textIndex1]['boundaries']['l'] = text_list[textIndex1]['boundaries']['l'] - 1*window.devicePixelRatio;
                text_list[textIndex1]['offsetX'] = text_list[textIndex1]['offsetX'] - 1*window.devicePixelRatio;
                geo_list[textIndex1]['offsetX'] = geo_list[textIndex1]['offsetX'] - 1*window.devicePixelRatio;
                //text_list[textIndex2]['boundaries']['r'] = text_list[textIndex2]['boundaries']['r'] + 1*window.devicePixelRatio;
                text_list[textIndex2]['offsetX'] = text_list[textIndex2]['offsetX'] + 1*window.devicePixelRatio;
                geo_list[textIndex2]['offsetX'] = geo_list[textIndex2]['offsetX'] + 1*window.devicePixelRatio;
            } else if (text_list[textIndex1]['boundaries']['l'] > 6) {
                //text_list[textIndex1]['boundaries']['l'] = text_list[textIndex1]['boundaries']['l'] - 2*window.devicePixelRatio;
                text_list[textIndex1]['offsetX'] = text_list[textIndex1]['offsetX'] - 2*window.devicePixelRatio;
                geo_list[textIndex1]['offsetX'] = geo_list[textIndex1]['offsetX'] - 2*window.devicePixelRatio;
            } else if (text_list[textIndex2]['boundaries']['r'] < (canvas.width - 6)) {
                //text_list[textIndex2]['boundaries']['r'] = text_list[textIndex2]['boundaries']['r'] + 2*window.devicePixelRatio;
                text_list[textIndex2]['offsetX'] = text_list[textIndex2]['offsetX'] + 2*window.devicePixelRatio;
                geo_list[textIndex2]['offsetX'] = geo_list[textIndex2]['offsetX'] + 2*window.devicePixelRatio;
            }
        } else {
            console.log('2 left');
            if ((text_list[textIndex2]['boundaries']['l'] > 5) && (text_list[textIndex1]['boundaries']['r'] < (canvas.width - 5))) {
                //text_list[textIndex2]['boundaries']['l'] = text_list[textIndex2]['boundaries']['l'] - 1*window.devicePixelRatio;
                text_list[textIndex2]['offsetX'] = text_list[textIndex2]['offsetX'] - 1*window.devicePixelRatio;
                geo_list[textIndex2]['offsetX'] = geo_list[textIndex2]['offsetX'] - 1*window.devicePixelRatio;
                //text_list[textIndex1]['boundaries']['r'] = text_list[textIndex1]['boundaries']['r'] + 1*window.devicePixelRatio;
                text_list[textIndex1]['offsetX'] = text_list[textIndex1]['offsetX'] + 1*window.devicePixelRatio;
                geo_list[textIndex1]['offsetX'] = geo_list[textIndex1]['offsetX'] + 1*window.devicePixelRatio;
            } else if (text_list[textIndex2]['boundaries']['l'] > 6) {
                //text_list[textIndex2]['boundaries']['l'] = text_list[textIndex2]['boundaries']['l'] - 2*window.devicePixelRatio;
                text_list[textIndex2]['offsetX'] = text_list[textIndex2]['offsetX'] - 2*window.devicePixelRatio;
                geo_list[textIndex2]['offsetX'] = geo_list[textIndex2]['offsetX'] - 2*window.devicePixelRatio;
            } else if (text_list[textIndex1]['boundaries']['r'] < (canvas.width - 6)) {
                //text_list[textIndex1]['boundaries']['r'] = text_list[textIndex1]['boundaries']['r'] + 2*window.devicePixelRatio;
                text_list[textIndex1]['offsetX'] = text_list[textIndex1]['offsetX'] + 2*window.devicePixelRatio;
                geo_list[textIndex1]['offsetX'] = geo_list[textIndex1]['offsetX'] + 2*window.devicePixelRatio;
            }
        }
    }
    //return true if not overlapping anymore
}

function changeOffset() {

}

function modText() {

}

function moveAllText() {

    //move text
    for (i = 0; i < moveTextList.length; i ++) {
        var k = 0;
        while (k < moveTextList[i].length) {
            /*if (moveText(i, k)) {
                moveTextList[i].splice(k,1);
            } else {
                k ++;
            }*/
            moveText(i, moveTextList[i][k]);
            k ++;
        }
    }

    //moveTextList = [[],[],[],[],[],[],[],[],[],[]];
    //return(checkText());
}

function drawAllText() {
    for (i = 0; i < geo_list.length; i++) {
        if (Object.keys(overflow).indexOf(geo_list[i]['title']) != -1) {
            text_list[i] = draw_title(geo_list[i]['angle'], geo_list[i]['title'], canvas, dist, geo_list[i]['sort'], Object.keys(overflow[geo_list[i]['title']]).length - 1, 15, geo_list[i]['offsetX'], geo_list[i]['offsetY']);
        } else {
            text_list[i] = draw_title(geo_list[i]['angle'], geo_list[i]['title'], canvas, dist, geo_list[i]['sort'], 0, 15, geo_list[i]['offsetX'], geo_list[i]['offsetY']);
        }
        geo_list[i]['tb'] = text_list[i]['boundaries'];
    }
}

function fillKnown(canvas) {
    ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.moveTo(canvas.width/2, canvas.height/2);
    ctx.beginPath();
    ctx.strokeStyle = "red";
    var a = 1;
    var b = 1;

    for (i = 0; i < 720; i++) {
        angle = 0.1 * i;
        x = canvas.width/2 + (a + b * angle) * Math.cos(angle);
        y = canvas.height/2 + (a + b * angle) * Math.sin(angle);
        ctx.lineTo(x, y);
    }
    ctx.stroke();
    for (i = 0; i < geo_list.length; i++) {
        draw_rotated_image(geo_list[i]['angle'], canvas, geo_list['title'], dist, geo_list[i]['sort']);
    }
}

function fixScreen(canvas) {
    fillKnown(canvas);
    moveAllText();
    console.log(moveTextList);
    drawAllText();
    moveTextList = [[],[],[],[],[],[],[],[],[],[]];
    var moreMovement = checkText();
    if (moreMovement) {
        setTimeout(function(){ fixScreen(canvas); }, 1000/30);
        //setTimeout(fixScreen(canvas), 3000);
    }
    //schedule more if necessary
}

function testAlert(event) {
    var canvas = $("#mainCanvas").get(0);
    alert("You clicked x: " + event.offsetX * window.devicePixelRatio + ", y: " + event.offsetY * window.devicePixelRatio);
    alert(Math.sqrt(Math.pow((canvas.width/2 - (event.offsetX * window.devicePixelRatio)), 2) + Math.pow((canvas.height/2 - (event.offsetY * window.devicePixelRatio)), 2)));
}

function arrowClick(event) {
    var minDist = 50;
    var closest = -1;
    x = event.offsetX * window.devicePixelRatio;
    y = event.offsetY * window.devicePixelRatio;
    //console.log(event.offsetX);
    //console.log(event.offsetY);
    var i;
    for (i = 0; i < geo_list.length; i++) {
        if (Math.sqrt(Math.pow(x - geo_list[i]['pos']['x'], 2) + Math.pow(y - geo_list[i]['pos']['y'], 2)) < minDist) {
            closest = i;
            minDist = Math.sqrt(Math.pow(x - geo_list[i]['pos']['x'], 2) + Math.pow(y - geo_list[i]['pos']['y'], 2));
        }
    }
    if (closest != -1) {
        //console.log(geo_list[closest]);
        //console.log(geo_list[closest]['geo']['lat'] + ', ' + geo_list[closest]['geo']['lon']);
        //localStorage.setItem('latLon', {'lat': geo_list[closest]['geo']['lat'], 'lon': geo_list[closest]['geo']['lon']});
        localStorage.setItem('thisLat', geo_list[closest]['geo']['lat']);
        localStorage.setItem('thisLon', geo_list[closest]['geo']['lon']);
        localStorage.setItem('thisTitle', geo_list[closest]['title']);
        $("body").pagecontainer("change", "#map-popup", {transition: "slideup"});
        //console.log(localStorage.getItem('latLon')['lat']);
        /*$("#map-popup").height(window.innerHeight);
        $("#button-div").height(window.innerHeight*0.1);
        $("#googleMap").height(window.innerHeight*.9);
        console.log($("#googleMap").height());*/
        /*function initMap() {
                var mapProp = {
                center:new google.maps.LatLng(geo_list[closest]['geo']['lat'],geo_list[closest]['geo']['lon']),
                zoom:15,
                mapTypeId:google.maps.MapTypeId.ROADMAP
            };
            var map=new google.maps.Map(document.getElementById("googleMap"), mapProp);
            var marker = new google.maps.Marker({
                position: new google.maps.LatLng(geo_list[closest]['geo']['lat'],geo_list[closest]['geo']['lon']),
                map: map,
                title: geo_list[closest]['title']
            });
            google.maps.event.trigger(map, 'resize');
        }*/
        /*var mapProp = {
            center:new google.maps.LatLng(geo_list[closest]['geo']['lat'],geo_list[closest]['geo']['lon']),
            zoom:15,
            mapTypeId:google.maps.MapTypeId.ROADMAP
        };
        var map=new google.maps.Map(document.getElementById("googleMap"), mapProp);*/
        /*var marker = new google.maps.Marker({
            position: new google.maps.LatLng(geo_list[closest]['geo']['lat'],geo_list[closest]['geo']['lon']),
            map: map,
            title: geo_list[closest]['title']
        });*/
        //google.maps.event.trigger(map, 'resize');
        //initMap();
    }
    //google.maps.event.trigger(googleMap, 'resize');
    //$.mobile.changePage( "#map-popup", { transition: "slideup", changeHash: false });
    
}

function textClick(event) {
    var minDist = 50;
    var closest = -1;
    var arrow = false;
    x = event.offsetX * window.devicePixelRatio;
    y = event.offsetY * window.devicePixelRatio;
    //console.log(event.offsetX);
    //console.log(event.offsetY);
    var i;
    for (i = 0; i < geo_list.length; i++) {
        if (Math.sqrt(Math.pow(x - geo_list[i]['pos']['x'], 2) + Math.pow(y - geo_list[i]['pos']['y'], 2)) < minDist) {
            arrow = true;
        }
    }
    //console.log(arrow);
    //console.log(text_list);
    if (!arrow) {
        //console.log('here');
        //console.log(event.offsetX);
        //console.log(event.offsetY);
        for (i = 0; i < text_list.length; i++) {
            //console.log(text_list[i]['boundaries']);
            if ((x <= text_list[i]['boundaries']['r']) && (x >= text_list[i]['boundaries']['l']) && (y >= text_list[i]['boundaries']['t']) && (y <= text_list[i]['boundaries']['b'])) {
                //console.log('here 2');
                closest = i;
            }
        }
    }
    //console.log(closest);
    console.log(text_list[closest]);
    console.log(closest);
    if (closest != -1) {
        if (Object.keys(overflow).indexOf(text_list[closest]['title']) != -1) {
            //console.log(Object.keys(overflow).indexOf(text_list[closest]['title']));
            console.log(geo_list);
            overflowId = geo_list[closest]['title'];
            $("body").pagecontainer("change", "#overflow-page", {transition: "slideup"});
        } else {
            currentInfo = closest;
            //console.log(geo_list[currentInfo]);
            $("body").pagecontainer("change", "#info-page", {transition: "slideup"});
        }
    }
}

function listView() {
    view = "list";
    $("body").pagecontainer("change", "#pagetwo", {transition: "flip"});
}

function radialView() {
    view = "radial";
    $("body").pagecontainer("change", "#pageone", {transition: "flip"});
}

function mainLeft() {
    //reset settings checkboxes to current docs
    $(':checkbox').each(function() {
        $(this).prop('checked', false);
    });
    /*for (i=0; i < cbList.length; i ++) {
        cbList[i].prop('checked', false);
    }*/
    var tempDocs = localStorage['docs'].split(',');
    for (i=0; i < tempDocs.length; i ++) {
        $('#' + tempDocs[i]).prop('checked', true);
    }

    if (view == "radial") {
        $("body").pagecontainer("change", "#pageone", {transition: "slide", reverse:true});
    } else {
        $("body").pagecontainer("change", "#pagetwo", {transition: "slide", reverse:true});
    }
}

function mainDown() {
    if (view == "radial") {
        $("body").pagecontainer("change", "#pageone", {transition: "slideup", reverse:true});
    } else {
        $("body").pagecontainer("change", "#pagetwo", {transition: "slideup", reverse:true});
    }
}

function loadOverflowInfo(text) {
    console.log(text);
    $("#overflow-info").text(overflow[overflowId][text]['info']);
}

function ovMapLoad(id) {
    localStorage.setItem('thisLat', overflow[overflowId][id]["geo"]["lat"]);
    localStorage.setItem('thisLon', overflow[overflowId][id]["geo"]["lon"]);
    localStorage.setItem('thisTitle', id);
    $("body").pagecontainer("change", "#overflow-map-popup", {transition: "slideup"});
}

function loadInfo(text) {
    console.log(text);
    for (i = 0; i < geo_list.length; i ++) {
        if (geo_list[i]['title'] == text) {
            currentInfo = i;
            $("#info-para").text(geo_list[i]['info']);
        }
    }
}

function mapLoad(id) {
    for (i = 0; i < geo_list.length; i ++) {
        if (geo_list[i]['title'] == id) {
            localStorage.setItem('thisLat', geo_list[i]["geo"]["lat"]);
            localStorage.setItem('thisLon', geo_list[i]["geo"]["lon"]);
            localStorage.setItem('thisTitle', id);
            $("body").pagecontainer("change", "#map-popup", {transition: "slideup"});
        }
    }
}

$(document).on("pageshow", "#map-popup", function() {
    $("#map-popup").height(window.innerHeight);
    $("#button-div").height(window.innerHeight*0.1);
    $("#googleMap").height(window.innerHeight*.9);
    var mapProp = {
            center:new google.maps.LatLng(localStorage['thisLat'],localStorage['thisLon']),
            zoom:15,
            mapTypeId:google.maps.MapTypeId.ROADMAP
        };
    var map=new google.maps.Map(document.getElementById("googleMap"), mapProp);
    var directionsDisplay = new google.maps.DirectionsRenderer();
    var directionsService = new google.maps.DirectionsService();
    directionsDisplay.setMap(map);
    var request = {
        origin: new google.maps.LatLng(localStorage['lat'], localStorage['lon']),
        destination: new google.maps.LatLng(localStorage['thisLat'], localStorage['thisLon']),
        travelMode: google.maps.TravelMode.WALKING
    };

    directionsService.route(request, function(result, status) {
        if (status == google.maps.DirectionsStatus.OK) {
          directionsDisplay.setDirections(result);
        }
    });

    /*var marker = new google.maps.Marker({
        position: new google.maps.LatLng(localStorage['thisLat'],localStorage['thisLon']),
        map: map,
        title: localStorage.getItem('thisTitle')
    });*/
    
    //console.log(localStorage['latLon']['lat']);
});

$(document).on("pagebeforeshow", "#info-page", function() {
    console.log(geo_list[currentInfo]['info']);
    $("#info-para").text(geo_list[currentInfo]['info']);
});

$(document).on("pagebeforeshow", "#overflow-page", function() {
    $("#overflow-table tr").remove();
    //var temp_str = '';
    //make a table probably
    for (var i = 0; i < Object.keys(overflow[overflowId]).length; i++) {
        //console.log('key: ' + Object.keys(overflow[overflowId])[i]);
        txt = Object.keys(overflow[overflowId])[i];
        $('#overflow-table').append('<tr><td><a href="#overflow-info-page" data-transition="slide" onClick="loadOverflowInfo(this.text)">' + Object.keys(overflow[overflowId])[i] + '</a><button class="ui-button" data-inline="true" data-icon="arrow-u-r" id="' + txt + '" onClick="ovMapLoad(this.id)">map</button></td></tr>');
        //$('#overflow-table').append('<tr><td><p>hello</p></td></tr>');
        //temp_str += overflow[overflowId][i] + '\n';
        //txt = "#" + Object.keys(overflow[overflowId])[i];
        //$(txt).button();
        //$("#" + txt).button();
        //button = document.getElementById(txt);
        //button.button();
        $("#overflow-table").trigger("create");
    }

    //$("#overflow-para").text(temp_str);
});

$(document).on("pageshow", "#overflow-map-popup", function() {
    $("#overflow-map-popup").height(window.innerHeight);
    $("#ov-button-div").height(window.innerHeight*0.1);
    $("#googleMapOv").height(window.innerHeight*.9);
    var mapProp = {
            center:new google.maps.LatLng(localStorage['thisLat'],localStorage['thisLon']),
            zoom:15,
            mapTypeId:google.maps.MapTypeId.ROADMAP
        };
    var map=new google.maps.Map(document.getElementById("googleMapOv"), mapProp);
    var directionsDisplay = new google.maps.DirectionsRenderer();
    var directionsService = new google.maps.DirectionsService();
    directionsDisplay.setMap(map);
    var request = {
        origin: new google.maps.LatLng(localStorage['lat'], localStorage['lon']),
        destination: new google.maps.LatLng(localStorage['thisLat'], localStorage['thisLon']),
        travelMode: google.maps.TravelMode.WALKING
    };

    directionsService.route(request, function(result, status) {
        if (status == google.maps.DirectionsStatus.OK) {
          directionsDisplay.setDirections(result);
        }
    });

    /*var marker = new google.maps.Marker({
        position: new google.maps.LatLng(localStorage['thisLat'],localStorage['thisLon']),
        map: map,
        title: localStorage.getItem('thisTitle')
    });*/
    
    //console.log(localStorage['latLon']['lat']);
});

/*$(document).on("pagebeforeshow", "#overflow-info-page", function() {
    console.log(geo_list[currentInfo]['info']);
    $("#overflow-info").text(geo_list[currentInfo]['info']);
});*/

$("#docs-form").submit(function(event) {
    var temp_docs = $(this).serializeArray();
    //console.log(docs[0]);
    var temp_txt = '';
    var i;
    if (temp_docs.length > 0) {
        temp_txt += temp_docs[0]['name'];
        for (i = 1; i < temp_docs.length; i++) {
            temp_txt += ',' + temp_docs[i]['name'];
        }
    }
    localStorage['docs'] = temp_txt;
    event.preventDefault();
});