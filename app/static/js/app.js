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

  // ---- auto-fill a slug field from its named source field -----------------
  document.querySelectorAll("[data-slug-source]").forEach(function (slugField) {
    var source = document.getElementById(slugField.getAttribute("data-slug-source"));
    if (!source) return;
    var auto = !slugField.value;
    slugField.addEventListener("input", function () { auto = false; });
    source.addEventListener("input", function () {
      if (!auto) return;
      slugField.value = source.value
        .toLowerCase()
        .trim()
        .replace(/[^a-z0-9]+/g, "-")
        .replace(/(^-|-$)/g, "");
    });
  });

  // ---- motion: staggered entrance, count-up stats, chart draw-in ----------
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (!reduceMotion) {
    // Stagger the fade-up entrance already applied to every .card/.stat via CSS.
    document.querySelectorAll(".card, .stat").forEach(function (el, i) {
      el.style.animationDelay = (Math.min(i, 8) * 45) + "ms";
    });

    // Count up stat-tile values from 0 instead of showing them instantly.
    document.querySelectorAll(".stat__value").forEach(function (el) {
      var raw = el.textContent.trim();
      if (!/^-?[\d,]+$/.test(raw)) return;
      var target = parseInt(raw.replace(/,/g, ""), 10);
      if (isNaN(target)) return;
      var duration = 700;
      var start = null;
      function step(ts) {
        if (start === null) start = ts;
        var progress = Math.min((ts - start) / duration, 1);
        var eased = 1 - Math.pow(1 - progress, 3);
        el.textContent = Math.round(eased * target).toLocaleString();
        if (progress < 1) requestAnimationFrame(step);
        else el.textContent = target.toLocaleString();
      }
      requestAnimationFrame(step);
    });

    // Grow bar-chart fills from 0 to their target width.
    document.querySelectorAll(".bar-row__fill").forEach(function (el, i) {
      var target = el.style.width;
      el.style.width = "0%";
      el.style.transition = "width 0.6s cubic-bezier(0.16, 0.8, 0.3, 1)";
      setTimeout(function () { el.style.width = target; }, 120 + Math.min(i, 10) * 45);
    });

    // Draw donut-chart rings in from empty instead of appearing fully drawn.
    document.querySelectorAll(".donut-svg circle[stroke-dasharray]").forEach(function (circle) {
      var dasharray = circle.getAttribute("stroke-dasharray");
      var r = circle.r && circle.r.baseVal ? circle.r.baseVal.value : 0;
      var full = 2 * Math.PI * r;
      circle.setAttribute("stroke-dasharray", "0 " + full);
      circle.style.transition = "stroke-dasharray 0.8s cubic-bezier(0.16, 0.8, 0.3, 1)";
      requestAnimationFrame(function () {
        setTimeout(function () { circle.setAttribute("stroke-dasharray", dasharray); }, 80);
      });
    });
  }
})();
