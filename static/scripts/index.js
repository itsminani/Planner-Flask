var root = document.querySelector(":root");
function setColor(i) {
  localStorage.setItem("--primary", i);
  root.style.setProperty("--primary", i);
}

function setStorage() {
  let mainColor = localStorage.getItem("--primary");
  setColor(mainColor);
}
if (localStorage.getItem("--primary") === null) {
  console.log("First Timer");
} else {
  setStorage();
}

// Handle colors for the app
window.onload = function () {
  // input Handler
  let input = document.querySelector("#exampleColorInput");
  input.addEventListener("change", function (e) {
    setColor(input.value);
  });

  //   Form Handler
  // document.querySelector("form").addEventListener("submit", function (e) {
  //   e.preventDefault();
  // });
};

// Trigger Flashing toast Notifier
const toastTrigger = document.getElementById('liveToastBtn')
const toastLiveExample = document.getElementById('liveToast')

if (toastLiveExample){
  const toast = new bootstrap.Toast(toastLiveExample)
  toast.show()
}