/**
 * Cloudflare Pages Function : /api/contribute
 *
 * Reçoit les contributions du formulaire et :
 * 1. Envoie un email de remerciement au contributeur (template 1)
 * 2. Envoie une notification interne à l'admin (template 3)
 * 3. Ajoute le contributeur à la liste Brevo "Contributeurs"
 *
 * Variables d'environnement requises (Cloudflare Pages > Settings > Environment Variables) :
 *   BREVO_API_KEY = xkeysib-...
 *
 * Le formulaire envoie un POST JSON :
 * {
 *   type: "erreur" | "autre",
 *   email: "user@example.com",
 *   message: "...",
 *   ville: "Paris" (optionnel),
 *   candidat: "Grégoire" (optionnel),
 *   sujet: "Suggestion d'amélioration" (optionnel),
 *   source: "https://..." (optionnel),
 *   pageUrl: "https://pourquituvotes.fr/..." (optionnel)
 * }
 */

const BREVO_API = "https://api.brevo.com/v3";
const ADMIN_EMAIL = "contact@pourquituvotes.fr";
const TEMPLATE_MERCI = 1;
const TEMPLATE_NOTIF = 3;
const LISTE_CONTRIBUTEURS = 3;

// CORS headers
const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "https://pourquituvotes.fr",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS_HEADERS });
}

export async function onRequestPost(context) {
  const { env, request } = context;
  const apiKey = env.BREVO_API_KEY;

  if (!apiKey) {
    return jsonResponse({ error: "Configuration serveur manquante" }, 500);
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return jsonResponse({ error: "JSON invalide" }, 400);
  }

  // Validation
  const { type, email, message } = body;
  if (!type || !email || !message) {
    return jsonResponse({ error: "Champs requis : type, email, message" }, 400);
  }

  if (!isValidEmail(email)) {
    return jsonResponse({ error: "Email invalide" }, 400);
  }

  if (message.length > 5000) {
    return jsonResponse({ error: "Message trop long (max 5000 caractères)" }, 400);
  }

  const typeLabel =
    type === "erreur" ? "signalement d'erreur" : "suggestion";

  try {
    // 1. Ajouter le contact à la liste Contributeurs
    await brevoPost(apiKey, "/contacts", {
      email: email,
      listIds: [LISTE_CONTRIBUTEURS],
      attributes: {
        PRENOM: "",
        NOM: "",
      },
      updateEnabled: true,
    });

    // 2. Envoyer le mail de remerciement au contributeur
    await brevoPost(apiKey, "/smtp/email", {
      templateId: TEMPLATE_MERCI,
      to: [{ email: email }],
      params: {
        type_contribution: typeLabel,
        message: sanitize(message),
      },
    });

    // 3. Envoyer la notification interne
    await brevoPost(apiKey, "/smtp/email", {
      templateId: TEMPLATE_NOTIF,
      to: [{ email: ADMIN_EMAIL }],
      params: {
        type_contribution: typeLabel,
        email_contributeur: email,
        ville: sanitize(body.ville || "—"),
        candidat: sanitize(body.candidat || "—"),
        message: sanitize(message),
        page_url: sanitize(body.pageUrl || ""),
        source_correcte: body.source
          ? "Source suggérée : " + sanitize(body.source)
          : "",
      },
    });

    return jsonResponse({ ok: true });
  } catch (err) {
    console.error("Brevo error:", err);
    return jsonResponse({ error: "Erreur d'envoi" }, 502);
  }
}

// ─── Helpers ───

async function brevoPost(apiKey, path, data) {
  const resp = await fetch(`${BREVO_API}${path}`, {
    method: "POST",
    headers: {
      "api-key": apiKey,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!resp.ok && resp.status !== 204) {
    const text = await resp.text();
    // Contact already exists is OK
    if (resp.status === 400 && text.includes("already exist")) return;
    throw new Error(`Brevo ${path}: ${resp.status} ${text}`);
  }
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) && email.length <= 254;
}

function sanitize(str) {
  if (typeof str !== "string") return "";
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .slice(0, 5000);
}

function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "Content-Type": "application/json",
      ...CORS_HEADERS,
    },
  });
}
