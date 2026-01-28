# TAUROS NEXUS - COMPLETION TASK

## CONTEXT
TAUROS NEXUS: Multi-AI distributed system (Telegram Bot + Web Dashboard + REST API + AI Engine).
Current state: 85% complete, production-grade architecture, needs critical components.

**Tech Stack:**
- Python 3.10+, asyncio, aiohttp
- SQLite (NexusDatabase with full schema)
- Flask + Flask-SocketIO (web/API)
- python-telegram-bot 20+ (bot)
- OpenAI, Anthropic, Mistral, Ollama APIs

**Architecture:**
```
nexus_core.py       → Core engine (NexusCore, UserManager, NexusAI, Database)
telegram_bot.py     → Bot with inline menus, command handlers
web_dashboard.py    → Dashboard with WebSocket real-time updates
api_server.py       → REST API with authentication
main.py             → Unified launcher (multi-thread/async)
```

---

## TASKS - PRIORITY ORDER

### 1. IMPLEMENT MISSING AI PROVIDERS

**File:** `nexus_core.py` (after line 492, after OllamaProvider)

**Requirements:**
- Create `AnthropicProvider(AIProvider)` class
  - Endpoint: `https://api.anthropic.com/v1/messages`
  - Models: claude-3-opus-20240229, claude-3-sonnet-20240229, claude-3-haiku-20240307
  - Use Messages API format (NOT completion format)
  - Handle streaming with `stream: true`
  
- Create `MistralProvider(AIProvider)` class
  - Endpoint: `https://api.mistral.ai/v1/chat/completions`
  - Models: mistral-large-latest, mistral-medium-latest
  - OpenAI-compatible format
  - Handle streaming

**Both providers must:**
- Implement `async def generate(messages, model, **kwargs) -> str`
- Implement `async def stream_generate(messages, model, **kwargs)` (async generator)
- Handle errors gracefully with try/except
- Use aiohttp.ClientSession()
- Return clean text responses

**Update `NexusAI._init_providers()` method:**
```python
if NexusConfig.ANTHROPIC_KEY:
    self.providers['anthropic'] = AnthropicProvider(NexusConfig.ANTHROPIC_KEY)
    log.info("✅ Provider Anthropic inizializzato")

if NexusConfig.MISTRAL_KEY:
    self.providers['mistral'] = MistralProvider(NexusConfig.MISTRAL_KEY)
    log.info("✅ Provider Mistral inizializzato")
```

---

### 2. COMPLETE WEB DASHBOARD TEMPLATE

**File:** `web_dashboard.py` (lines 218-476 are truncated)

**Missing components:**
1. Stats cards HTML (after line 217):
   - Total Users card
   - Unlocked Users card
   - Total Commands card
   - AI Sessions card
   - Commands Today card
   - Unlock Rate card
   - Each card: glass background, icon, value, label, trend indicator

2. Charts section:
```html
   <canvas id="activityChart"></canvas>
   <canvas id="commandsChart"></canvas>
```

3. Users table with columns: Username, Level, Commands, Last Activity

4. Logs table with columns: Timestamp, Command, Status, Execution Time

5. JavaScript section (before {% endblock %}):
```javascript
   // Chart.js initialization
   const activityChart = new Chart(ctx1, {
     type: 'line',
     data: { labels: {{ activity_data.labels|tojson }}, datasets: [...] }
   });
   
   const commandsChart = new Chart(ctx2, {
     type: 'doughnut',
     data: { labels: {{ commands_data.labels|tojson }}, datasets: [...] }
   });
   
   // WebSocket handlers
   const socket = io();
   socket.on('stats_update', (data) => { /* update UI */ });
   socket.on('new_activity', (data) => { /* append to logs */ });
```

**Style:** Modern glassmorphism, gradient accents, responsive grid layout.

---

### 3. IMPLEMENT TELEGRAM BROADCAST

**File:** `telegram_bot.py` (replace placeholder at ~line 260)

**Function:** `async def handle_broadcast(self, update, context)`

**Logic:**
1. Check user level >= 3 (Architect)
2. Parse message from `/broadcast <text>`
3. Fetch all user_ids from database
4. Loop: send message to each user with rate limiting (0.1s sleep)
5. Count sent/failed
6. Reply with summary

**Error handling:** Catch telegram.error exceptions per user, log failures, continue loop.

---

### 4. CREATE EXAMPLE PLUGIN

**File:** `plugins/weather_plugin.py` (new file)

**Class:** `WeatherPlugin(NexusPlugin)`
- plugin_id: "weather"
- Register command: `/weather <city>`
- Call free weather API (e.g., wttr.in or openweathermap)
- Return formatted weather string with emoji

**File:** `nexus_core.py` (add method to NexusCore)
```python
async def load_plugin(self, plugin_class: type):
    """Load and register plugin"""
    plugin = plugin_class(self)
    await plugin.on_load()
    self.plugins[plugin.plugin_id] = plugin
    # Save to DB
    log.nexus(f"Plugin loaded: {plugin.name} v{plugin.version}")

async def unload_plugin(self, plugin_id: str):
    """Unload plugin"""
    if plugin_id in self.plugins:
        await self.plugins[plugin_id].on_unload()
        del self.plugins[plugin_id]
```

---

### 5. PERSIST API KEYS IN DATABASE

**File:** `api_server.py`

**Changes:**
1. Add schema to `nexus_core.py` (in init_schema):
```sql
   CREATE TABLE IF NOT EXISTS api_keys (
       key_hash TEXT PRIMARY KEY,
       user_id INTEGER,
       access_level INTEGER,
       name TEXT,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       last_used TIMESTAMP,
       FOREIGN KEY (user_id) REFERENCES users(user_id)
   );
```

2. Replace `API_KEYS` dict with DB lookups:
```python
   def get_api_key_info(api_key: str) -> Optional[Dict]:
       nexus = get_nexus()
       key_hash = hashlib.sha256(api_key.encode()).hexdigest()
       return nexus.db.fetch_one(
           "SELECT * FROM api_keys WHERE key_hash = ?", (key_hash,)
       )
```

3. Update `generate_api_key()` to write to DB

---

## CONSTRAINTS

**DO:**
- Write production-ready code, no placeholders
- Handle errors with try/except
- Use existing patterns from codebase
- Add logging with `log.info()`, `log.error()`
- Follow async/await patterns
- Use type hints
- Keep Italian language in user-facing strings

**DON'T:**
- Mock implementations
- Hardcoded test data
- Breaking changes to existing API
- Remove existing functionality
- Change database schema without migrations

---

## TESTING CHECKLIST

After implementation, verify:
- [ ] All AI providers work with real API keys
- [ ] Dashboard renders without errors
- [ ] Charts display data correctly
- [ ] WebSocket updates work real-time
- [ ] Broadcast sends to all users
- [ ] Plugin loads and command registers
- [ ] API keys authenticate correctly
- [ ] No console errors in browser
- [ ] No Python exceptions in logs

---

## OUTPUT

Provide complete, working code for each file modification. Include:
1. Full function/class implementations
2. Any new imports needed
3. Schema changes if applicable
4. Brief comment explaining non-obvious logic

**Format:** Ready-to-paste code blocks with file paths.
