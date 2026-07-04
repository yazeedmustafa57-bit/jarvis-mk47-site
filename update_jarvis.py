import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Add ElevenLabs settings in the modal
old = '''    <label>Auto-Vorlesen (TTS)</label>
    <select id="tts-toggle">
      <option value="off">Aus</option>
      <option value="on">Ein - Antworten vorlesen</option>
    </select>'''
new = '''    <label>TTS-Engine</label>
    <select id="tts-engine">
      <option value="browser">Browser-TTS</option>
      <option value="elevenlabs" selected>ElevenLabs (Premium)</option>
    </select>
    <div id="elevenlabs-settings">
      <label>ElevenLabs API-Schlüssel</label>
      <input type="password" id="elevenlabs-key-input" placeholder="sk_...">
      <label>Stimme (englisch)</label>
      <select id="elevenlabs-voice-select">
        <option value="21m00Tcm4TlvDq8ikWAM">Rachel</option>
        <option value="AZnzlk1XvdvUeBnXmlld">Domi</option>
        <option value="EXAVITQu4vr2P8n3zFgD">Bella</option>
        <option value="ErXwobaYiN019PkySvjV">Antoni</option>
        <option value="MF3mGyEYCl7XYWbV9V6O">Elli</option>
        <option value="TxGEqnHWrfWFTfGW9XjX">Josh</option>
      </select>
      <label>Stimme (deutsch)</label>
      <select id="elevenlabs-de-voice">
        <option value="21m00Tcm4TlvDq8ikWAM">Rachel (EN)</option>
        <option value="N2lE8t7NStwS7b5hF5jA">Anna (DE)</option>
        <option value="X8zY6iL9qR3vB4nM7cP2">Lena (DE)</option>
      </select>
    </div>
    <label>Auto-Vorlesen (TTS)</label>
    <select id="tts-toggle">
      <option value="off">Aus</option>
      <option value="on" selected>Ein</option>
    </select>'''
html = html.replace(old, new)

# 2. Add EleveLabs variables with hardcoded keys
html = html.replace(
    "let GEMINI_API_KEY = localStorage.getItem('jarvis_gemini_key') || '';",
    "let GEMINI_API_KEY = localStorage.getItem('jarvis_gemini_key') || 'AQ.Ab8RN6IX8CO25B9oLeGkCvApdRYXM4RkZGp-_VXZ9DdtA9R6OA';"
)

html = html.replace(
    "let ttsEnabled = false;",
    "let ttsEnabled = true;\nlet ELEVENLABS_API_KEY = localStorage.getItem('jarvis_elevenlabs_key') || 'sk_3c9dd884344f708d5db4b608f75c86e716ff4322959bfc26';\nlet TTS_ENGINE = 'elevenlabs';\nlet ELEVENLABS_VOICE = '21m00Tcm4TlvDq8ikWAM';\nlet ELEVENLABS_DE_VOICE = 'N2lE8t7NStwS7b5hF5jA';"
)

# 3. Add DOM refs
html = html.replace(
    "const ttsToggle = document.getElementById('tts-toggle');",
    "const ttsToggle = document.getElementById('tts-toggle');\nconst ttsEngine = document.getElementById('tts-engine');\nconst elevenlabsSettings = document.getElementById('elevenlabs-settings');\nconst elevenlabsKeyInput = document.getElementById('elevenlabs-key-input');\nconst elevenlabsVoiceSelect = document.getElementById('elevenlabs-voice-select');\nconst elevenlabsDeVoice = document.getElementById('elevenlabs-de-voice');"
)

# 4. Load ElevenLabs settings
html = html.replace(
    "ttsEnabled = localStorage.getItem('jarvis_tts') === 'true';",
    "ttsEnabled = localStorage.getItem('jarvis_tts') !== 'false';\nELEVENLABS_API_KEY = localStorage.getItem('jarvis_elevenlabs_key') || 'sk_3c9dd884344f708d5db4b608f75c86e716ff4322959bfc26';\nTTS_ENGINE = localStorage.getItem('jarvis_tts_engine') || 'elevenlabs';\nELEVENLABS_VOICE = localStorage.getItem('jarvis_elevenlabs_voice') || '21m00Tcm4TlvDq8ikWAM';\nELEVENLABS_DE_VOICE = localStorage.getItem('jarvis_elevenlabs_de_voice') || 'N2lE8t7NStwS7b5hF5jA';"
)

