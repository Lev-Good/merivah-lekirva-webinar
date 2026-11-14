import os
import re
import html

REPO_DIR = r"c:\Users\משתמש\Downloads\merivah-lekirva-webinar"
PREVIEW_DIR = os.path.join(REPO_DIR, "preview")
EMAILS_DIR = os.path.join(PREVIEW_DIR, "emails")
WHATSAPP_DIR = os.path.join(PREVIEW_DIR, "whatsapp")
SRC_EMAILS_DIR = r"c:\Users\משתמש\Downloads\מיילים וובינר זוג או פרט\מיילים HTML"
SRC_WA_FILE = r"c:\Users\משתמש\Downloads\מיילים וובינר זוג או פרט\הודעות וואטסאפ לקמפיין.md"

os.makedirs(EMAILS_DIR, exist_ok=True)
os.makedirs(WHATSAPP_DIR, exist_ok=True)

# List of emails to process
emails_meta = [
    {
        "id": "A4",
        "title": "כשמתחילה מריבה, מה הדפוס שלכם?",
        "series": "סדרה A — תפוצה כללית",
        "timing": "יום ראשון 15.11",
        "audience": "רשימת תפוצה (למי שטרם נרשם)",
        "file": "A4 - כשמתחילה מריבה מה הדפוס שלכם.html",
        "badge": "ראשון 15.11"
    },
    {
        "id": "A7",
        "title": "מחר בערב: שני משפטים שישנו לכם את המריבה הבאה",
        "series": "סדרה A — תפוצה כללית",
        "timing": "יום שלישי 17.11",
        "audience": "רשימת תפוצה (למי שטרם נרשם)",
        "file": "A7 - מחר בערב שני משפטים שישנו לכם את המריבה הבאה.html",
        "badge": "שלישי 17.11"
    },
    {
        "id": "A9",
        "title": "הערב ב־20:30 — וזו הפעם היחידה",
        "series": "סדרה A — תפוצה כללית",
        "timing": "יום רביעי 18.11 (בוקר)",
        "audience": "רשימת תפוצה (למי שטרם נרשם)",
        "file": "A9 - הערב ב-20-30 וזו הפעם היחידה.html",
        "badge": "רביעי 18.11 בוקר"
    },
    {
        "id": "A8",
        "title": "מה היה אתמול בערב — ואיך אפשר עדיין לקבל את זה",
        "series": "סדרה A — תפוצה כללית",
        "timing": "יום חמישי 19.11 (בוקר)",
        "audience": "רשימת תפוצה (למי שטרם נרשם — רכישת הקלטה)",
        "file": "A8 - מה היה אתמול בערב.html",
        "badge": "חמישי 19.11"
    },
    {
        "id": "R1",
        "title": "ההרשמה התקבלה — ומה מחכה לכם ביום רביעי",
        "series": "סדרה R — רצף לנרשמים",
        "timing": "מיידי בהרשמה (קבוצה 1070109)",
        "audience": "נרשמים חדשים למפגש",
        "file": "R1 - תודה שנרשמתם למפגש ממריבה לקרבה (נוסח מעודכן).html",
        "badge": "מיידי בהרשמה"
    },
    {
        "id": "R2",
        "title": "מה קורה אצלכם בשיחות שלא תמיד שמים לב אליו?",
        "series": "סדרה R — רצף לנרשמים",
        "timing": "יום ראשון 15.11",
        "audience": "כל הנרשמים (שאלון קצר)",
        "file": "R2 - מה קורה אצלכם בשיחות שאלון (נוסח מעודכן).html",
        "badge": "ראשון 15.11"
    },
    {
        "id": "R3",
        "title": "שני דברים שתיקחו איתכם כבר באותו ערב",
        "series": "סדרה R — רצף לנרשמים",
        "timing": "יום שני 16.11",
        "audience": "כל הנרשמים",
        "file": "R3 - שני דברים שתיקחו איתכם.html",
        "badge": "שני 16.11"
    },
    {
        "id": "R4",
        "title": "מחר ב-20:30 — ושאלה אחת להחזיק בראש עד אז",
        "series": "סדרה R — רצף לנרשמים",
        "timing": "יום שלישי 17.11",
        "audience": "כל הנרשמים",
        "file": "R4 - מחר ב-20-30 ושאלה אחת.html",
        "badge": "שלישי 17.11"
    },
    {
        "id": "R5",
        "title": "היום ב-20:30",
        "series": "סדרה R — רצף לנרשמים",
        "timing": "יום רביעי 18.11 (בוקר)",
        "audience": "כל הנרשמים (הכנה לקראת הערב)",
        "file": "R5 - היום ב-20-30.html",
        "badge": "רביעי 18.11 בוקר"
    },
    {
        "id": "R6",
        "title": "עוד רבע שעה מתחילים",
        "series": "סדרה R — רצף לנרשמים",
        "timing": "יום רביעי 18.11, בשעה 19:45",
        "audience": "כל הנרשמים (תזכורת קישור לזום)",
        "file": "R6 - עוד רבע שעה מתחילים.html",
        "badge": "רביעי 19:45"
    },
    {
        "id": "R7B",
        "title": "מה שדיברנו עליו הערב — ואיך ממשיכים איתו",
        "series": "סדרה R — רצף לנרשמים",
        "timing": "יום רביעי 18.11, בשעה 22:15",
        "audience": "נוכחים בשידור בלבד (הטבת קורס עד חצות)",
        "file": "R7B - מה שדיברנו עליו הערב ואיך ממשיכים.html",
        "badge": "רביעי 22:15"
    },
    {
        "id": "R8",
        "title": "עוד 45 דקות",
        "series": "סדרה R — רצף לנרשמים",
        "timing": "יום רביעי 18.11, בשעה 23:15",
        "audience": "נוכחים שטרם רכשו (תזכורת חצות)",
        "file": "R8 - עוד 45 דקות נעילת מבצע.html",
        "badge": "רביעי 23:15"
    },
    {
        "id": "R7A",
        "title": "לא הצלחתם להיות איתנו? יש דרך אחת להשיג את מה שנתנו שם",
        "series": "סדרה R — רצף לנרשמים",
        "timing": "יום חמישי 19.11 (בוקר)",
        "audience": "נרשמים שלא נכחו בשידור (רכישת הקלטה ב-47 ₪)",
        "file": "R7A - לא הצלחתם להיות איתנו הקלטה.html",
        "badge": "חמישי 19.11"
    }
]

