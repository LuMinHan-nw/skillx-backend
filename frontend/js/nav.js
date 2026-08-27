/* Sidebar shell, shared by every signed-in page.
   Student links point at separate pages. Admin links switch between the
   sections of admin.html - each one is a <section data-view="..."> there. */

const NAV_ICONS = {
  grid: '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
  layers: '<path d="M12 3 3 7.5l9 4.5 9-4.5L12 3Z"/><path d="M3 12.5 12 17l9-4.5"/><path d="M3 17 12 21.5 21 17"/>',
  calendar: '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M8 3v4M16 3v4M3 10h18"/>',
  award: '<circle cx="12" cy="9" r="6"/><path d="m9 14.5-1.5 7L12 19l4.5 2.5L15 14.5"/>',
  bell: '<path d="M18 9a6 6 0 1 0-12 0c0 5-2 6-2 6h16s-2-1-2-6Z"/><path d="M10.5 20a2 2 0 0 0 3 0"/>',
  user: '<circle cx="12" cy="8" r="4"/><path d="M4.5 20a7.5 7.5 0 0 1 15 0"/>',
  users: '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16.5 5.2a3.5 3.5 0 0 1 0 6.6"/><path d="M18 14.5a6.5 6.5 0 0 1 3.5 5.5"/>',
  flag: '<path d="M5 21V4"/><path d="M5 5h11l-2 3.5L16 12H5"/>',
  chart: '<path d="M4 20h16"/><rect x="5" y="12" width="3.5" height="6" rx="1"/><rect x="10.25" y="8" width="3.5" height="10" rx="1"/><rect x="15.5" y="4" width="3.5" height="14" rx="1"/>',
  tag: '<path d="M3.5 12.5 11 5h8v8l-7.5 7.5a1.5 1.5 0 0 1-2.1 0l-5.9-5.9a1.5 1.5 0 0 1 0-2.1Z"/><circle cx="15.5" cy="8.5" r="1.3"/>',
};

function icon(name) {
  return `<svg viewBox="0 0 24 24" fill="none" stroke-width="1.8"
            stroke-linecap="round" stroke-linejoin="round">${NAV_ICONS[name]}</svg>`;
}

const ADMIN_LINKS = [
  ["dashboard", "Dashboard", "grid"],
  ["skills", "Skill listings", "layers"],
  ["categories", "Categories", "tag"],
  ["users", "Students", "users"],
  ["certificates", "Certificates", "award"],
  ["complaints", "Complaints", "flag"],
  ["reports", "Reports", "chart"],
];

const STUDENT_LINKS = [
  ["dashboard.html", "Browse skills", "grid"],
  ["my_skills.html", "My skills", "layers"],
  ["bookings.html", "Bookings", "calendar"],
  ["certificates.html", "Certificates", "award"],
  ["profile.html", "Profile", "user"],
];

/* Show one admin section and mark its link active. */
function showView(name) {
  const sections = document.querySelectorAll("section[data-view]");
  if (!sections.length) return;
  let matched = false;
  for (const s of sections) {
    s.hidden = s.dataset.view !== name;
    if (!s.hidden) matched = true;
  }
  if (!matched) return showView("dashboard");

  for (const a of document.querySelectorAll(".sidebar a[data-view]")) {
    a.classList.toggle("active", a.dataset.view === name);
  }
  history.replaceState(null, "", "#" + name);
  window.scrollTo(0, 0);
}

async function renderNav(active) {
  const isAdmin = getRole() === "admin";
  const name = getName() ?? "";

  let unread = 0;
  try {
    const res = await api("/api/notifications");
    unread = res.data.filter((n) => !n.is_read).length;
  } catch (err) {}

  // The admin views live on admin.html, so the links carry a real destination.
  // On admin.html itself the click is intercepted below and the view is swapped
  // in place; from any other page (Alerts) the browser follows the link and
  // renderNav opens the right view from the hash.
  const links = isAdmin
    ? ADMIN_LINKS.map(([view, label, ic]) =>
        `<a href="/admin.html#${view}" data-view="${view}">${icon(ic)}${label}</a>`)
    : STUDENT_LINKS.map(([href, label, ic]) =>
        `<a href="/${href}" class="${active === href ? "active" : ""}">${icon(ic)}${label}</a>`);

  links.push(`<a href="/notifications.html"
        class="${active === "notifications.html" ? "active" : ""}">
        ${icon("bell")}Alerts
        ${unread ? `<span class="badge-dot" style="margin-left:auto">${unread}</span>` : ""}
      </a>`);

  const aside = document.createElement("aside");
  aside.className = "sidebar";
  aside.innerHTML = `
    <a class="brand" href="/${isAdmin ? "admin.html" : "dashboard.html"}">
      <span class="mark">SX</span>
      <span>
        <span class="name">SkillX</span>
        <span class="tagline">Skill Exchange</span>
      </span>
    </a>
    <nav>${links.join("")}</nav>
    <div class="who">
      <span class="initial">${name.charAt(0).toUpperCase()}</span>
      <div>
        <div class="n">${name}</div>
        <div class="r">${isAdmin ? "Administrator" : "Student"}</div>
      </div>
    </div>
    <button class="ghost logout" onclick="logout()">Log out</button>`;
  document.body.prepend(aside);

  // Only take over the links on a page that actually holds the view sections.
  // Without this check the Alerts page swallowed every click and left the
  // administrator with no way back.
  if (isAdmin && document.querySelector("section[data-view]")) {
    for (const a of aside.querySelectorAll("a[data-view]")) {
      a.addEventListener("click", (e) => {
        e.preventDefault();
        showView(a.dataset.view);
      });
    }
    showView(location.hash.slice(1) || "dashboard");
    // keeps a pasted or bookmarked #view link working once the page is open
    window.addEventListener("hashchange", () =>
      showView(location.hash.slice(1) || "dashboard"));
  }
}
