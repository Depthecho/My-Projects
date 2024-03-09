function darkmode(){
    console.log('Dark mode')
    const body = document.body
    const wasDarkmode = localStorage.getItem("darkmode") == "true"
    if (localStorage.getItem("darkmode") == "true"){
    document.getElementsByClassName("swap-theme")[0].children[0].classList.toggle('fa-sun')
    document.getElementsByClassName("swap-theme")[0].children[0].classList.toggle('fa-moon')
    }else{
    document.getElementsByClassName("swap-theme")[0].children[0].classList.toggle('fa-moon')
    document.getElementsByClassName("swap-theme")[0].children[0].classList.toggle('fa-sun')
    }

    localStorage.setItem("darkmode", !wasDarkmode)
    body.classList.toggle('dark-mode', !wasDarkmode)
}

 if ((window.location.href.split('/')[3] + window.location.href.split('/')[4]) === "settings?setting=appearance"
     || window.location.href.split('/')[3] === "login" || window.location.href.split('/')[3] === "signup" ||
     window.location.href.split('/')[3] === "password-reset" || window.location.href.split('/')[3] === "password-reset-confirm"){
    document.querySelector('.swap-theme').addEventListener('click', darkmode)
    }


function onload(){
if (localStorage.getItem("darkmode") == "true"){
    if ((window.location.href.split('/')[3] + window.location.href.split('/')[4]) === "settings?setting=appearance"
     || window.location.href.split('/')[3] === "login" || window.location.href.split('/')[3] === "signup" ||
     window.location.href.split('/')[3] === "password-reset" || window.location.href.split('/')[3] === "password-reset-confirm"){
        document.getElementsByClassName("swap-theme")[0].children[0].classList.toggle('fa-sun')
        document.getElementsByClassName("swap-theme")[0].children[0].classList.toggle('fa-moon')
        }
    }
    document.body.classList.toggle('dark-mode', localStorage.getItem('darkmode') == 'true')
}
document.addEventListener('DOMContentLoaded', onload)


        // Function to toggle dropdown menu visibility
        //function toggleDropdown() {
            //var dropdownMenu = document.getElementById("dropdownMenu");
            //var dropdownMenuButton = document.getElementById("burger-button");
            //if (dropdownMenu.style.display === "block") {
                //dropdownMenu.style.display = "none";
                //dropdownMenuButton.style.setProperty("color", "white", "important")
            //} else {
                //dropdownMenu.style.display = "block";
                //dropdownMenuButton.style.setProperty("color", "var(--main-light-theme-color)", "important")
        //}
        //document.getElementById('burger-button').addEventListener('click', function () {
   //if (this.style.color === "white") {
      //this.style.color === "var(--main-light-theme-color)"
   //} else {
      //this.style.color === "white"
   //}
//});