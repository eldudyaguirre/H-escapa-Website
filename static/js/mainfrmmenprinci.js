/*==================== SHOW NAVBAR ====================*/
document.addEventListener('DOMContentLoaded', function(){

    const toggleBtn = document.getElementById('header-toggle')
    const nav = document.getElementById('navbar')

    if(toggleBtn && nav){
        toggleBtn.addEventListener('click', function(){
            nav.classList.toggle('show-menu')
            toggleBtn.classList.toggle('bx-x')
        })
    }

})

/*==================== LINK ACTIVE ====================*/
const linkColor = document.querySelectorAll('.nav__link')

function colorLink(){
    linkColor.forEach(l => l.classList.remove('active'))
    this.classList.add('active')
}

linkColor.forEach(l => l.addEventListener('click', colorLink))

document.addEventListener('DOMContentLoaded', function(){
    showMenu('header-toggle','navbar')
})

