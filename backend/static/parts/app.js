// ===== State =====
const API = '/api/v1';
let token = localStorage.getItem('gs_token') || '';
let currentUser = null;
let currentDate = new Date().toISOString().slice(0, 10);
let selectedMealType = 'breakfast';
let selectedGoal = 'lose_weight';
let selectedIntensity = 'medium';
let sleepQuality = 3;
let recogType = 'food';
let recogMealType = 'lunch';
let recogData = null;
let currentSessionId = null;
let chatStreaming = false;
let planGoalType = 'lose_weight';
let statDays = 7;

// ===== Utility =====
function hdrs() {
  return { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token };
}

async function api(method, path, body) {
  const opts = { method, headers: hdrs() };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(API + path, opts);
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Request failed');
  return data;
}

function toast(msg) {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.classList.add('show');
  setTimeout(() => el.classList.remove('show'), 2200);
}

function fmtDate(dateStr) {
  const d = new Date(dateStr + 'T00:00:00');
  const m = d.getMonth() + 1;
  const day = d.getDate();
  const wk = ['日', '一', '二', '三', '四', '五', '六'][d.getDay()];
  return { text: m + '月' + day + '日', sub: '星期' + wk };
}

function isToday(dateStr) {
  return dateStr === new Date().toISOString().slice(0, 10);
}

function closeModal(id) {
  document.getElementById(id).classList.remove('active');
}

// ===== Auth =====
function switchAuthTab(tab) {
  document.querySelectorAll('.auth-tab').forEach((t, i) => {
    t.classList.toggle('active', tab === 'login' ? i === 0 : i === 1);
  });
  document.getElementById('loginForm').style.display = tab === 'login' ? 'block' : 'none';
  document.getElementById('registerForm').style.display = tab === 'register' ? 'block' : 'none';
  document.getElementById('authError').textContent = '';
}

async function doLogin() {
  try {
    const data = await api('POST', '/auth/login', {
      phone: document.getElementById('loginPhone').value,
      password: document.getElementById('loginPassword').value,
    });
    token = data.data.access_token;
    localStorage.setItem('gs_token', token);
    enterApp();
  } catch (e) { document.getElementById('authError').textContent = e.message; }
}

async function doRegister() {
  try {
    const data = await api('POST', '/auth/register', {
      phone: document.getElementById('regPhone').value,
      nickname: document.getElementById('regNickname').value,
      password: document.getElementById('regPassword').value,
    });
    token = data.data.access_token;
    localStorage.setItem('gs_token', token);
    enterApp();
  } catch (e) { document.getElementById('authError').textContent = e.message; }
}

function doLogout() {
  token = '';
  currentUser = null;
  localStorage.removeItem('gs_token');
  document.getElementById('authPage').classList.add('active');
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.getElementById('tabBar').classList.add('hidden');
}

// ===== Navigation =====
function switchPage(name) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.getElementById(name + 'Page').classList.add('active');
  const tabs = ['home', 'chat', 'stats', 'profile'];
  document.querySelectorAll('.tab-item').forEach((t, i) => {
    t.classList.toggle('active', tabs[i] === name);
  });
  if (name === 'chat') loadChatSessions();
  if (name === 'stats') loadStats();
  if (name === 'profile') loadProfile();
}

// ===== Date Navigation =====
function updateDateDisplay() {
  const f = fmtDate(currentDate);
  document.getElementById('dateText').textContent = isToday(currentDate) ? '今天 ' + f.text : f.text;
  document.getElementById('dateSub').textContent = f.sub;
}

function changeDate(delta) {
  const d = new Date(currentDate + 'T00:00:00');
  d.setDate(d.getDate() + delta);
  currentDate = d.toISOString().slice(0, 10);
  updateDateDisplay();
  loadDashboard();
}

// ===== Enter App =====
async function enterApp() {
  document.getElementById('authPage').classList.remove('active');
  document.getElementById('homePage').classList.add('active');
  document.getElementById('tabBar').classList.remove('hidden');

  try {
    const me = await api('GET', '/users/me');
    currentUser = me.data;
  } catch { currentUser = {}; }

  updateDateDisplay();
  loadDashboard();
}

