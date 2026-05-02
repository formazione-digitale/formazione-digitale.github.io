// ════════════════════════════════════════════════════════════════
//  FORMAZIONE DIGITALE — supabase.js
//  Client Supabase condiviso tra tutte le pagine.
//  Importato via <script> prima di auth.js e degli script pagina.
// ════════════════════════════════════════════════════════════════

import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm';

const SUPABASE_URL  = 'https://xfefrhaleoqvpzsrrepq.supabase.co';
const SUPABASE_ANON = 'sb_publishable_EeKIBeTGG7Xd914Dhj1iCQ_XaqcjaZE';

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON);
