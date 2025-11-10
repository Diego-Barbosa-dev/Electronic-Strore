// Cuenta regresiva para el mini evento de descuento en index.html
// Este script actualiza el elemento #countdown-timer si existe en la página.

// Comentarios añadidos: el archivo contiene varias responsabilidades pequeñas:
// - Inicialización del menú y la cuenta regresiva
// - Gestión del theme (dark/light)
// - Lógica de cálculo de precios y botones de compra

(function(){
	// Tiempo del evento: 24 horas desde la carga (puedes cambiarlo a una fecha fija)
	const EVENT_DURATION_MS = 24 * 60 * 60 * 1000; // 24 horas

	function startCountdown(deadlineTimestamp){
		const el = document.getElementById('countdown-timer');
		if(!el) return; // nada que hacer si elemento no existe

	// update() calcula la diferencia entre la fecha límite y ahora,
	// formatea HH:MM:SS y actualiza el texto del elemento.
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
        
		// --- Theme toggle (dark/light) ---
		const themeToggle = document.getElementById('theme-toggle');
		function applyTheme(theme){
			if(theme === 'dark') document.documentElement.setAttribute('data-theme','dark');
			else document.documentElement.removeAttribute('data-theme');
			try{ localStorage.setItem('site-theme', theme); }catch(e){}
		}
		// Inicializar desde preferencia
		const saved = (function(){ try{ return localStorage.getItem('site-theme') }catch(e){return null} })();
		if(saved) applyTheme(saved);
		else {
			// comprobar preferencia del sistema
			const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
			if(prefersDark) applyTheme('dark');
		}
		if(themeToggle){
			themeToggle.addEventListener('click', function(){
				const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
				applyTheme(isDark ? 'light' : 'dark');
			});
		}

	// --- Scroll reveal using IntersectionObserver ---
		const revealEls = document.querySelectorAll('.reveal-on-scroll');
		if(revealEls.length){
			const obs = new IntersectionObserver((entries)=>{
				entries.forEach(ent=>{
					if(ent.isIntersecting){
						ent.target.classList.add('reveal');
						obs.unobserve(ent.target);
					}
				});
			}, { threshold: 0.12 });
			revealEls.forEach(el=>obs.observe(el));
		}

		// --- Mobile: si la pantalla es pequeña, abrir menú a pantalla completa ---
		function ensureMobileMenuBehavior(){
			const isMobile = window.innerWidth <= 700;
			if(isMobile){
				// cuando el menú se abre, aplicar clase mobile-open
				const origOpen = openMenu;
				openMenu = function(){ menu.classList.add('open','mobile-open'); menu.setAttribute('aria-hidden','false'); const first = menu.querySelector('.menu-item'); if(first) first.focus(); };
				const origClose = closeMenu;
				closeMenu = function(){ menu.classList.remove('open','mobile-open'); menu.setAttribute('aria-hidden','true'); menuButton.focus(); };
			}
		}
		// llamar una vez y en resize
		ensureMobileMenuBehavior();
		window.addEventListener('resize', ensureMobileMenuBehavior);
	}

	if(document.readyState === 'loading'){
		document.addEventListener('DOMContentLoaded', initMenuAndCountdown);
	} else {
		initMenuAndCountdown();
	}

})();


// Código movido desde index.html: gestión de precios y botones del evento de descuento
(function(){
	// Precio base en pesos colombianos
	const basePrice = 30000000;
	const fmt = new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 });

	const elOriginal = document.getElementById('price-original');
	const elFinal = document.getElementById('price-final');
	const elSavings = document.getElementById('price-savings');
	const select = document.getElementById('discount-select');
	const buyBtn = document.getElementById('buy-now');

	function updatePrices(){
		if(!select || !elOriginal || !elFinal || !elSavings) return;
		const pct = Number(select.value) / 100;
		const discounted = Math.round(basePrice * (1 - pct));
		const savings = basePrice - discounted;
		elOriginal.textContent = fmt.format(basePrice);
		elFinal.textContent = fmt.format(discounted);
		elSavings.textContent = `Ahorras ${fmt.format(savings)} (${select.value}%)`;
	}

	// Init cuando el DOM esté listo
	function initDiscountControls(){
		updatePrices();
		if(select) select.addEventListener('change', updatePrices);
		if(buyBtn){
			buyBtn.addEventListener('click', function(){
				alert('Has seleccionado la laptop con ' + (select ? select.value : '') + '% de descuento. Precio final: ' + (elFinal ? elFinal.textContent : ''));
			});
		}

		const addToCartBtn = document.getElementById('add-to-cart');
		if(addToCartBtn){
			addToCartBtn.addEventListener('click', function(){
				alert('carrito agregado');
			});
		}
	}

	if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initDiscountControls);
	else initDiscountControls();

})();