// ===== Dashboard =====
async function loadDashboard() {
  try {
    const stats = await api('GET', '/stats/daily?date=' + currentDate);
    const s = stats.data;
    const target = s.calorie_target || 2000;
    const consumed = Math.round(s.calories_consumed || 0);
    const remain = Math.max(0, target - consumed);
    const pct = Math.min(consumed / target, 1);

    document.getElementById('calNum').textContent = consumed;
    document.getElementById('calTarget').textContent = target + ' kcal';
    document.getElementById('calEaten').textContent = consumed + ' kcal';
    document.getElementById('calRemain').textContent = remain + ' kcal';

    // Ring animation
    const circ = 2 * Math.PI * 34;
    const arc = document.getElementById('calArc');
    arc.style.strokeDasharray = circ;
    arc.style.strokeDashoffset = circ * (1 - pct);
    arc.style.stroke = pct > 0.9 ? 'var(--danger)' : pct > 0.7 ? 'var(--warning)' : 'var(--primary)';

    // Macros
    const pt = (currentUser && currentUser.daily_calorie_target) ? Math.round(target * 0.3 / 4) : 120;
    const ft = (currentUser && currentUser.daily_calorie_target) ? Math.round(target * 0.25 / 9) : 60;
    const ct = (currentUser && currentUser.daily_calorie_target) ? Math.round(target * 0.45 / 4) : 250;
    document.getElementById('pVal').textContent = Math.round(s.protein_g || 0) + 'g';
    document.getElementById('fVal').textContent = Math.round(s.fat_g || 0) + 'g';
    document.getElementById('cVal').textContent = Math.round(s.carbs_g || 0) + 'g';
    document.getElementById('pBar').style.width = Math.min(100, (s.protein_g || 0) / pt * 100) + '%';
    document.getElementById('fBar').style.width = Math.min(100, (s.fat_g || 0) / ft * 100) + '%';
    document.getElementById('cBar').style.width = Math.min(100, (s.carbs_g || 0) / ct * 100) + '%';

    // Mini stats
    document.getElementById('exMin').innerHTML = (s.exercise_minutes || 0) + '<span class="unit"> 分钟</span>';
    document.getElementById('exCal').textContent = '消耗 ' + Math.round(s.calories_burned || 0) + ' kcal';

    if (s.sleep_duration_minutes) {
      const h = Math.floor(s.sleep_duration_minutes / 60);
      const m = s.sleep_duration_minutes % 60;
      document.getElementById('slpH').innerHTML = h + (m > 0 ? '.' + Math.round(m / 6) : '') + '<span class="unit"> 小时</span>';
      const q = s.sleep_quality || 3;
      document.getElementById('slpQ').textContent = '质量 ' + '\u2B50'.repeat(q);
    } else {
      document.getElementById('slpH').innerHTML = '--<span class="unit"> 小时</span>';
      document.getElementById('slpQ').textContent = '暂无记录';
    }

    if (s.weight_kg) {
      document.getElementById('wtVal').innerHTML = s.weight_kg + '<span class="unit"> kg</span>';
    }

  } catch (e) { console.error('Dashboard err:', e); }

  loadMeals();
  loadExercises();
}

// ===== Meals =====
async function loadMeals() {
  try {
    const res = await api('GET', '/diet/daily-summary?record_date=' + currentDate);
    const d = res.data;
    const el = document.getElementById('mealList');
    const icons = { breakfast: '\u{1F305}', lunch: '\u2600\uFE0F', dinner: '\u{1F319}', snack: '\u{1F36A}' };
    const names = { breakfast: '早餐', lunch: '午餐', dinner: '晚餐', snack: '加餐' };

    if (d.meal_count === 0) {
      el.innerHTML = '<div class="empty"><div class="ico">\u{1F37D}</div><div class="txt">还没有饮食记录<br>点击拍照识别或 + 添加</div></div>';
      return;
    }

    let html = '';
    for (const [type, foods] of Object.entries(d.meals)) {
      for (const f of foods) {
        html += '<div class="record-card">' +
          '<div class="record-left">' +
          '<div class="record-ico">' + (icons[type] || '\u{1F37D}') + '</div>' +
          '<div class="record-info">' +
          '<div class="record-name">' + f.food_name + '</div>' +
          '<div class="record-meta">' + (names[type] || type) + (f.serving_size ? ' \u00B7 ' + f.serving_size : '') + '</div>' +
          '</div></div>' +
          '<div class="record-val">' + Math.round(f.calories) + ' <span class="u">kcal</span></div>' +
          '</div>';
      }
    }
    el.innerHTML = html;
  } catch (e) { console.error('Meals err:', e); }
}

