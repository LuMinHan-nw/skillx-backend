function getToken()  { return localStorage.getItem("skillx_token"); }
function getRole()   { return localStorage.getItem("skillx_role"); }
function getName()   { return localStorage.getItem("skillx_name"); }

function saveLogin(data) {
  localStorage.setItem("skillx_token", data.access_token);
  localStorage.setItem("skillx_role", data.user.role);
  localStorage.setItem("skillx_name", data.user.name);
}

function logout() {
  localStorage.removeItem("skillx_token");
  localStorage.removeItem("skillx_role");
  localStorage.removeItem("skillx_name");
  window.location.href = "/login.html";
}

function requireLogin() {
  if (!getToken()) window.location.href = "/login.html";
}

async function api(path, options = {}) {
  const headers = options.headers || {};
  if (getToken()) headers["Authorization"] = "Bearer " + getToken();

  let body = options.body;
  if (body && typeof body === "object" && !(body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
    body = JSON.stringify(body);
  }

  const res = await fetch(path, { ...options, headers, body });

  if (res.status === 401 && getToken()) { logout(); return; }

  const json = await res.json().catch(() => ({}));
  if (!res.ok || json.status === false) {
    throw new Error(json.message || "Something went wrong. Please try again.");
  }
  return json;
}
