/*==================== SHOW NAVBAR ====================*/
const showMenu = (headerToggle, navbarId) => {
    const toggleBtn = document.getElementById(headerToggle);
    const nav = document.getElementById(navbarId);
    if (toggleBtn && nav) {
        // Use Font Awesome icons already loaded by Frm-MenPri.html.
        // Avoid mixing Boxicons' bx-menu and bx-x classes, which can render
        // as a missing-glyph box on some responsive browsers.
        const setToggleIcon = (isOpen) => {
            toggleBtn.classList.remove('bx', 'bx-menu', 'bx-x');
            toggleBtn.classList.add('fa-solid', isOpen ? 'fa-xmark' : 'fa-bars');
            toggleBtn.setAttribute('aria-label', isOpen ? 'Cerrar menú' : 'Abrir menú');
            toggleBtn.setAttribute('role', 'button');
            toggleBtn.setAttribute('tabindex', '0');
            toggleBtn.setAttribute('aria-expanded', String(isOpen));
        };

        setToggleIcon(nav.classList.contains('show-menu'));
        const toggleMenu = () => {
            const isOpen = nav.classList.toggle('show-menu');
            setToggleIcon(isOpen);
        };
        toggleBtn.addEventListener('click', toggleMenu);
        toggleBtn.addEventListener('keydown', (event) => {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                toggleMenu();
            }
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
