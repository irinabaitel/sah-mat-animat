/**
 * server.js — Server turneu Swiss de șah
 * Pornire: npm install && node server.js
 * Jucători: http://[IP]:3000
 * Admin:    http://[IP]:3000/admin.html  (parola: prof)
 */

const express  = require('express');
const http     = require('http');
const { Server } = require('socket.io');
const path     = require('path');
const os       = require('os');

const app    = express();
const server = http.createServer(app);
const io     = new Server(server);

const PORT       = 3000;
const ADMIN_PASS = 'prof';

// Servim fișierele statice din același folder
app.use(express.static(path.join(__dirname)));

// Redirecționare rădăcină → pagina jucătorului
app.get('/', (req, res) => res.redirect('/jucator.html'));

// ═══════════════════════════════════════════════════════════════
//  STAREA TURNEULUI
// ═══════════════════════════════════════════════════════════════
const T = {
  players: new Map(),  // socketId → Player
  games:   new Map(),  // gameId   → Game
  rounds:  [],         // [Round]
  status:  'lobby',    // 'lobby' | 'active' | 'finished'
  clock:   { time: 0, increment: 0 },  // 0 = fără ceas
};

let _seq = 0;
const newId = () => `g${++_seq}`;

/** @returns {Player} */
function mkPlayer(id, name) {
  return { id, name, score: 0, colors: [], opponents: new Set(), byes: 0 };
}

// ═══════════════════════════════════════════════════════════════
//  IMPERECHERE SWISS
// ═══════════════════════════════════════════════════════════════
function havePlayedBefore(a, b) {
  return a.opponents.has(b.id);
}

/** Returnează culoarea preferată (jucătorul care a jucat mai mult cu alb vrea negru) */
function preferredColor(p) {
  const w = p.colors.filter(c => c === 'w').length;
  const b = p.colors.filter(c => c === 'b').length;
  return w <= b ? 'w' : 'b';
}

function assignColors(a, b) {
  const ap = preferredColor(a), bp = preferredColor(b);
  if (ap === 'w' && bp !== 'w') return [a.id, b.id];
  if (bp === 'w' && ap !== 'w') return [b.id, a.id];
  // Ambii vor același — dăm alb celui cu mai puțin alb
  const aw = a.colors.filter(c => c === 'w').length;
  const bw = b.colors.filter(c => c === 'w').length;
  if (aw < bw) return [a.id, b.id];
  if (bw < aw) return [b.id, a.id];
  return Math.random() < 0.5 ? [a.id, b.id] : [b.id, a.id];
}

function swissPair() {
  const players = [...T.players.values()];
  // Sortăm descrescător după punctaj, tiebreak aleatoriu
  players.sort((a, b) => b.score - a.score || Math.random() - 0.5);

  const paired = new Set();
  const pairings = [];

  for (let i = 0; i < players.length; i++) {
    if (paired.has(players[i].id)) continue;

    let partner = null;
    // Cautăm adversar cu care nu s-au mai întâlnit
    for (let j = i + 1; j < players.length; j++) {
      if (paired.has(players[j].id)) continue;
      if (!havePlayedBefore(players[i], players[j])) {
        partner = players[j]; break;
      }
    }
    // Fallback: oricum, chiar dacă s-au mai întâlnit
    if (!partner) {
      for (let j = i + 1; j < players.length; j++) {
        if (!paired.has(players[j].id)) { partner = players[j]; break; }
      }
    }

    if (partner) {
      const [whiteId, blackId] = assignColors(players[i], partner);
      const gameId = newId();
      pairings.push({ whiteId, blackId, gameId, result: null });
      paired.add(players[i].id);
      paired.add(partner.id);
    }
  }

  // BYE — jucătorul neîmperecheat (număr impar)
  for (const p of players) {
    if (!paired.has(p.id)) {
      pairings.push({ whiteId: p.id, blackId: 'BYE', gameId: null, result: 'bye' });
      paired.add(p.id);
    }
  }

  return pairings;
}

// ═══════════════════════════════════════════════════════════════
//  HELPERS BROADCAST
// ═══════════════════════════════════════════════════════════════

/** Scorul jucătorului aId în meciurile directe împotriva bId */
function getDirectScore(aId, bId) {
  let score = 0;
  for (const game of T.games.values()) {
    if (!game.result) continue;
    if (game.whiteId === aId && game.blackId === bId) {
      if (game.result === '1-0')         score += 1;
      else if (game.result === '1/2-1/2') score += 0.5;
    } else if (game.whiteId === bId && game.blackId === aId) {
      if (game.result === '0-1')         score += 1;
      else if (game.result === '1/2-1/2') score += 0.5;
    }
  }
  return score;
}

