/*==================== SHOW NAVBAR ====================*/
const showMenu = (headerToggle, navbarId) => {
    const toggleBtn = document.getElementById(headerToggle);
    const nav = document.getElementById(navbarId);
    if (toggleBtn && nav) {
        // El id puede estar en el propio <i> o en el contenedor del botón.
        // Siempre alternamos las clases en un único icono para evitar duplicados.
        const toggleIcon = toggleBtn.matches('i') ? toggleBtn : toggleBtn.querySelector('i');
        toggleBtn.setAttribute('aria-expanded', 'false');
        if (toggleBtn.tagName === 'BUTTON') {
            toggleBtn.setAttribute('aria-label', 'Abrir menú');
        }
        toggleBtn.addEventListener('click', () => {
            const opened = nav.classList.toggle('show-menu');
            if (toggleIcon) {
                toggleIcon.classList.toggle('bx-menu', !opened);
                toggleIcon.classList.toggle('bx-x', opened);
            }
            toggleBtn.setAttribute('aria-expanded', String(opened));
            if (toggleBtn.tagName === 'BUTTON') {
                toggleBtn.setAttribute('aria-label', opened ? 'Cerrar menú' : 'Abrir menú');
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
    const activeColor = 'var(--h-escapa3-color, #005855)';

    function clearActiveMenu() {
        nav.querySelectorAll('.active, [aria-current="page"]').forEach(el => {
            el.classList.remove('active');
            el.removeAttribute('aria-current');
        });
        // Quitar también los estilos inline aplicados a iconos y textos hijos.
        // Si no se limpian, conservan el color oscuro aunque el enlace ya no esté activo.
        nav.querySelectorAll('.nav__link, .nav__dropdown-item, .nav__icon, .nav__name').forEach(el => {
            el.style.removeProperty('color');
            el.style.removeProperty('font-weight');
            el.style.removeProperty('opacity');
            el.style.removeProperty('background-color');
        });
    }

    function highlight(element) {
        element.classList.add('active');
        element.setAttribute('aria-current', 'page');
        element.style.setProperty('color', activeColor, 'important');
        element.style.setProperty('font-weight', '600', 'important');
        element.querySelectorAll('.nav__icon, .nav__name').forEach(child => {
            child.style.setProperty('color', activeColor, 'important');
            child.style.setProperty('opacity', '1', 'important');
        });
    }

    function activateSubmenu(item) {
        clearActiveMenu();
        highlight(item);
        const dropdown = item.closest('.nav__dropdown');
        if (dropdown) {
            dropdown.classList.add('show-dropdown');
            const parent = dropdown.querySelector(':scope > .nav__link');
            if (parent) highlight(parent);
        }
    }

    function activateMain(link) {
        clearActiveMenu();
        highlight(link);
    }

    // Completar rutas de enlaces que estaban como marcadores.
    submenuItems.forEach(item => {
        const label = item.textContent.trim().replace(/\s+/g, ' ').toLocaleLowerCase('es');
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
        if (path === currentPath) {
            activateSubmenu(item);
            found = true;
        }
    });

    if (!found) {
        mainLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (!href || href === '#') return;
            const path = new URL(href, location.origin).pathname.replace(/\/$/, '') || '/';
            if (path === currentPath) {
                activateMain(link);
                found = true;
            }
        });
    }

    mainLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (!link.closest('.nav__dropdown') && link.getAttribute('href') !== '#') activateMain(link);
        });
    });
    submenuItems.forEach(item => item.addEventListener('click', () => activateSubmenu(item)));
}
