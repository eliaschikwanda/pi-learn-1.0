document.addEventListener('click',menuButton);
function menuButton(){
    let menu = document.getElementById('menu-btn');
    menu.classList.toggle('fa-times');
    let navbar = document.getElementById('navbar-1');
    navbar.classList.toggle('activate');
}