# Generate standalone wrapper pages for each email
for em in emails_meta:
    src_path = os.path.join(SRC_EMAILS_DIR, em["file"])
    with open(src_path, "r", encoding="utf-8") as f:
        raw_email_html = f.read()

    full_page = f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>תצוגה מקדימה • {em['id']} — {em['title']}</title>
  <link href="https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;700;800&display=swap" rel="stylesheet">
  <style>
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 0;
      background-color: #e9e5dc;
      font-family: 'Assistant', sans-serif;
      direction: rtl;
    }}
    .top-nav-bar {{
      position: sticky;
      top: 0;
      z-index: 1000;
      background: #1e352f;
      color: #ffffff;
      padding: 12px 20px;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      box-shadow: 0 4px 15px rgba(0,0,0,0.15);
      border-bottom: 2px solid #b7382d;
    }}
    .top-nav-bar .meta-info {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 15px;
    }}
    .badge-code {{
      background: #b7382d;
      color: white;
      font-weight: 800;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 14px;
    }}
    .badge-time {{
      background: #2d4c42;
      color: #e8c588;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 13px;
    }}
    .nav-actions {{
      display: flex;
      gap: 10px;
    }}
    .nav-btn {{
      background: #ffffff;
      color: #1e352f;
      text-decoration: none;
      padding: 6px 14px;
      border-radius: 6px;
      font-weight: 700;
      font-size: 13.5px;
      transition: all 0.2s;
    }}
    .nav-btn:hover {{
      background: #e8c588;
      color: #1e352f;
    }}
    .email-viewport {{
      max-width: 660px;
      margin: 30px auto 60px auto;
      padding: 0 10px;
    }}
    .info-card {{
      background: white;
      border-radius: 10px;
      padding: 16px 20px;
      margin-bottom: 20px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.06);
      border-right: 4px solid #1e352f;
    }}
    .info-card h2 {{
      margin: 0 0 6px 0;
      font-size: 19px;
      color: #1e352f;
    }}
    .info-card p {{
      margin: 4px 0;
      color: #555;
      font-size: 14.5px;
    }}
  </style>
</head>
<body>

  <div class="top-nav-bar">
    <div class="meta-info">
      <span class="badge-code">{em['id']}</span>
      <span class="badge-time">⏰ {em['timing']}</span>
      <span style="font-weight: 600;">{em['title']}</span>
    </div>
    <div class="nav-actions">
      <a href="../index.html" class="nav-btn">↤ חזרה לכל ההודעות</a>
    </div>
  </div>

  <div class="email-viewport">
    <div class="info-card">
      <h2>שורת נושא: {em['title']}</h2>
      <p><strong>סדרה וקהל יעד:</strong> {em['series']} | {em['audience']}</p>
      <p><strong>תזמון שליחה מיועד:</strong> {em['timing']}</p>
    </div>

    <!-- גוף המייל של פולסים -->
    {raw_email_html}
  </div>