// ===== Exercises =====
async function loadExercises() {
  try {
    const res = await api('GET', '/exercise/records?record_date=' + currentDate);
    const list = res.data || [];
    const el = document.getElementById('exList');
    if (list.length === 0) {
      el.innerHTML = '<div class="empty"><div class="ico">\u{1F3CB}</div><div class="txt">还没有运动记录</div></div>';
      return;
    }
    el.innerHTML = list.map(function(e) {
      return '<div class="record-card">' +
        '<div class="record-left">' +
        '<div class="record-ico">' + (e.exercise_type === 'cardio' ? '\u{1F3C3}' : '\u{1F3CB}') + '</div>' +
        '<div class="record-info">' +
        '<div class="record-name">' + e.exercise_name + '</div>' +
        '<div class="record-meta">' + (e.duration_minutes || 0) + '分钟' + (e.sets ? ' \u00B7 ' + e.sets + '组' : '') + '</div>' +
        '</div></div>' +
        '<div class="record-val">' + Math.round(e.calories_burned || 0) + ' <span class="u">kcal</span></div>' +
        '</div>';
    }).join('');
  } catch (e) { console.error('Exercise err:', e); }
}

// ===== Add Meal =====
function openAddMeal() {
  document.getElementById('mealModal').classList.add('active');
  document.getElementById('mealFoodName').value = '';
  document.getElementById('mealCal').value = '';
  document.getElementById('mealP').value = '';
  document.getElementById('mealF').value = '';
  document.getElementById('mealC').value = '';
  selectedMealType = 'breakfast';
  document.querySelectorAll('#mealTypePills .pill').forEach(function(p) {
    p.classList.toggle('active', p.dataset.type === 'breakfast');
  });
}

function pickMealType(el) {
  document.querySelectorAll('#mealTypePills .pill').forEach(function(p) { p.classList.remove('active'); });
  el.classList.add('active');
  selectedMealType = el.dataset.type;
}

async function saveMeal() {
  var name = document.getElementById('mealFoodName').value.trim();
  if (!name) { toast('请输入食物名称'); return; }
  try {
    await api('POST', '/diet/records', {
      record_date: currentDate,
      meal_type: selectedMealType,
      food_name: name,
      calories: parseFloat(document.getElementById('mealCal').value) || 0,
      protein_g: parseFloat(document.getElementById('mealP').value) || 0,
      fat_g: parseFloat(document.getElementById('mealF').value) || 0,
      carbs_g: parseFloat(document.getElementById('mealC').value) || 0,
    });
    closeModal('mealModal');
    toast('记录已保存');
    loadDashboard();
  } catch (e) { toast('保存失败: ' + e.message); }
}

// ===== Add Exercise =====
function openAddExercise() {
  document.getElementById('exerciseModal').classList.add('active');
  document.getElementById('exName').value = '';
  document.getElementById('exDur').value = '';
  document.getElementById('exBurn').value = '';
  document.getElementById('exSets').value = '';
}

function pickIntensity(el) {
  document.querySelectorAll('#exerciseModal .pill').forEach(function(p) { p.classList.remove('active'); });
  el.classList.add('active');
  selectedIntensity = el.dataset.int;
}

async function saveExercise() {
  var name = document.getElementById('exName').value.trim();
  if (!name) { toast('请输入运动名称'); return; }
  try {
    await api('POST', '/exercise/records', {
      record_date: currentDate,
      exercise_type: 'cardio',
      exercise_name: name,
      duration_minutes: parseInt(document.getElementById('exDur').value) || 30,
      calories_burned: parseFloat(document.getElementById('exBurn').value) || 0,
      intensity: selectedIntensity,
      sets: parseInt(document.getElementById('exSets').value) || 0,
    });
    closeModal('exerciseModal');
    toast('运动记录已保存');
    loadDashboard();
  } catch (e) { toast('保存失败: ' + e.message); }
}

// ===== Sleep =====
function openAddSleep() {
  document.getElementById('sleepModal').classList.add('active');
}

function setSlpQ(val) {
  sleepQuality = val;
  var stars = document.querySelectorAll('#sleepStars span');
  stars.forEach(function(s, i) { s.textContent = i < val ? '\u2B50' : '\u2606'; });
}

async function saveSleep() {
  var start = document.getElementById('slpStart').value;
  var end = document.getElementById('slpEnd').value;
  if (!start || !end) { toast('请选择时间'); return; }
  var sh = parseInt(start.split(':')[0]), sm = parseInt(start.split(':')[1]);
  var eh = parseInt(end.split(':')[0]), em = parseInt(end.split(':')[1]);
  var mins = (eh * 60 + em) - (sh * 60 + sm);
  if (mins < 0) mins += 1440;
  try {
    await api('POST', '/sleep/records', {
      record_date: currentDate,
      sleep_start: currentDate + 'T' + start + ':00',
      sleep_end: currentDate + 'T' + end + ':00',
      duration_minutes: mins,
      quality: sleepQuality,
    });
    closeModal('sleepModal');
    toast('睡眠记录已保存');
    loadDashboard();
  } catch (e) { toast('保存失败: ' + e.message); }
}

