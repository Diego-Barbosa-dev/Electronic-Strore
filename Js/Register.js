/* ========================================
   Script del REGISTRO
   ======================================== */

   document.addEventListener("DOMContentLoaded", () => {
    const registerForm = document.getElementById("registerForm");
  
    registerForm.addEventListener("submit", (e) => {
      e.preventDefault();
  
      const name = document.getElementById("name").value.trim();
      const email = document.getElementById("email").value.trim();
      const address = document.getElementById("address").value.trim();
      const phone = document.getElementById("phone").value.trim();
      const password = document.getElementById("password").value.trim();
  
      if (!name || !email || !address || !phone || !password) {
        alert("⚠️ Por favor, completa todos los campos.");
        return;
      }
  
      // Simulación de registro exitoso
      alert(`✅ Registro exitoso, bienvenido ${name}`);
      window.location.href = "login.html";
    });
  });
  