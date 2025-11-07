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
  
      // Simulación de login exitoso
      alert(`✅ Bienvenido, ${email}`);
      window.location.href = "register.html";
    });
  });
  