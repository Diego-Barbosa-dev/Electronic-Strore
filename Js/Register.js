/* ========================================
   Script del REGISTRO
   ======================================== */

  document.addEventListener("DOMContentLoaded", () => {
    // Inicializar tema (si el usuario ya seleccionó dark/light en la página principal)
    (function(){
      function applyTheme(theme){
        if(theme === 'dark') document.documentElement.setAttribute('data-theme','dark');
        else document.documentElement.removeAttribute('data-theme');
      }
      var saved = null;
      try{ saved = localStorage.getItem('site-theme'); }catch(e){ saved = null; }
      if(saved) applyTheme(saved);
      else {
        // Si no hay preferencia guardada, respetar la preferencia del sistema
        try{
          var prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
          if(prefersDark) applyTheme('dark');
        }catch(e){}
      }
    })();
    const registerForm = document.getElementById("registerForm");
  
      const nameInput = document.getElementById('name');
      const emailInput = document.getElementById('email');
      const addressInput = document.getElementById('address');
      const phoneInput = document.getElementById('phone');
      const passwordInput = document.getElementById('password');

      const nameError = document.getElementById('name-error');
      const emailError = document.getElementById('email-error');
      const addressError = document.getElementById('address-error');
      const phoneError = document.getElementById('phone-error');
      const passwordError = document.getElementById('password-error');
      //validación del nombre
      function validateName(){
        const v = nameInput.value.trim();
        if(!v) { nameError.textContent = 'El nombre es obligatorio.'; return false; }
        nameError.textContent = '';
        return true;
      }
      //validación del correo
      function validateEmail(){
        const v = emailInput.value.trim();
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if(!v) { emailError.textContent = 'El correo es obligatorio.'; return false; }
        if(!re.test(v)) { emailError.textContent = 'Introduce un correo válido.'; return false; }
        emailError.textContent = '';
        return true;
      }
      //validación de la dirección
      function validateAddress(){
        const v = addressInput.value.trim();
        if(!v){ addressError.textContent = 'La dirección es obligatoria.'; return false; }
        addressError.textContent = '';
        return true;
      }
      //validación del teléfono
      function validatePhone(){
        const v = phoneInput.value.trim();
        const digits = v.replace(/[^0-9]/g,'');
        if(!v){ phoneError.textContent = 'El teléfono es obligatorio.'; return false; }
        if(digits.length < 7){ phoneError.textContent = 'Número demasiado corto.'; return false; }
        phoneError.textContent = '';
        return true;
      }
      //validación de la contraseña
      function validatePassword(){
        const v = passwordInput.value;
        if(!v){ passwordError.textContent = 'La contraseña es obligatoria.'; return false; }
        if(v.length < 6){ passwordError.textContent = 'La contraseña debe tener al menos 6 caracteres.'; return false; }
        passwordError.textContent = '';
        return true;
      }

      // Real-time validation
      nameInput.addEventListener('input', validateName);
      emailInput.addEventListener('input', validateEmail);
      addressInput.addEventListener('input', validateAddress);
      phoneInput.addEventListener('input', validatePhone);
      passwordInput.addEventListener('input', validatePassword);

      registerForm.addEventListener('submit', function(e){
        e.preventDefault();
        const ok = [validateName(), validateEmail(), validateAddress(), validatePhone(), validatePassword()].every(Boolean);
        if(!ok){
          alert('Revisa los campos en rojo antes de enviar.');
          return;
        }
        // Determinar base de la API.
        // Si la página ya está servida desde el backend (puerto 5000) usamos rutas relativas,
        // en caso contrario (file:// o servidor estático en otro puerto) apuntamos a 127.0.0.1:5000.
        let API_BASE = 'http://127.0.0.1:5000';

        // Enviar datos al backend mediante fetch a la ruta /api/users/register
        // Construimos el payload con los campos requeridos por la API.
        const payload = {
          name: nameInput.value.trim(),
          email: emailInput.value.trim(),
          password: passwordInput.value
        };

        // Petición POST con JSON. La API devuelve 201 en caso de éxito.
        fetch(API_BASE + '/api/users/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        }).then(async (res) => {
          if(res.status === 201){
            // Registro correcto: redirigimos al login.
            alert('✅ Registro exitoso, por favor inicia sesión');
            window.location.href = 'login.html';
            return;
          }
          // Si no fue 201 intentamos leer el error devuelto por la API
          const data = await res.json().catch(()=>({}));
          alert('Error: ' + (data.error || 'No se pudo registrar'));
        }).catch((err)=>{
          // Error de red o la API no está accesible
          console.error(err);
          alert('Error de red al contactar la API.');
        });
      });
  });
  