// ===== Weight =====
async function recordWeight() {
  var w = parseFloat(document.getElementById('weightInput').value);
  if (!w || w < 20 || w > 300) { toast('请输入合理体重'); return; }
  try {
    await api('POST', '/body/metrics', { record_date: currentDate, weight_kg: w });
    document.getElementById('weightStatus').textContent = '已记录: ' + w + ' kg';
    document.getElementById('weightInput').value = '';
    toast('体重已记录');
    loadDashboard();
  } catch (e) { toast('保存失败: ' + e.message); }
}

// ===== Photo Recognition =====
function openRecognition() {
  document.getElementById('recogModal').classList.add('active');
  document.getElementById('recogPreview').style.display = 'none';
  document.getElementById('recogLoading').style.display = 'none';
  recogType = 'food';
  document.querySelectorAll('#recogModal .pill').forEach(function(p) {
    p.classList.toggle('active', p.dataset.rtype === 'food');
  });
}

function pickRecogType(el) {
  document.querySelectorAll('#recogModal .pill').forEach(function(p) { p.classList.remove('active'); });
  el.classList.add('active');
  recogType = el.dataset.rtype;
}

function triggerCamera() { document.getElementById('cameraInput').click(); }
function triggerGallery() { document.getElementById('galleryInput').click(); }

async function handleImagePick(event) {
  var file = event.target.files[0];
  if (!file) return;
  event.target.value = '';

  // Show preview
  var url = URL.createObjectURL(file);
  document.getElementById('recogImg').src = url;
  document.getElementById('recogPreview').style.display = 'block';
  document.getElementById('recogLoading').style.display = 'flex';

  // Upload for recognition
  var formData = new FormData();
  formData.append('file', file);

  var endpoint = recogType === 'food' ? '/ai/recognize/food/upload' : '/ai/recognize/exercise/upload';

  try {
    var res = await fetch(API + endpoint, {
      method: 'POST',
      headers: { 'Authorization': 'Bearer ' + token },
      body: formData,
    });
    var data = await res.json();
    if (!res.ok) throw new Error(data.detail || '识别失败');

    document.getElementById('recogLoading').style.display = 'none';
    closeModal('recogModal');

    // Show result
    recogData = data.data;
    showRecogResult();
  } catch (e) {
    document.getElementById('recogLoading').style.display = 'none';
    toast('识别失败: ' + e.message);
  }
}

function showRecogResult() {
  document.getElementById('recogResultModal').classList.add('active');
  var el = document.getElementById('recogResultContent');
  var mealTypeEl = document.getElementById('recogMealType');

  if (recogType === 'food' && recogData.foods) {
    document.getElementById('recogResultTitle').textContent = '食物识别结果';
    mealTypeEl.style.display = 'block';
    var html = '<div class="recog-foods">';
    recogData.foods.forEach(function(f, i) {
      html += '<div class="recog-food">' +
        '<div class="recog-food-head">' +
        '<span class="recog-food-name">' + f.name + '</span>' +
        '<span class="recog-food-conf">' + (f.estimated_serving || '') + '</span>' +
        '</div>' +
        '<div class="recog-food-grid">' +
        '<div class="fg"><label>热量</label><input type="number" id="rf_cal_' + i + '" value="' + Math.round(f.calories) + '"></div>' +
        '<div class="fg"><label>蛋白质</label><input type="number" id="rf_p_' + i + '" value="' + Math.round(f.protein_g) + '" step="0.1"></div>' +
        '<div class="fg"><label>脂肪</label><input type="number" id="rf_f_' + i + '" value="' + Math.round(f.fat_g) + '" step="0.1"></div>' +
        '<div class="fg"><label>碳水</label><input type="number" id="rf_c_' + i + '" value="' + Math.round(f.carbs_g) + '" step="0.1"></div>' +
        '</div></div>';
    });
    html += '</div>';
    html += '<div style="background:var(--accent-bg);border-radius:var(--radius-xs);padding:10px;text-align:center;font-size:14px;">' +
      '总热量: <strong>' + Math.round(recogData.total_calories) + '</strong> kcal' +
      '<div style="font-size:12px;color:var(--text-secondary);margin-top:4px;">数值可编辑，觉得不准确请直接修改</div>' +
      '</div>';
    el.innerHTML = html;

    // Auto-select meal type based on time
    var hour = new Date().getHours();
    if (hour < 10) recogMealType = 'breakfast';
    else if (hour < 14) recogMealType = 'lunch';
    else if (hour < 20) recogMealType = 'dinner';
    else recogMealType = 'snack';
    document.querySelectorAll('#recogMealPills .pill').forEach(function(p) {
      p.classList.toggle('active', p.dataset.type === recogMealType);
    });

  } else if (recogType === 'exercise' && recogData.exercise) {
    document.getElementById('recogResultTitle').textContent = '运动识别结果';
    mealTypeEl.style.display = 'none';
    var ex = recogData.exercise;
    var html = '<div class="recog-food">' +
      '<div class="recog-food-head"><span class="recog-food-name">' + ex.exercise_name + '</span></div>' +
      '<div class="recog-food-grid" style="grid-template-columns:1fr 1fr 1fr;">' +
      '<div class="fg"><label>时长(分)</label><input type="number" id="re_dur" value="' + (ex.estimated_duration_min || 30) + '"></div>' +
      '<div class="fg"><label>消耗</label><input type="number" id="re_cal" value="' + Math.round(ex.calories_burned) + '"></div>' +
      '<div class="fg"><label>强度</label><input type="text" id="re_int" value="' + (ex.intensity || 'medium') + '"></div>' +
      '</div></div>';
    el.innerHTML = html;
  }
}

