import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
client = Groq(api_key=GROQ_API_KEY)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    mavzu = data.get('mavzu', '').strip()
    sinf = data.get('sinf', '').strip()
    fan = data.get('fan', '').strip()
    
    if not mavzu:
        return jsonify({'natija': 'Mavzuni kiriting!'})
    
    prompt = f"""Sen tajribali o'qituvchisan. "{mavzu}" mavzusi uchun {sinf} {fan} darsi rejasini yoz.

Quyidagilar bo'lishi kerak:
1. Dars maqsadi
2. Dars bosqichlari:
   - Tashkiliy qism (5 daqiqa)
   - Takrorlash (5 daqiqa)
   - Yangi mavzu (20 daqiqa)
   - Mustahkamlash (10 daqiqa)
   - Uyga vazifa (5 daqiqa)
3. Har bir bosqich uchun aniq savollar
4. Baholash usuli
5. Uyga vazifa

O'zbek tilida, aniq va tushunarli yoz. Sarlavhalar bilan."""
    
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": "Sen tajribali o'qituvchisan. Faqat o'zbek tilida javob ber."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2500
        )
        natija = response.choices[0].message.content
        return jsonify({'natija': natija})
    except Exception as e:
        return jsonify({'natija': f'Xatolik: {str(e)}'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)