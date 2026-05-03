// ════════════════════════════════════════════════════════════════
//  FORMAZIONE DIGITALE — auth.js
//  Gestisce: login magic link, logout, stato utente, segnalibri.
//  Richiede supabase.js caricato prima.
// ════════════════════════════════════════════════════════════════

import { supabase } from '/supabase.js';

// ── STATO ────────────────────────────────────────────────────────
let currentUser = null;
let bookmarks   = new Set();

// ── INIT — eseguito su ogni pagina ───────────────────────────────
export async function initAuth() {
  // Recupera sessione corrente
  const { data: { session } } = await supabase.auth.getSession();
  currentUser = session?.user ?? null;

  // Aggiorna UI
  renderAuthUI();

  // Ascolta cambi di stato (login, logout, refresh token)
  supabase.auth.onAuthStateChange((_event, session) => {
    currentUser = session?.user ?? null;
    renderAuthUI();
    if (currentUser) loadBookmarks();
  });

  // Carica segnalibri se loggato
  if (currentUser) await loadBookmarks();
}

// ── LOGIN con magic link ──────────────────────────────────────────
export async function loginWithEmail(email) {
  const { error } = await supabase.auth.signInWithOtp({
    email,
    options: {
      emailRedirectTo: window.location.origin + '/'
    }
  });
  return error;
}

// ── LOGOUT ───────────────────────────────────────────────────────
export async function logout() {
  await supabase.auth.signOut();
}

// ── SEGNALIBRI ───────────────────────────────────────────────────
async function loadBookmarks() {
  if (!currentUser) return;
  const { data } = await supabase
    .from('bookmarks')
    .select('resource_path');
  if (data) {
    bookmarks = new Set(data.map(b => b.resource_path));
    renderBookmarkButtons();
  }
}

export async function toggleBookmark(path) {
  if (!currentUser) {
    openAuthModal();
    return;
  }
  if (bookmarks.has(path)) {
    await supabase.from('bookmarks').delete()
      .eq('user_id', currentUser.id)
      .eq('resource_path', path);
    bookmarks.delete(path);
  } else {
    await supabase.from('bookmarks').insert({
      user_id: currentUser.id,
      resource_path: path
    });
    bookmarks.add(path);
  }
  renderBookmarkButtons();
}

export function isBookmarked(path) {
  return bookmarks.has(path);
}

export function getUser() {
  return currentUser;
}

// ── RENDER UI ────────────────────────────────────────────────────
function renderAuthUI() {
  const btn = document.getElementById('auth-btn');
  if (!btn) return;

  if (currentUser) {
    const email = currentUser.email;
    const initial = email.charAt(0).toUpperCase();
    btn.innerHTML = `<span class="auth-avatar">${initial}</span>`;
    btn.title = email;
    btn.onclick = openProfileModal;
  } else {
    btn.innerHTML = '🔐 Accedi';
    btn.onclick = openAuthModal;
  }
}

function renderBookmarkButtons() {
  document.querySelectorAll('[data-bookmark]').forEach(btn => {
    const path = btn.dataset.bookmark;
    btn.classList.toggle('bookmarked', bookmarks.has(path));
    btn.title = bookmarks.has(path) ? 'Rimuovi dai salvati' : 'Salva risorsa';
  });
}

// ── MODAL AUTH ───────────────────────────────────────────────────
export function openAuthModal() {
  const modal = document.getElementById('auth-modal');
  if (modal) {
    modal.classList.add('is-open');
    document.body.classList.add('modal-open');
    setTimeout(() => document.getElementById('auth-email')?.focus(), 80);
  }
}

export function closeAuthModal() {
  const modal = document.getElementById('auth-modal');
  if (modal) {
    modal.classList.remove('is-open');
    document.body.classList.remove('modal-open');
  }
}

// ── MODAL PROFILO ─────────────────────────────────────────────────
function openProfileModal() {
  const modal = document.getElementById('profile-modal');
  if (modal) {
    document.getElementById('profile-email').textContent = currentUser.email;
    document.getElementById('profile-bookmarks-count').textContent = bookmarks.size;
    modal.classList.add('is-open');
    document.body.classList.add('modal-open');
  }
}

export function closeProfileModal() {
  const modal = document.getElementById('profile-modal');
  if (modal) {
    modal.classList.remove('is-open');
    document.body.classList.remove('modal-open');
  }
}

// ── FORM SUBMIT ──────────────────────────────────────────────────
export function initAuthForm() {
  const form = document.getElementById('auth-form');
  if (!form) return;

  form.addEventListener('submit', async e => {
    e.preventDefault();
    const email = document.getElementById('auth-email').value.trim();
    const btn   = form.querySelector('button[type=submit]');
    const msg   = document.getElementById('auth-message');

    btn.disabled = true;
    btn.textContent = 'Invio in corso…';

    const error = await loginWithEmail(email);

    if (error) {
      msg.textContent = 'Errore: ' + error.message;
      msg.className = 'auth-msg error';
      btn.disabled = false;
      btn.textContent = 'Invia link →';
    } else {
      msg.textContent = 'Controlla la tua email — ti abbiamo inviato il link di accesso.';
      msg.className = 'auth-msg success';
      btn.textContent = 'Inviato ✓';
    }
  });
}
