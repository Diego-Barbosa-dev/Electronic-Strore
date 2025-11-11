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

    // Determinar base de la API
    let API_BASE = "http://127.0.0.1:5000";

    const payload = { email, password };

    fetch(API_BASE + "/api/users/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    })
      .then(async (res) => {
        if (res.status === 200) {
          const data = await res.json().catch(() => ({}));
          alert("✅ Inicio de sesión correcto");

          // Guardamos el usuario en sessionStorage para usarlo en el resto del sitio
          sessionStorage.setItem("user", JSON.stringify(data.user));

          window.location.href = "index.html";
          return;
        }

        const d = await res.json().catch(() => ({}));
        alert("Error: " + (d.error || "Credenciales inválidas"));
      })
      .catch((err) => {
        console.error(err);
        alert("Error de red al contactar la API.");
      });
  });
});