function getStandings() {
  const players = [...T.players.values()];

  // Buchholz = suma scorurilor actuale ale adversarilor
  const bh = new Map();
  for (const p of players) {
    let sum = 0;
    for (const oppId of p.opponents) {
      const opp = T.players.get(oppId);
      if (opp) sum += opp.score;
    }
    bh.set(p.id, Math.round(sum * 10) / 10);
  }

  players.sort((a, b) => {
    // 1. Scor total
    if (b.score !== a.score) return b.score - a.score;
    // 2. Întâlnire directă (dacă s-au întâlnit, cel care a câștigat e mai sus)
    const sa = getDirectScore(a.id, b.id);
    const sb = getDirectScore(b.id, a.id);
    if (sa + sb > 0 && sa !== sb) return sb - sa;
    // 3. Buchholz
    const bhDiff = (bh.get(b.id) || 0) - (bh.get(a.id) || 0);
    if (bhDiff !== 0) return bhDiff;
    // 4. Nume (alfabetic)
    return a.name.localeCompare(b.name);
  });

  return players.map((p, i) => ({
    rank:     i + 1,
    name:     p.name,
    score:    p.score,
    games:    p.colors.length + p.byes,
    buchholz: bh.get(p.id) || 0,
  }));
}

function broadcastLobby() {
  io.emit('lobby_update', {
    players:  [...T.players.values()].map(p => ({ id: p.id, name: p.name, score: p.score })),
    standings: getStandings(),
    roundNum: T.rounds.length,
    status:   T.status,
  });
}

function broadcastAdmin() {
  const roundsInfo = T.rounds.map(r => ({
    num: r.num,
    status: r.status,
    pairings: r.pairings.map(p => ({
      whiteId: p.whiteId,
      whiteName: T.players.get(p.whiteId)?.name || '?',
      blackId: p.blackId,
      blackName: p.blackId === 'BYE' ? 'BYE' : (T.players.get(p.blackId)?.name || '?'),
      gameId: p.gameId,
      result: p.result,
    })),
  }));

  io.to('admin').emit('admin_state', {
    players:   [...T.players.values()].map(p => ({ id: p.id, name: p.name, score: p.score })),
    rounds:    roundsInfo,
    standings: getStandings(),
    status:    T.status,
    clock:     T.clock,
  });
}

// ═══════════════════════════════════════════════════════════════
//  FINALIZARE JOC
// ═══════════════════════════════════════════════════════════════
function finishGame(gameId, result, reason) {
  const game = T.games.get(gameId);
  if (!game || game.result) return;
  game.result = result;

  // Actualizăm pairing-ul din runda curentă
  const round = T.rounds[T.rounds.length - 1];
  if (round) {
    const pairing = round.pairings.find(p => p.gameId === gameId);
    if (pairing) pairing.result = result;
  }

  // Actualizăm punctajele
  const white = T.players.get(game.whiteId);
  const black = T.players.get(game.blackId);
  if (result === '1-0')       { if (white) white.score += 1; }
  else if (result === '0-1')  { if (black) black.score += 1; }
  else if (result === '1/2-1/2') {
    if (white) white.score += 0.5;
    if (black) black.score += 0.5;
  }

  // Notificăm jucătorii
  const wSock = io.sockets.sockets.get(game.whiteId);
  const bSock = io.sockets.sockets.get(game.blackId);
  let wRes, bRes;
  if (result === '1-0')       { wRes = 'win';  bRes = 'loss'; }
  else if (result === '0-1')  { wRes = 'loss'; bRes = 'win';  }
  else                        { wRes = 'draw'; bRes = 'draw'; }

  if (wSock) wSock.emit('game_over', { gameId, result, reason, yourResult: wRes, opponentName: black?.name || '?' });
  if (bSock) bSock.emit('game_over', { gameId, result, reason, yourResult: bRes, opponentName: white?.name || '?' });

  // Dacă toate jocurile s-au terminat, runda e gata
  if (round) {
    const allDone = round.pairings.every(p => p.result !== null);
    if (allDone) {
      round.status = 'done';
      io.emit('round_complete', { roundNum: round.num, standings: getStandings() });
    }
  }

  broadcastLobby();
  broadcastAdmin();
}

