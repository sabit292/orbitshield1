let chart;

// yıldızlar
const canvas = document.getElementById("stars");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let stars = Array(150).fill().map(()=>({
    x:Math.random()*canvas.width,
    y:Math.random()*canvas.height
}));

function draw(){
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle="#00ffff";

    stars.forEach(s=>{
        ctx.fillRect(s.x,s.y,2,2);
        s.y+=0.3;
        if(s.y>canvas.height) s.y=0;
    });

    requestAnimationFrame(draw);
}
draw();

// detay
function details(kp){
    return {
        gps: kp>=5?"Risk":"Normal",
        sat: kp>=7?"Risk":"Normal",
        power: kp>=8?"Tehlike":"Normal"
    }
}

async function update(){
    const res = await fetch("/data");
    const d = await res.json();

    document.getElementById("kp").innerText = d.kp;
    document.getElementById("time").innerText = d.time;
    document.getElementById("pred").innerText = d.prediction;
    document.getElementById("region").innerText = d.region;

    document.getElementById("wind").innerText = d.solar_wind + " km/s";
    document.getElementById("flare").innerText = d.flare;

    let det = details(d.kp);
    document.getElementById("gps").innerText = det.gps;
    document.getElementById("sat").innerText = det.sat;
    document.getElementById("power").innerText = det.power;

    // alarm
    if(d.risk==="HIGH"||d.risk==="EXTREME"){
        new Audio("https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg").play();
    }

    // grafik
    if(chart) chart.destroy();

    chart = new Chart(document.getElementById("chart"), {
        type:'line',
        data:{
            labels:d.history.map((_,i)=>i),
            datasets:[{
                data:d.history,
                borderColor:"#00ffff",
                tension:0.4
            }]
        }
    });
}

setInterval(update,4000);
update();