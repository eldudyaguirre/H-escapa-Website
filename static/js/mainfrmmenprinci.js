/*==================== SHOW NAVBAR ====================*/
const showMenu = (headerToggle, navbarId) => {
    const toggleBtn = document.getElementById(headerToggle);
    const nav = document.getElementById(navbarId);
    if (toggleBtn && nav) {
        toggleBtn.addEventListener('click', () => {
            nav.classList.toggle('show-menu');
            toggleBtn.classList.toggle('bx-x');
        });
    }
};
showMenu('header-toggle', 'navbar');

/*==================== ACTIVE MENU STATE ====================*/
const nav = document.getElementById('navbar');
if (nav) {
    const mainLinks = nav.querySelectorAll('.nav__link');
    const submenuItems = nav.querySelectorAll('.nav__dropdown-item');

    function clearActiveMenu() {
        nav.querySelectorAll('.active, [aria-current="page"]').forEach(el => {
            el.classList.remove('active');
            el.removeAttribute('aria-current');
        });
    }
    function activateSubmenu(item) {
        clearActiveMenu();
        item.classList.add('active');
        item.setAttribute('aria-current', 'page');
        const dropdown = item.closest('.nav__dropdown');
        if (dropdown) {
            dropdown.classList.add('show-dropdown');
            const parent = dropdown.querySelector(':scope > .nav__link');
            if (parent) {
                parent.classList.add('active');
                parent.setAttribute('aria-current', 'page');
            }
        }
    }
    function activateMain(link) {
        clearActiveMenu();
        link.classList.add('active');
        link.setAttribute('aria-current', 'page');
    }

    // Rutas que antes estaban como # en el menú.
    submenuItems.forEach(item => {
        const label = item.textContent.trim().toLocaleLowerCase('es');
        if (label === 'pacientes') item.href = '/homein-pacientes/';
    });
    mainLinks.forEach(link => {
        const label = link.textContent.trim().replace(/\s+/g, ' ').toLocaleLowerCase('es');
        if (label === 'agendar cita') link.href = '/homein-nuevacita/';
    });

    const currentPath = location.pathname.replace(/\/$/, '') || '/';
    let found = false;
    submenuItems.forEach(item => {
        const href = item.getAttribute('href');
        if (!href || href === '#') return;
        const path = new URL(href, location.origin).pathname.replace(/\/$/, '') || '/';
        if (path === currentPath) { activateSubmenu(item); found = true; }
    });
    if (!found) {
        mainLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (!href || href === '#') return;
            const path = new URL(href, location.origin).pathname.replace(/\/$/, '') || '/';
            if (path === currentPath) { activateMain(link); found = true; }
        });
    }

    mainLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (!link.closest('.nav__dropdown') && link.getAttribute('href') !== '#') activateMain(link);
        });
    });
    submenuItems.forEach(item => item.addEventListener('click', () => activateSubmenu(item)));
}
