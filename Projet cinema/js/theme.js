const themeToggle = document.getElementById("themeToggle");

// Appliquer le thème sauvegardé au chargement
if (localStorage.getItem("theme")) {
  document.documentElement.setAttribute("data-theme", localStorage.getItem("theme"));
}

// Changer le thème au clic
themeToggle.addEventListener("click", () => {
  const currentTheme = document.documentElement.getAttribute("data-theme");
  const newTheme = currentTheme === "dark" ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", newTheme);
  localStorage.setItem("theme", newTheme);
});
