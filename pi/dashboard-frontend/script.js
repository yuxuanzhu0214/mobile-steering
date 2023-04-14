// METER

let Meter = function Meter($elm, config) {

  // DOM
  let $needle, $value;

  // Others

  let steps = (config.valueMax - config.valueMin) / config.valueStep,
  angleStep = (config.angleMax - config.angleMin) / steps;

  let margin = 10; // in %
  let angle = 0; // in degrees

  let value2angle = function (value) {
    let angle = value / (config.valueMax - config.valueMin) * (config.angleMax - config.angleMin) + config.angleMin;

    return angle;
  };

  this.setValue = function (v) {
    $needle.style.transform = "translate3d(-50%, 0, 0) rotate(" + Math.round(value2angle(v)) + "deg)";
    $value.innerHTML = config.needleFormat(v);
  };

  let switchLabel = function (e) {
    e.target.closest(".meter").classList.toggle('meter--big-label');
  };

  let makeElement = function (parent, className, innerHtml, style) {

    let e = document.createElement('div');
    e.className = className;

    if (innerHtml) {
      e.innerHTML = innerHtml;
    }

    if (style) {
      for (var prop in style) {
        e.style[prop] = style[prop];
      }
    }

    parent.appendChild(e);

    return e;
  };

  // Label unit
  makeElement($elm, "label label-unit", config.valueUnit);

  for (let n = 0; n < steps + 1; n++) {
    let value = config.valueMin + n * config.valueStep;
    angle = config.angleMin + n * angleStep;

    // Graduation numbers

    // Red zone
    let redzoneClass = "";
    if (value > config.valueRed) {
      redzoneClass = " redzone";
    }

    makeElement($elm, "grad grad--" + n + redzoneClass, config.labelFormat(value), {
      left: 50 - (50 - margin) * Math.sin(angle * (Math.PI / 180)) + "%",
      top: 50 + (50 - margin) * Math.cos(angle * (Math.PI / 180)) + "%" });


    // Tick
    makeElement($elm, "grad-tick grad-tick--" + n + redzoneClass, "", {
      left: 50 - 50 * Math.sin(angle * (Math.PI / 180)) + "%",
      top: 50 + 50 * Math.cos(angle * (Math.PI / 180)) + "%",
      transform: "translate3d(-50%, 0, 0) rotate(" + (angle + 180) + "deg)" });


    // Half ticks
    angle += angleStep / 2;

    if (angle < config.angleMax) {
      makeElement($elm, "grad-tick grad-tick--half grad-tick--" + n + redzoneClass, "", {
        left: 50 - 50 * Math.sin(angle * (Math.PI / 180)) + "%",
        top: 50 + 50 * Math.cos(angle * (Math.PI / 180)) + "%",
        transform: "translate3d(-50%, 0, 0) rotate(" + (angle + 180) + "deg)" });

    }

    // Quarter ticks
    angle += angleStep / 4;

    if (angle < config.angleMax) {
      makeElement($elm, "grad-tick grad-tick--quarter grad-tick--" + n + redzoneClass, "", {
        left: 50 - 50 * Math.sin(angle * (Math.PI / 180)) + "%",
        top: 50 + 50 * Math.cos(angle * (Math.PI / 180)) + "%",
        transform: "translate3d(-50%, 0, 0) rotate(" + (angle + 180) + "deg)" });

    }

    angle -= angleStep / 2;

    if (angle < config.angleMax) {
      makeElement($elm, "grad-tick grad-tick--quarter grad-tick--" + n + redzoneClass, "", {
        left: 50 - 50 * Math.sin(angle * (Math.PI / 180)) + "%",
        top: 50 + 50 * Math.cos(angle * (Math.PI / 180)) + "%",
        transform: "translate3d(-50%, 0, 0) rotate(" + (angle + 180) + "deg)" });

    }
  }

  // NEEDLE

  angle = value2angle(config.value);

  $needle = makeElement($elm, "needle", "", {
    transform: "translate3d(-50%, 0, 0) rotate(" + angle + "deg)" });


  let $axle = makeElement($elm, "needle-axle").addEventListener("click", switchLabel);
  makeElement($elm, "label label-value", "<div>" + config.labelFormat(config.value) + "</div>" + "<span>" + config.labelUnit + "</span>").addEventListener("click", switchLabel);

  $value = $elm.querySelector(".label-value div");
};


// DOM LOADED FIESTA

document.addEventListener("DOMContentLoaded", function () {

  let rpmMeter = new Meter(document.querySelector(".meter--rpm"), {
    value: 6.3,
    valueMin: 0,
    valueMax: 8000,
    valueStep: 1000,
    valueUnit: "<div>RPM</div><span>x1000</span>",
    angleMin: 30,
    angleMax: 330,
    labelUnit: "RPM",
    labelFormat: function (v) {return Math.round(v / 1000);},
    needleFormat: function (v) {return Math.round(v / 100) * 100;},
    valueRed: 6500 });


  let speedMeter = new Meter(document.querySelector(".meter--speed"), {
    value: 203,
    valueMin: 0,
    valueMax: 220,
    valueStep: 20,
    valueUnit: "<span>Speed</span><div>Km/h</div>",
    angleMin: 30,
    angleMax: 330,
    labelUnit: "Km/h",
    labelFormat: function (v) {return Math.round(v);},
    needleFormat: function (v) {return Math.round(v);} });


  let gearMeter = document.querySelector('.meter--gear div');

  // MAIN LOOP
  let FPS = 10
  let interval = Math.floor(1000/FPS)
  setInterval(() => {
     // Update GUI
     fetch('http://localhost:3000/car')
     .then(response => response.json())
     .then(data => {
       gear = data.gear
       rpm = data.rpm
       speed = data.speed
       speedMeter.setValue(speed);
       rpmMeter.setValue(rpm);
       gearMeter.innerHTML = gear
      //  console.log(`RPS: ${rpm}, Gear: ${gear}, Speed: ${speed}`);
   })
   .catch(error => {
       console.error('Error fetching car data:', error);
   });
  }, interval);

});