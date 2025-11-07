// Cuenta regresiva para el mini evento de descuento en index.html
// Este script actualiza el elemento #countdown-timer si existe en la página.

(function(){
	// Tiempo del evento: 24 horas desde la carga (puedes cambiarlo a una fecha fija)
	const EVENT_DURATION_MS = 24 * 60 * 60 * 1000; // 24 horas

	function startCountdown(deadlineTimestamp){
		const el = document.getElementById('countdown-timer');
		if(!el) return; // nada que hacer si elemento no existe

		function update(){
			const now = Date.now();
			let diff = deadlineTimestamp - now;
			if(diff <= 0){
				el.textContent = 'Expirado';
				clearInterval(timer);
				return;
			}

			const hours = Math.floor(diff / (1000*60*60));
			diff -= hours * (1000*60*60);
			const minutes = Math.floor(diff / (1000*60));
			diff -= minutes * (1000*60);
			const seconds = Math.floor(diff / 1000);

			// Formato HH:MM:SS
			const hh = String(hours).padStart(2,'0');
			const mm = String(minutes).padStart(2,'0');
			const ss = String(seconds).padStart(2,'0');
			el.textContent = `${hh}:${mm}:${ss}`;
		}

		update();
		const timer = setInterval(update, 1000);
	}

	// Esperar DOM
	function initMenuAndCountdown(){
		const deadline = Date.now() + EVENT_DURATION_MS;
		startCountdown(deadline);

		// --- Lógica del menú desplegable ---
		const menuButton = document.querySelector('button.nav-icon[aria-label="Abrir menú"]');
		const menu = document.getElementById('menu-dropdown');
		if(!menuButton || !menu) return;

		function openMenu(){
			menu.classList.add('open');
			menu.setAttribute('aria-hidden','false');
			// llevar foco al primer enlace
			const first = menu.querySelector('.menu-item');
			if(first) first.focus();
		}

		function closeMenu(){
			menu.classList.remove('open');
			menu.setAttribute('aria-hidden','true');
			menuButton.focus();
		}

		menuButton.addEventListener('click', function(e){
			e.stopPropagation();
			if(menu.classList.contains('open')) closeMenu(); else openMenu();
		});

		// Cerrar al hacer clic fuera
		document.addEventListener('click', function(ev){
			if(!menu.classList.contains('open')) return;
			if(ev.target.closest('#menu-dropdown')) return;
			if(ev.target.closest('button.nav-icon[aria-label="Abrir menú"]')) return;
			closeMenu();
		});

		// Cerrar con Escape y navegación con teclado
		document.addEventListener('keydown', function(ev){
			if(ev.key === 'Escape' && menu.classList.contains('open')){
				closeMenu();
			}
		});
	}

	if(document.readyState === 'loading'){
		document.addEventListener('DOMContentLoaded', initMenuAndCountdown);
	} else {
		initMenuAndCountdown();
	}

})();
