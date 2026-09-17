/*==================== SHOW NAVBAR ====================*/
const showMenu = (headerToggle, navbarId) =>{
    const toggleBtn = document.getElementById(headerToggle),
    nav = document.getElementById(navbarId)
    
    // Validate that variables exist
    if(headerToggle && navbarId && toggleBtn && nav){
        toggleBtn.addEventListener('click', ()=>{
            nav.classList.toggle('show-menu')
            toggleBtn.classList.toggle('bx-x')
        })
    }
}
showMenu('header-toggle','navbar')

/*==================== LINK ACTIVE ====================*/
const linkColor = document.querySelectorAll('.nav__link')
function colorLink(){
    linkColor.forEach(l => l.classList.remove('active'))
    this.classList.add('active')
}
linkColor.forEach(l => l.addEventListener('click', colorLink))

/*==================== PATIENTS MENU ROUTE ====================*/
document.querySelectorAll('.nav__dropdown-content .nav__dropdown-item').forEach(item => {
    if (item.textContent.trim().toLocaleLowerCase('es') === 'pacientes') {
        item.href = '/homein-pacientes/';
    }
});