function pickRecogMealType(el) {
  document.querySelectorAll('#recogMealPills .pill').forEach(function(p) { p.classList.remove('active'); });
  el.classList.add('active');
  recogMealType = el.dataset.type;
}

async function saveRecogResult() {
  try {
    if (recogType === 'food' && recogData.foods) {
      for (var i = 0; i < recogData.foods.length; i++) {
        var f = recogData.foods[i];
        await api('POST', '/diet/records', {
          record_date: currentDate,
          meal_type: recogMealType,
          food_name: f.name,
          calories: parseFloat(document.getElementById('rf_cal_' + i).value) || 0,
          protein_g: parseFloat(document.getElementById('rf_p_' + i).value) || 0,
          fat_g: parseFloat(document.getElementById('rf_f_' + i).value) || 0,
          carbs_g: parseFloat(document.getElementById('rf_c_' + i).value) || 0,
          serving_size: f.estimated_serving || '',
          source: 'ai_image',
        });
      }
      toast('已保存 ' + recogData.foods.length + ' 项食物');
    } else if (recogType === 'exercise' && recogData.exercise) {
      var ex = recogData.exercise;
      await api('POST', '/exercise/records', {
        record_date: currentDate,
        exercise_type: ex.exercise_type || 'cardio',
        exercise_name: ex.exercise_name,
        duration_minutes: parseInt(document.getElementById('re_dur').value) || 30,
        calories_burned: parseFloat(document.getElementById('re_cal').value) || 0,
        intensity: document.getElementById('re_int').value || 'medium',
        source: 'ai_image',
      });
      toast('运动记录已保存');
    }
    closeModal('recogResultModal');
    loadDashboard();
  } catch (e) { toast('保存失败: ' + e.message); }
}