// ═══════════════════════════════════════════════════════════════
//  SOCKET EVENTS
// ═══════════════════════════════════════════════════════════════
io.on('connection', (socket) => {
  // ── JUCĂTOR: înregistrare ──
  socket.on('register', ({ name }) => {
    if (T.status !== 'lobby') {
      socket.emit('error_msg', 'Turneul a început deja. Contactează profesorul.');
      return;
    }
    const cleanName = String(name || '').trim().slice(0, 25);
    if (!cleanName) return;

    const dup = [...T.players.values()].find(
      p => p.name.toLowerCase() === cleanName.toLowerCase()
    );
    if (dup) {
      socket.emit('error_msg', `Numele "${cleanName}" e deja luat. Alege altul.`);
      return;
    }

    T.players.set(socket.id, mkPlayer(socket.id, cleanName));
    socket.emit('welcome', { id: socket.id, name: cleanName });
    broadcastLobby();
    broadcastAdmin();
    console.log(`[+] Jucător: ${cleanName}`);
  });

  // ── ADMIN: autentificare ──
  socket.on('admin_login', ({ password }) => {
    if (password === ADMIN_PASS) {
      socket.join('admin');
      socket.emit('admin_ok');
      broadcastAdmin();
      console.log(`[ADMIN] conectat: ${socket.id}`);
    } else {
      socket.emit('admin_error', 'Parolă greșită.');
    }
  });

  // ── ADMIN: pornire rundă nouă ──
  socket.on('admin_start_round', () => {
    if (!socket.rooms.has('admin')) return;
    if (T.players.size < 2) {
      socket.emit('error_msg', 'Trebuie cel puțin 2 jucători înregistrați.');
      return;
    }

    // Verificăm că runda anterioară s-a terminat (sau e prima)
    const lastRound = T.rounds[T.rounds.length - 1];
    if (lastRound && lastRound.status === 'active') {
      socket.emit('error_msg', 'Runda curentă nu s-a terminat încă. Folosește "Forțează rezultat" pentru jocurile rămase.');
      return;
    }

    T.status = 'active';
    const pairings = swissPair();
    const round = { num: T.rounds.length + 1, pairings, status: 'active' };
    T.rounds.push(round);

    for (const p of pairings) {
      if (p.blackId === 'BYE') {
        // BYE: punctul se acordă imediat în swissPair() → doar notificăm
        const byeSock = io.sockets.sockets.get(p.whiteId);
        if (byeSock) byeSock.emit('got_bye', {
          round: round.num,
          name: T.players.get(p.whiteId)?.name,
        });
        continue;
      }

      const white = T.players.get(p.whiteId);
      const black = T.players.get(p.blackId);
      if (white) { white.colors.push('w'); white.opponents.add(p.blackId); }
      if (black) { black.colors.push('b'); black.opponents.add(p.whiteId); }

      T.games.set(p.gameId, {
        id: p.gameId,
        whiteId: p.whiteId,
        blackId: p.blackId,
        result: null,
        round: round.num,
      });

      const wSock = io.sockets.sockets.get(p.whiteId);
      const bSock = io.sockets.sockets.get(p.blackId);
      if (wSock) wSock.emit('game_start', { gameId: p.gameId, yourColor: 'w', opponentName: black?.name || '?', round: round.num, clock: T.clock });
      if (bSock) bSock.emit('game_start', { gameId: p.gameId, yourColor: 'b', opponentName: white?.name || '?', round: round.num, clock: T.clock });
    }

    broadcastLobby();
    broadcastAdmin();
    console.log(`[RUNDA ${round.num}] ${pairings.length} perechi`);
  });

  // ── JUCĂTOR: mutare ──
  socket.on('make_move', ({ gameId, from, to, promotion, fen }) => {
    const game = T.games.get(gameId);
    if (!game || game.result) return;
    const isWhite = game.whiteId === socket.id;
    const isBlack = game.blackId === socket.id;
    if (!isWhite && !isBlack) return;

    const opponentId = isWhite ? game.blackId : game.whiteId;
    const opponentSock = io.sockets.sockets.get(opponentId);
    if (opponentSock) opponentSock.emit('opponent_move', { gameId, from, to, promotion, fen });
    socket.emit('move_ack', { gameId, from, to, promotion, fen });
  });

  // ── JUCĂTOR: raportare rezultat (detectat de chess.js client) ──
  socket.on('game_result', ({ gameId, result, reason }) => {
    const game = T.games.get(gameId);
    if (!game || game.result) return;
    if (!['1-0', '0-1', '1/2-1/2'].includes(result)) return;
    finishGame(gameId, result, reason || 'normal');
  });

  // ── JUCĂTOR: abandonare ──
  socket.on('resign', ({ gameId }) => {
    const game = T.games.get(gameId);
    if (!game || game.result) return;
    const result = game.whiteId === socket.id ? '0-1' : '1-0';
    finishGame(gameId, result, 'abandon');
  });

  // ── JUCĂTOR: ofertă remiză ──
  socket.on('offer_draw', ({ gameId }) => {
    const game = T.games.get(gameId);
    if (!game || game.result) return;
    const opponentId = game.whiteId === socket.id ? game.blackId : game.whiteId;
    const opponentSock = io.sockets.sockets.get(opponentId);
    const myName = T.players.get(socket.id)?.name || '?';
    if (opponentSock) opponentSock.emit('draw_offered', { gameId, byName: myName });
  });

  // ── JUCĂTOR: acceptare remiză ──
  socket.on('accept_draw', ({ gameId }) => {
    const game = T.games.get(gameId);
    if (!game || game.result) return;
    finishGame(gameId, '1/2-1/2', 'acord_remiză');
  });

  // ── ADMIN: forțare rezultat ──
  socket.on('admin_force_result', ({ gameId, result }) => {
    if (!socket.rooms.has('admin')) return;
    if (!['1-0', '0-1', '1/2-1/2'].includes(result)) return;
    finishGame(gameId, result, 'admin');
  });

  // ── ADMIN: scoate jucător din lobby ──
  socket.on('admin_remove_player', ({ playerId }) => {
    if (!socket.rooms.has('admin')) return;
    const p = T.players.get(playerId);
    if (p) {
      console.log(`[ADMIN] Scoate jucător: ${p.name}`);
      T.players.delete(playerId);
      broadcastLobby();
      broadcastAdmin();
    }
  });

  // ── ADMIN: resetare turneu ──
  socket.on('admin_reset', () => {
    if (!socket.rooms.has('admin')) return;
    T.players.clear();
    T.games.clear();
    T.rounds.length = 0;
    T.status = 'lobby';
    _seq = 0;
    io.emit('tournament_reset');
    broadcastLobby();
    broadcastAdmin();
    console.log('[ADMIN] Turneu resetat.');
  });

  // ── ADMIN: setare ceas ──
  socket.on('admin_set_clock', ({ time, increment }) => {
    if (!socket.rooms.has('admin')) return;
    const t   = Math.max(0, parseInt(time)      || 0);
    const inc = Math.max(0, parseInt(increment) || 0);
    T.clock = { time: t, increment: inc };
    broadcastAdmin();
    console.log(`[ADMIN] Ceas setat: ${t}s + ${inc}s increment`);
  });

  // ── JUCĂTOR: timp expirat ──
  socket.on('out_of_time', ({ gameId }) => {
    const game = T.games.get(gameId);
    if (!game || game.result) return;
    const result = game.whiteId === socket.id ? '0-1' : '1-0';
    finishGame(gameId, result, 'timp');
  });

  // ── ADMIN: finalizare turneu ──
  socket.on('admin_finish_tournament', () => {
    if (!socket.rooms.has('admin')) return;
    T.status = 'finished';
    io.emit('tournament_finished', { standings: getStandings() });
    broadcastLobby();
    broadcastAdmin();
    console.log('[ADMIN] Turneu finalizat.');
  });

  // ── DECONECTARE ──
  socket.on('disconnect', () => {
    const player = T.players.get(socket.id);
    if (!player) return;
    console.log(`[-] Deconectat: ${player.name}`);

    // Dacă era într-un joc activ, adversarul câștigă
    for (const [gameId, game] of T.games) {
      if (game.result) continue;
      if (game.whiteId === socket.id || game.blackId === socket.id) {
        const result = game.whiteId === socket.id ? '0-1' : '1-0';
        finishGame(gameId, result, 'deconectare');
        break;
      }
    }

    // Ștergem din players numai dacă turneul nu a început
    if (T.status === 'lobby') {
      T.players.delete(socket.id);
    }

    broadcastLobby();
    broadcastAdmin();
  });
});

// ═══════════════════════════════════════════════════════════════
//  START SERVER
// ═══════════════════════════════════════════════════════════════
server.listen(PORT, '0.0.0.0', () => {
  // Afișăm IP-ul local al serverului
  const nets = os.networkInterfaces();
  let localIP = 'localhost';
  for (const name of Object.keys(nets)) {
    for (const net of nets[name]) {
      if (net.family === 'IPv4' && !net.internal) {
        localIP = net.address;
        break;
      }
    }
    if (localIP !== 'localhost') break;
  }

  console.log('\n╔══════════════════════════════════════════╗');
  console.log(`║  🏆  Server Turneu Swiss de Șah          ║`);
  console.log('╠══════════════════════════════════════════╣');
  console.log(`║  Jucători: http://${localIP}:${PORT}   `);
  console.log(`║  Admin:    http://${localIP}:${PORT}/admin.html`);
  console.log(`║  Parolă admin: ${ADMIN_PASS}               `);
  console.log('╚══════════════════════════════════════════╝\n');
});