</body>
</html>
"""
    out_file = os.path.join(EMAILS_DIR, f"{em['id']}.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(full_page)

print(f"Generated {len(emails_meta)} standalone email preview pages.")

# Parse WhatsApp messages from markdown
with open(SRC_WA_FILE, "r", encoding="utf-8") as f:
    wa_raw = f.read()

# Pattern for WhatsApp blocks
blocks = re.findall(r"### (W[0-9A-Z]+) — ([^\n]+)\n(.*?)(?=\n### W|\Z)", wa_raw, re.DOTALL)
wa_meta = []

for code, header_title, content in blocks:
    time_m = re.search(r"\* \*\*מועד שליחה:\*\* ([^\n]+)", content)
    aud_m = re.search(r"\* \*\*קהל יעד:\*\* ([^\n]+)", content)
    text_m = re.search(r"```text\n(.*?)\n```", content, re.DOTALL)
    
    timing = time_m.group(1).strip() if time_m else ""
    audience = aud_m.group(1).strip() if aud_m else ""
    body_text = text_m.group(1).strip() if text_m else ""

    wa_meta.append({
        "id": code,
        "title": header_title.strip(),
        "timing": timing,
        "audience": audience,
        "text": body_text
    })

print(f"Found {len(wa_meta)} WhatsApp messages.")

# Generate WhatsApp preview pages
for wa in wa_meta:
    # Convert markdown-style *bold* to <strong>
    formatted_text = html.escape(wa["text"])
    formatted_text = re.sub(r"\*([^\*\n]+)\*", r"<strong>\1</strong>", formatted_text)
    formatted_text = formatted_text.replace("\n", "<br>")
    
    # Auto-link URLs
    formatted_text = re.sub(r"(https?://[^\s<]+)", r'<a href="\1" target="_blank" style="color: #027eb5; text-decoration: underline; word-break: break-all;">\1</a>', formatted_text)

    wa_page = f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>תצוגה מקדימה וואטסאפ • {wa['id']} — {wa['title']}</title>
  <link href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700;800&display=swap" rel="stylesheet">
  <style>
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 0;
      background-color: #0c1317;
      font-family: 'Assistant', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      direction: rtl;
      display: flex;
      flex-direction: column;
      min-height: 100vh;
    }}
    .top-nav-bar {{
      background: #1f2c34;
      color: #e9edef;
      padding: 12px 20px;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
      border-bottom: 1px solid rgba(255,255,255,0.1);
    }}
    .meta-info {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 15px;
    }}
    .badge-code {{
      background: #00a884;
      color: white;
      font-weight: 800;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 14px;
    }}
    .badge-time {{
      background: #111b21;
      color: #8696a0;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 13px;
    }}
    .nav-btn {{
      background: #00a884;
      color: white;
      text-decoration: none;
      padding: 7px 16px;
      border-radius: 6px;
      font-weight: 700;
      font-size: 13.5px;
      transition: background 0.2s;
    }}
    .nav-btn:hover {{ background: #06cf9c; }}
    
    .chat-container {{
      max-width: 580px;
      width: 100%;
      margin: 30px auto;
      padding: 0 16px;
      flex: 1;
    }}
    .chat-header {{
      background: #202c33;
      padding: 12px 16px;
      border-radius: 14px 14px 0 0;
      display: flex;
      align-items: center;
      gap: 12px;
      border-bottom: 1px solid rgba(255,255,255,0.06);
    }}
    .avatar {{
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: #00a884;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 18px;
    }}
    .chat-header-text h3 {{
      margin: 0;
      color: #e9edef;
      font-size: 16.5px;
      font-weight: 700;
    }}
    .chat-header-text p {{
      margin: 2px 0 0 0;
      color: #8696a0;
      font-size: 13px;
    }}
    
    .chat-body {{
      background-color: #0b141a;
      background-image: radial-gradient(#1f2c34 1px, transparent 1px);
      background-size: 20px 20px;
      padding: 24px 18px;
      border-radius: 0 0 14px 14px;
      box-shadow: 0 8px 30px rgba(0,0,0,0.4);
    }}
    
    .bubble {{
      background: #005c4b;
      color: #e9edef;
      border-radius: 12px 0 12px 12px;
      padding: 14px 18px 24px 18px;
      position: relative;
      font-size: 16px;
      line-height: 1.65;
      box-shadow: 0 2px 6px rgba(0,0,0,0.25);
    }}
    .bubble .msg-time {{
      position: absolute;
      bottom: 6px;
      left: 10px;
      font-size: 12px;
      color: #8696a0;
      display: flex;
      align-items: center;
      gap: 4px;
    }}
    .ticks {{
      color: #53bdeb;
      font-size: 13px;
    }}
    .copy-box {{
      margin-top: 25px;
      text-align: center;
    }}
    .copy-btn {{
      background: #202c33;
      color: #00a884;
      border: 1px solid #00a884;
      padding: 10px 22px;
      border-radius: 8px;
      font-size: 15px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .copy-btn:hover {{
      background: #00a884;
      color: white;
    }}
    .copy-success {{
      color: #00a884;
      font-size: 13.5px;
      margin-top: 8px;
      display: none;
    }}
  </style>
</head>
<body>

  <div class="top-nav-bar">
    <div class="meta-info">
      <span class="badge-code">{wa['id']}</span>
      <span class="badge-time">⏰ {wa['timing']}</span>
      <span style="font-weight: 600;">{wa['title']}</span>
    </div>
    <div>
      <a href="../index.html" class="nav-btn">↤ חזרה לכל ההודעות</a>
    </div>
  </div>

  <div class="chat-container">
    <div class="chat-header">
      <div class="avatar">יס</div>
      <div class="chat-header-text">
        <h3>יובל סודאי • זוג או פרט</h3>
        <p>קבוצה 1070110 • {wa['timing']}</p>
      </div>
    </div>
    
    <div class="chat-body">
      <div class="bubble">
        <div>{formatted_text}</div>
        <div class="msg-time">
          <span>{wa['id']}</span>
          <span class="ticks">✓✓</span>
        </div>
      </div>

      <div class="copy-box">
        <button class="copy-btn" onclick="copyText()">📋 העתק נוסח וואטסאפ נקי</button>
        <div id="copied-msg" class="copy-success">✓ הנוסח הועתק בהצלחה ללוח!</div>
      </div>
    </div>
  </div>

  <textarea id="raw-text" style="display:none;">{wa['text']}</textarea>

  <script>
    function copyText() {{
      const text = document.getElementById('raw-text').value;
      navigator.clipboard.writeText(text).then(() => {{
        const msg = document.getElementById('copied-msg');
        msg.style.display = 'block';
        setTimeout(() => {{ msg.style.display = 'none'; }}, 3000);
      }});
    }}
  </script>

</body>
</html>
"""
    out_file = os.path.join(WHATSAPP_DIR, f"{wa['id']}.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(wa_page)

print(f"Generated {len(wa_meta)} WhatsApp preview pages.")

# Generate Master Index Portal (preview/index.html)
email_cards_html = ""
for em in emails_meta:
    email_cards_html += f"""
    <div class="item-card">
      <div class="card-header">
        <span class="badge email-badge">{em['id']}</span>
        <span class="badge-timing">⏰ {em['timing']}</span>
      </div>
      <h3 class="card-title">{em['title']}</h3>
      <p class="card-meta"><strong>קהל יעד:</strong> {em['audience']}</p>
      <div class="card-actions">
        <a href="emails/{em['id']}.html" target="_blank" class="preview-btn email-btn">צפייה במייל המעוצב ↗</a>
      </div>
    </div>
    """

wa_cards_html = ""
for wa in wa_meta:
    wa_cards_html += f"""
    <div class="item-card">
      <div class="card-header">
        <span class="badge wa-badge">{wa['id']}</span>
        <span class="badge-timing">⏰ {wa['timing']}</span>
      </div>
      <h3 class="card-title">{wa['title']}</h3>
      <p class="card-meta"><strong>קהל יעד:</strong> {wa['audience']}</p>
      <div class="card-actions">
        <a href="whatsapp/{wa['id']}.html" target="_blank" class="preview-btn wa-btn">צפייה בתצוגת וואטסאפ ↗</a>
      </div>
    </div>
    """

index_html = f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>פורטל תצוגה מקדימה • קמפיין ״ממריבה לקִרבה״ (יובל סודאי)</title>
  <link href="https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;700;800&display=swap" rel="stylesheet">
  <style>
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 0;
      background-color: #f4f1ea;
      font-family: 'Assistant', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
      color: #2b2b2b;
      direction: rtl;
    }}
    .hero {{
      background: linear-gradient(135deg, #1e352f 0%, #29473f 100%);
      color: white;
      padding: 40px 20px;
      text-align: center;
      box-shadow: 0 4px 20px rgba(0,0,0,0.15);
      border-bottom: 4px solid #b7382d;
    }}
    .hero h1 {{
      margin: 0 0 10px 0;
      font-size: 32px;
      font-weight: 800;
    }}
    .hero p {{
      margin: 0 auto;
      max-width: 700px;
      font-size: 18px;
      color: #e5ede9;
      line-height: 1.6;
    }}
    .hero .tagline {{
      display: inline-block;
      margin-top: 15px;
      background: #b7382d;
      color: white;
      padding: 6px 16px;
      border-radius: 50px;
      font-weight: 700;
      font-size: 14.5px;
    }}
    .container {{
      max-width: 1100px;
      margin: 40px auto;
      padding: 0 20px;
    }}
    .section-header {{
      display: flex;
      align-items: center;
      gap: 12px;
      margin: 40px 0 20px 0;
      padding-bottom: 12px;
      border-bottom: 2px solid #dfd7cb;
    }}
    .section-header h2 {{
      margin: 0;
      font-size: 26px;
      color: #1e352f;
      font-weight: 800;
    }}
    .section-desc {{
      margin: -10px 0 25px 0;
      color: #666;
      font-size: 16px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 20px;
      margin-bottom: 40px;
    }}
    .item-card {{
      background: white;
      border-radius: 12px;
      padding: 22px;
      box-shadow: 0 3px 12px rgba(0,0,0,0.06);
      border: 1px solid #ebd9c8;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.2s, box-shadow 0.2s;
    }}
    .item-card:hover {{
      transform: translateY(-3px);
      box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }}
    .card-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }}
    .badge {{
      font-weight: 800;
      padding: 4px 12px;
      border-radius: 6px;
      font-size: 14px;
      color: white;
    }}
    .email-badge {{ background: #1e352f; }}
    .wa-badge {{ background: #00a884; }}
    .badge-timing {{
      font-size: 13.5px;
      color: #7d6b5c;
      font-weight: 700;
    }}
    .card-title {{
      margin: 0 0 10px 0;
      font-size: 18.5px;
      color: #1e352f;
      line-height: 1.4;
      font-weight: 700;
    }}
    .card-meta {{
      margin: 0 0 18px 0;
      font-size: 14.5px;
      color: #666;
      line-height: 1.5;
    }}
    .card-actions {{
      margin-top: auto;
    }}
    .preview-btn {{
      display: block;
      text-align: center;
      padding: 12px 18px;
      border-radius: 8px;
      font-weight: 800;
      text-decoration: none;
      font-size: 15.5px;
      transition: all 0.2s;
    }}
    .email-btn {{
      background: #1e352f;
      color: white;
    }}
    .email-btn:hover {{
      background: #b7382d;
    }}
    .wa-btn {{
      background: #00a884;
      color: white;
    }}
    .wa-btn:hover {{
      background: #038064;
    }}
    .footer {{
      text-align: center;
      padding: 30px;
      color: #888;
      font-size: 14px;
      border-top: 1px solid #dfd7cb;
      margin-top: 60px;
    }}
  </style>
</head>
<body>

  <div class="hero">
    <h1>מרכז תצוגה מקדימה • קמפיין ״ממריבה לקִרבה״</h1>
    <p>וובינר יובל סודאי • יום רביעי, 18.11.2026, 20:30</p>
    <div class="tagline">עודכן ונערך במלואו לפי הלו״ז והנוסחים החדשים של טובי</div>
  </div>

  <div class="container">
    
    <!-- חלק המיילים -->
    <div class="section-header">
      <h2>📧 תצוגת כל המיילים המעוצבים לפולסים (13 מיילים)</h2>
    </div>
    <p class="section-desc">מיילים מעוצבים לפי תקן Pulseem (מותאם מובייל, RTL, גופן Assistant, כפתורים בולטים וחלופות מסוננות).</p>
    
    <div class="grid">
      {email_cards_html}
    </div>

    <!-- חלק הוואטסאפ -->
    <div class="section-header">
      <h2>💬 תצוגת הודעות וואטסאפ (9 הודעות לקבוצה 1070110)</h2>
    </div>
    <p class="section-desc">הודעות וואטסאפ מעוצבות בתצוגת צ'אט אותנטית עם כפתור העתקת נוסח נקי בקליק אחד.</p>
    
    <div class="grid">
      {wa_cards_html}
    </div>

  </div>

  <div class="footer">
    קמפיין וובינר יובל סודאי — זוג או פרט • מערכת תצוגה מקדימה לטובי
  </div>

</body>
</html>
"""

with open(os.path.join(PREVIEW_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)

print("Master preview portal created successfully at preview/index.html!")
