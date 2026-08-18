(function () {
  "use strict";

  // ---- theme toggle -------------------------------------------------------
  var root = document.documentElement;
  var themeBtn = document.getElementById("themeToggle");
  if (themeBtn) {
    themeBtn.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      localStorage.setItem("bb-theme", next);
    });
  }

  // ---- mobile sidebar -----------------------------------------------------
  var sidebar = document.getElementById("sidebar");
  var toggle = document.getElementById("sidebarToggle");
  var scrim = null;

  function closeSidebar() {
    if (!sidebar) return;
    sidebar.classList.remove("is-open");
    if (scrim) { scrim.remove(); scrim = null; }
  }

  if (toggle && sidebar) {
    toggle.addEventListener("click", function () {
      if (sidebar.classList.contains("is-open")) return closeSidebar();
      sidebar.classList.add("is-open");
      scrim = document.createElement("div");
      scrim.className = "scrim";
      scrim.addEventListener("click", closeSidebar);
      document.body.appendChild(scrim);
    });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeSidebar();
  });

  // ---- flash messages: dismiss + auto-hide --------------------------------
  document.querySelectorAll(".flash").forEach(function (el) {
    var close = el.querySelector(".flash__close");
    var dismiss = function () {
      el.style.transition = "opacity .2s ease, transform .2s ease";
      el.style.opacity = "0";
      el.style.transform = "translateX(20px)";
      setTimeout(function () { el.remove(); }, 220);
    };
    if (close) close.addEventListener("click", dismiss);
    setTimeout(dismiss, 5000);
  });

  // ---- confirm destructive actions ----------------------------------------
  document.querySelectorAll("form[data-confirm]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      if (!window.confirm(form.getAttribute("data-confirm"))) e.preventDefault();
    });
  });

  // ---- auto-submit filter selects ----------------------------------------
  document.querySelectorAll("[data-autosubmit]").forEach(function (el) {
    el.addEventListener("change", function () { el.form.submit(); });
  });
})();
