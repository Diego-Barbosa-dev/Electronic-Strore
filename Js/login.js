/* ========================================
   Script del LOGIN
   ======================================== */

   document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");
  
    loginForm.addEventListener("submit", (e) => {
      e.preventDefault();
  
      const email = document.getElementById("email").value.trim();
      const password = document.getElementById("password").value.trim();
  
      if (!email || !password) {
        alert("⚠️ Por favor, complete todos los campos.");
        return;
      }
  
      // Enviar credenciales al backend para autenticar al usuario.
      // Se espera que la API responda 200 en caso de éxito.
      const payload = { email, password };
      fetch('/api/users/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      }).then(async (res) => {
        if(res.status === 200){
          // Inicio de sesión correcto. Podríamos guardar un token o la info del usuario.
          const data = await res.json().catch(()=>({}));
          alert('✅ Inicio de sesión correcto');
          // EJEMPLO: guardar el usuario en sessionStorage (opcional)
          // sessionStorage.setItem('user', JSON.stringify(data.user));
          window.location.href = 'index.html';
          return;
        }
        // Si no fue 200 mostramos el mensaje de error (si existe)
        const d = await res.json().catch(()=>({}));
        alert('Error: ' + (d.error || 'Credenciales inválidas'));
      }).catch((err)=>{
        // Error de red o la API no disponible
        console.error(err);
        alert('Error de red al contactar la API.');
      });
    });
  });
  