# 5. Set initial values
html = html.replace(
    "ttsToggle.value = ttsEnabled ? 'on' : 'off';",
    "ttsToggle.value = ttsEnabled ? 'on' : 'off';\nttsEngine.value = TTS_ENGINE;\nif (ELEVENLABS_API_KEY) elevenlabsKeyInput.value = ELEVENLABS_API_KEY;\nif (ELEVENLABS_VOICE) elevenlabsVoiceSelect.value = ELEVENLABS_VOICE;\nif (ELEVENLABS_DE_VOICE) elevenlabsDeVoice.value = ELEVENLABS_DE_VOICE;\nelevenlabsSettings.style.display = TTS_ENGINE === 'elevenlabs' ? 'block' : 'none';\nttsEngine.onchange = function() { elevenlabsSettings.style.display = ttsEngine.value === 'elevenlabs' ? 'block' : 'none'; };"
)

# 6. Save ElevenLabs settings
html = html.replace(
    "localStorage.setItem('jarvis_tts', ttsEnabled ? 'true' : 'false');",
    "localStorage.setItem('jarvis_tts', ttsEnabled ? 'true' : 'false');\nELEVENLABS_API_KEY = elevenlabsKeyInput.value.trim() || 'sk_3c9dd884344f708d5db4b608f75c86e716ff4322959bfc26';\nTTS_ENGINE = ttsEngine.value;\nELEVENLABS_VOICE = elevenlabsVoiceSelect.value;\nELEVENLABS_DE_VOICE = elevenlabsDeVoice.value;\nlocalStorage.setItem('jarvis_elevenlabs_key', ELEVENLABS_API_KEY);\nlocalStorage.setItem('jarvis_tts_engine', TTS_ENGINE);\nlocalStorage.setItem('jarvis_elevenlabs_voice', ELEVENLABS_VOICE);\nlocalStorage.setItem('jarvis_elevenlabs_de_voice', ELEVENLABS_DE_VOICE);"
)

# 7. Replace speak() function
old_speak = '''function speak(text) {
  if (!window.speechSynthesis) return;
  const utterance = new SpeechSynthesisUtterance(text.replace(/[#*_\`]/g, ''));
  utterance.lang = langSelect.value || 'de-DE';
  const selectedVoice = voiceSelect.value;
  if (selectedVoice) {
    const voice = speechSynthesis.getVoices().find(v => v.name === selectedVoice);
    if (voice) utterance.voice = voice;
  }
  utterance.rate = 0.9;
  speechSynthesis.speak(utterance);
}'''

new_speak = '''function speak(text) {
  var cleanText = text.replace(/[#*_\`>]/g, '').replace(/\\[.*?\\]\\(.*?\\)/g, '').substring(0, 2000);
  if (TTS_ENGINE === 'elevenlabs' && ELEVENLABS_API_KEY) {
    speakElevenLabs(cleanText);
  } else {
    speakBrowser(cleanText);
  }
}

function speakBrowser(text) {
  if (!window.speechSynthesis) return;
  window.speechSynthesis.cancel();
  var utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = langSelect.value || 'de-DE';
  var selectedVoice = voiceSelect.value;
  if (selectedVoice) {
    var voice = speechSynthesis.getVoices().find(function(v) { return v.name === selectedVoice; });
    if (voice) utterance.voice = voice;
  }
  utterance.rate = 0.9;
  speechSynthesis.speak(utterance);
}

async function speakElevenLabs(text) {
  try {
    var lang = langSelect.value || 'de-DE';
    var voiceId = lang.startsWith('de') ? ELEVENLABS_DE_VOICE : ELEVENLABS_VOICE;
    var res = await fetch('https://api.elevenlabs.io/v1/text-to-speech/' + voiceId, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'xi-api-key': ELEVENLABS_API_KEY
      },
      body: JSON.stringify({
        text: text,
        model_id: 'eleven_multilingual_v2',
        voice_settings: { stability: 0.5, similarity_boost: 0.75 }
      })
    });
    if (!res.ok) { throw new Error('ElevenLabs Fehler: ' + res.status); }
    var blob = await res.blob();
    var url = URL.createObjectURL(blob);
    var audio = new Audio(url);
    audio.onended = function() { URL.revokeObjectURL(url); };
    await audio.play();
  } catch(e) {
    console.warn('ElevenLabs fehlgeschlagen, nutze Browser-TTS:', e);
    speakBrowser(text);
  }
}'''

html = html.replace(old_speak, new_speak)

with open('index.html', 'w') as f:
    f.write(html)

print("OK")