// ===== Chat =====
async function loadChatSessions() {
  try {
    var res = await api('GET', '/ai/chat/sessions');
    var sessions = res.data || [];
    var el = document.getElementById('chatSessionList');
    if (sessions.length === 0) {
      el.innerHTML = '<div class="empty"><div class="ico">\u{1F4AC}</div><div class="txt">开始你的第一次对话<br>AI 助手将为你提供健康建议</div></div>';
      return;
    }
    el.innerHTML = sessions.map(function(s) {
      var t = new Date(s.updated_at);
      var timeStr = (t.getMonth() + 1) + '/' + t.getDate() + ' ' + t.getHours() + ':' + String(t.getMinutes()).padStart(2, '0');
      return '<div class="chat-list-item" onclick="openChatSession(\'' + s.id + '\', \'' + s.title.replace(/'/g, "\\'") + '\')">' +
        '<div class="chat-list-title">' + s.title + '</div>' +
        '<div class="chat-list-time">' + timeStr + '</div></div>';
    }).join('');
  } catch (e) { console.error('Chat sessions err:', e); }
}

async function createChatSession() {
  try {
    var res = await api('POST', '/ai/chat/sessions');
    var session = res.data;
    openChatSession(session.id, session.title);
  } catch (e) { toast('创建对话失败: ' + e.message); }
}

async function openChatSession(id, title) {
  currentSessionId = id;
  document.getElementById('chatViewTitle').textContent = title || '对话';
  document.getElementById('chatView').classList.add('active');
  document.getElementById('chatMessages').innerHTML = '';
  document.getElementById('chatInput').value = '';

  try {
    var res = await api('GET', '/ai/chat/sessions/' + id + '/messages');
    var msgs = res.data || [];
    var container = document.getElementById('chatMessages');
    if (msgs.length === 0) {
      container.innerHTML = '<div class="msg assistant"><div class="msg-bubble">你好！我是你的 AI 健康助手。可以问我关于饮食、运动、健康计划的任何问题！</div></div>';
    } else {
      container.innerHTML = msgs.map(function(m) {
        return '<div class="msg ' + m.role + '"><div class="msg-bubble">' + escapeHtml(m.content) + '</div></div>';
      }).join('');
    }
    container.scrollTop = container.scrollHeight;
  } catch (e) { console.error('Load messages err:', e); }
}

function closeChatView() {
  document.getElementById('chatView').classList.remove('active');
  currentSessionId = null;
  loadChatSessions();
}

function escapeHtml(text) {
  var div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

async function sendChat() {
  if (chatStreaming) return;
  var input = document.getElementById('chatInput');
  var msg = input.value.trim();
  if (!msg || !currentSessionId) return;

  input.value = '';
  chatStreaming = true;
  document.getElementById('chatSendBtn').disabled = true;

  var container = document.getElementById('chatMessages');

  // Add user message
  container.innerHTML += '<div class="msg user"><div class="msg-bubble">' + escapeHtml(msg) + '</div></div>';

  // Add assistant placeholder
  var assistantDiv = document.createElement('div');
  assistantDiv.className = 'msg assistant';
  var bubble = document.createElement('div');
  bubble.className = 'msg-bubble';
  bubble.textContent = '...';
  assistantDiv.appendChild(bubble);
  container.appendChild(assistantDiv);
  container.scrollTop = container.scrollHeight;

  try {
    var response = await fetch(API + '/ai/chat/sessions/' + currentSessionId + '/messages', {
      method: 'POST',
      headers: hdrs(),
      body: JSON.stringify({ content: msg }),
    });

    var reader = response.body.getReader();
    var decoder = new TextDecoder();
    var fullText = '';

    while (true) {
      var result = await reader.read();
      if (result.done) break;
      var chunk = decoder.decode(result.value, { stream: true });
      var lines = chunk.split('\n');
      for (var i = 0; i < lines.length; i++) {
        var line = lines[i].trim();
        if (line.startsWith('data: ')) {
          var data = line.substring(6);
          if (data === '[DONE]') continue;
          if (data.startsWith('[ERROR]')) {
            fullText += ' (错误: ' + data.substring(8) + ')';
            continue;
          }
          fullText += data;
          bubble.textContent = fullText;
          container.scrollTop = container.scrollHeight;
        }
      }
    }
  } catch (e) {
    bubble.textContent = '发送失败: ' + e.message;
  }

  chatStreaming = false;
  document.getElementById('chatSendBtn').disabled = false;
}

// ===== Statistics =====
function setStatPeriod(days, btn) {
  statDays = days;
  document.querySelectorAll('.stat-period-btn').forEach(function(b) { b.classList.remove('active'); });
  btn.classList.add('active');
  loadStats();
}

async function loadStats() {
  loadCalorieTrend();
  loadWeightTrend();
  loadActivePlan();
}

async function loadCalorieTrend() {
  try {
    var res = await api('GET', '/stats/calorie-trend?days=' + statDays);
    var data = res.data;
    drawBarChart('calChart', data.points || [], data.average, 'var(--primary)');
    var el = document.getElementById('calChartSummary');
    if (data.average) {
      el.innerHTML = '<span class="chart-summary-item">平均: <strong>' + Math.round(data.average) + ' kcal</strong></span>';
    } else {
      el.innerHTML = '<span class="chart-summary-item">暂无数据</span>';
    }
  } catch (e) { console.error('Calorie trend err:', e); }
}

async function loadWeightTrend() {
  try {
    var res = await api('GET', '/stats/weight-trend?days=' + statDays);
    var data = res.data;
    drawLineChart('wtChart', data.points || [], 'var(--accent)');
    var el = document.getElementById('wtChartSummary');
    if (data.min_value && data.max_value) {
      el.innerHTML = '<span class="chart-summary-item">最低: <strong>' + data.min_value + ' kg</strong></span>' +
        '<span class="chart-summary-item">最高: <strong>' + data.max_value + ' kg</strong></span>';
    } else {
      el.innerHTML = '<span class="chart-summary-item">暂无数据</span>';
    }
  } catch (e) { console.error('Weight trend err:', e); }
}

function drawBarChart(svgId, points, avg, color) {
  var svg = document.getElementById(svgId);
  if (!points.length) { svg.innerHTML = '<text x="160" y="60" text-anchor="middle" fill="#C7C7CC" font-size="13">暂无数据</text>'; return; }
  var w = 320, h = 120, pad = 20;
  var maxVal = Math.max.apply(null, points.map(function(p) { return p.value; })) || 1;
  var barW = Math.min(30, (w - pad * 2) / points.length - 4);
  var html = '';
  points.forEach(function(p, i) {
    var x = pad + i * ((w - pad * 2) / points.length) + ((w - pad * 2) / points.length - barW) / 2;
    var barH = (p.value / maxVal) * (h - pad * 2);
    var y = h - pad - barH;
    html += '<rect x="' + x + '" y="' + y + '" width="' + barW + '" height="' + barH + '" rx="3" fill="' + color + '" opacity="0.7"/>';
    // Date label
    var d = new Date(p.date + 'T00:00:00');
    html += '<text x="' + (x + barW / 2) + '" y="' + (h - 4) + '" text-anchor="middle" fill="#8E8E93" font-size="9">' + (d.getMonth() + 1) + '/' + d.getDate() + '</text>';
  });
  if (avg) {
    var avgY = h - pad - (avg / maxVal) * (h - pad * 2);
    html += '<line x1="' + pad + '" y1="' + avgY + '" x2="' + (w - pad) + '" y2="' + avgY + '" stroke="#C7C7CC" stroke-dasharray="4,3" stroke-width="1"/>';
  }
  svg.innerHTML = html;
}

function drawLineChart(svgId, points, color) {
  var svg = document.getElementById(svgId);
  if (!points.length) { svg.innerHTML = '<text x="160" y="60" text-anchor="middle" fill="#C7C7CC" font-size="13">暂无数据</text>'; return; }
  var w = 320, h = 120, pad = 20;
  var vals = points.map(function(p) { return p.value; });
  var minV = Math.min.apply(null, vals);
  var maxV = Math.max.apply(null, vals);
  var range = maxV - minV || 1;

  var pathParts = [];
  var dots = '';
  points.forEach(function(p, i) {
    var x = pad + i * ((w - pad * 2) / (points.length - 1 || 1));
    var y = h - pad - ((p.value - minV) / range) * (h - pad * 2);
    pathParts.push((i === 0 ? 'M' : 'L') + x + ',' + y);
    dots += '<circle cx="' + x + '" cy="' + y + '" r="3" fill="' + color + '"/>';
    var d = new Date(p.date + 'T00:00:00');
    dots += '<text x="' + x + '" y="' + (h - 4) + '" text-anchor="middle" fill="#8E8E93" font-size="9">' + (d.getMonth() + 1) + '/' + d.getDate() + '</text>';
  });

  var html = '<path d="' + pathParts.join(' ') + '" fill="none" stroke="' + color + '" stroke-width="2" stroke-linejoin="round"/>' + dots;
  svg.innerHTML = html;
}

async function loadActivePlan() {
  try {
    var res = await api('GET', '/plans/active');
    var plan = res.data;
    var el = document.getElementById('planArea');
    if (!plan) {
      el.innerHTML = '<div style="text-align:center;padding:20px;">' +
        '<div style="font-size:14px;color:var(--text-secondary);margin-bottom:12px;">还没有健身计划</div>' +
        '<button class="btn btn-primary btn-sm" style="width:auto;padding:10px 24px;" onclick="openGenPlan()">生成 AI 计划</button></div>';
      return;
    }
    var goals = { lose_weight: '减脂', gain_muscle: '增肌', maintain: '保持' };
    el.innerHTML = '<div class="plan-card">' +
      '<div class="ttl">' + (goals[plan.goal_type] || plan.goal_type) + '计划 \u00B7 ' + plan.duration_weeks + '周</div>' +
      '<div class="plan-grid">' +
      '<div class="plan-item"><div class="v">' + (plan.daily_calorie_target || '--') + '</div><div class="l">每日热量(kcal)</div></div>' +
      '<div class="plan-item"><div class="v">' + (plan.daily_exercise_minutes || '--') + '</div><div class="l">每日运动(分钟)</div></div>' +
      '<div class="plan-item"><div class="v">' + (plan.daily_protein_target || '--') + '</div><div class="l">蛋白质(g)</div></div>' +
      '<div class="plan-item"><div class="v">' + (plan.calorie_deficit || '--') + '</div><div class="l">热量缺口(kcal)</div></div>' +
      '</div></div>' +
      '<button class="btn btn-outline btn-sm" style="width:auto" onclick="openGenPlan()">重新生成</button>';
  } catch (e) { console.error('Plan err:', e); }
}

function openGenPlan() {
  document.getElementById('planModal').classList.add('active');
}

function pickPlanGoal(el) {
  document.querySelectorAll('#planGoalPills .pill').forEach(function(p) { p.classList.remove('active'); });
  el.classList.add('active');
  planGoalType = el.dataset.goal;
}

async function generatePlan() {
  var btn = document.getElementById('genPlanBtn');
  btn.textContent = '生成中...';
  btn.disabled = true;
  try {
    await api('POST', '/plans/generate', {
      goal_type: planGoalType,
      duration_weeks: parseInt(document.getElementById('planWeeks').value) || 4,
    });
    closeModal('planModal');
    toast('健身计划已生成');
    loadActivePlan();
    // Refresh user data since calorie target may have changed
    var me = await api('GET', '/users/me');
    currentUser = me.data;
    loadDashboard();
  } catch (e) {
    toast('生成失败: ' + e.message);
  } finally {
    btn.textContent = '生成计划';
    btn.disabled = false;
  }
}

// ===== Profile =====
async function loadProfile() {
  try {
    var res = await api('GET', '/users/me');
    var u = res.data;
    currentUser = u;
    document.getElementById('profName').textContent = u.nickname || '未设置昵称';
    document.getElementById('profPhone').textContent = u.phone;
    document.getElementById('profH').textContent = u.height_cm || '--';
    document.getElementById('profW').textContent = u.current_weight_kg || '--';
    var goals = { lose_weight: '减脂', build_muscle: '增肌', maintain: '保持', improve_health: '健康' };
    document.getElementById('profG').textContent = goals[u.fitness_goal] || '--';
    document.getElementById('profCal').textContent = (u.daily_calorie_target || 2000) + ' kcal \u203A';
    var providers = { kimi: 'Kimi', gemini: 'Gemini', auto: '自动' };
    document.getElementById('profAi').textContent = (providers[u.ai_provider] || 'Kimi') + ' \u203A';
  } catch (e) { console.error('Profile err:', e); }
}

function openEditProfile() {
  document.getElementById('profileModal').classList.add('active');
  if (currentUser) {
    document.getElementById('editH').value = currentUser.height_cm || '';
    document.getElementById('editW').value = currentUser.current_weight_kg || '';
    document.getElementById('editTW').value = currentUser.target_weight_kg || '';
    selectedGoal = currentUser.fitness_goal || 'lose_weight';
    document.querySelectorAll('#goalPills .pill').forEach(function(p) {
      p.classList.toggle('active', p.dataset.goal === selectedGoal);
    });
  }
}

function pickGoal(el) {
  document.querySelectorAll('#goalPills .pill').forEach(function(p) { p.classList.remove('active'); });
  el.classList.add('active');
  selectedGoal = el.dataset.goal;
}

async function saveProfile() {
  try {
    await api('PUT', '/users/me', {
      height_cm: parseFloat(document.getElementById('editH').value) || null,
      current_weight_kg: parseFloat(document.getElementById('editW').value) || null,
      target_weight_kg: parseFloat(document.getElementById('editTW').value) || null,
      fitness_goal: selectedGoal,
    });
    closeModal('profileModal');
    toast('个人信息已更新');
    loadProfile();
  } catch (e) { toast('保存失败: ' + e.message); }
}

function openCalTarget() {
  var target = prompt('设置每日卡路里目标 (kcal):', (currentUser && currentUser.daily_calorie_target) || 2000);
  if (target && !isNaN(parseInt(target))) {
    api('PUT', '/users/me', { daily_calorie_target: parseInt(target) })
      .then(function() { toast('目标已更新'); loadProfile(); loadDashboard(); })
      .catch(function(e) { toast('更新失败: ' + e.message); });
  }
}

function openAiPref() {
  var current = (currentUser && currentUser.ai_provider) || 'kimi';
  var next = current === 'kimi' ? 'gemini' : current === 'gemini' ? 'auto' : 'kimi';
  api('PUT', '/users/me', { ai_provider: next })
    .then(function() { toast('AI 服务已切换为 ' + next); loadProfile(); })
    .catch(function(e) { toast('更新失败: ' + e.message); });
}

// ===== Init =====
if (token) {
  api('GET', '/users/me').then(function() { enterApp(); }).catch(function() {
    token = '';
    localStorage.removeItem('gs_token');
  });
}
