var xValues = ["dimanche", "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche", "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche", "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche", "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi"];

new Chart("myChart", {
  type: "line",
  data: {
    labels: xValues,
    datasets: [{
      data: [8, 3, 32, 42, 15, 30, 21, 9, 13, 5, 29, 38, 4, 1, 15, 16, 40, 37, 32, 29, 28, 10, 5, 10, 15, 20, 25, 15],
      borderColor: "brown",
      fill: false
    }, {
      data: [11, 37, 43, 12, 12, 15, 2, 9, 17, 23, 39, 25, 11, 07, 12, 16, 02, 45, 32, 12, 28, 7, 32, 9, 2, 14, 20, 11],
      borderColor: "orange",
      fill: false
    }]
  },
  options: {
    legend: { display: false }
  }
});
var xValuess = ["Mode Femme", "Mode Homme", "TV", "Parfums", "Pc"];
var yValuess = [33, 22, 17, 14, 14];
var barColorss = [
  "#b91d47",
  "#00aba9",
  "#2b5797",
  "#e8c3b9",
  "#1e7145"
];

new Chart("myChartt", {
  type: "pie",
  data: {
    labels: xValuess,
    datasets: [{
      backgroundColor: barColorss,
      data: yValuess
    }]
  },
  options: {
    title: {
      display: true,
      text: "Top 5 Produits"
    }
  }
});

var mybutton = document.getElementById("myBtn");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function () { scrollFunction() };

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}

/*var xArray = ["Alger", "TiziOuzou", "Adrar", "Blida"];
var yArray = [36, 9, 16, 08];
 
var data = [{
  x:xArray,
  y:yArray,
  type:"bar"
}];
 
var layout = {title:"Nombre des produits non livrés "};
 
Plotly.newPlot("myPlot", data, layout);*/


function testAjax(a, b) {

  $.ajax('/pfc/?a=' + a + '&b=' + b, '&c=' + c, '&d' + d,
    {
      dataType: 'json',
      timeout: 240000,     // timeout milliseconds
      success: function (data, status, xhr) {   // success callback function
        alert("ok");
      },

    });


}


function yesnoCheck() {
  if (document.getElementById('flexRadioDefault1').checked) {
    document.getElementById('ifYes').style.display = 'none';
  } else {
    document.getElementById('ifYes').style.display = 'block';
  }
}
function startTime() {
  const today = new Date();
  let h = today.getHours();
  let m = today.getMinutes();
  let s = today.getSeconds();
  m = checkTime(m);
  s = checkTime(s);
  // document.getElementById('txt').innerHTML =  h + ":" + m + ":" + s;
  document.getElementById('h').innerHTML= h + ":        "+m + ":         "+s 


  setTimeout(startTime, 1000);
}

function checkTime(i) {
  if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
  return i;
}

var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
var yyyy = today.getFullYear();

today = mm + '/' + dd + '/' + yyyy;
document.getElementById('dd').innerHTML=dd+"    "+mm+"  "+yyyy+"   "

