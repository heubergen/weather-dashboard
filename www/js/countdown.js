const y = document.getElementsByClassName("countdown")

for (let item of y) {
  printCountdown(item);
}
  function printCountdown(item){
    var elementDate = new Date(item.dataset.time).getTime();
    //console.log(elementDate);
    function calccount() {
      // Calculate the difference between now and the count down date
      var distance = elementDate - Date.now();

      // Time calculations for days, hours and minutes
      var days = Math.floor(distance / (1000 * 60 * 60 * 24));
      var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));

      // Draw result
      item.innerHTML = days + "d " + hours + "h " + minutes + "m ";

      // Handle if countdown is finished
      if (distance < 0) {
        clearInterval(x);
        item.innerHTML = "REACHED";
      }
    }
    // Call function immediately and then every minute
    calccount();
    var x = setInterval(calccount, 60000);
  }
