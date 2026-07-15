from flask import Flask, request, render_template, send_from_directory
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "yusifazimov2010@gmail.com"
SENDER_PASSWORD = "edjufnxvixslpihg" 
RECEIVER_EMAIL = "mamedazimov1983@gmail.com"

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Получаем данные из формы
    name = request.form.get('name')
    area = request.form.get('area')
    area_other = request.form.get('area_other')
    risks = request.form.getlist('risks')
    risks_other = request.form.get('risks_other')
    phone = request.form.get('phone')
    email = request.form.get('email')
    employees = request.form.get('employees')
    insurance = request.form.get('insurance')
    

    # Логика обработки "Другое"
    final_area = area_other if area == 'other' else area
    
    selected_risks = [r if r != 'other' else risks_other for r in risks]
    risks_str = ", ".join(selected_risks)

    # Формируем письмо
    msg = EmailMessage()
    msg.set_content(f"""
    Новая заявка с сайта:
    --------------------
    Имя предприятия: {name}
    Сфера деятельности: {final_area}
    Выбранные риски: {risks_str}
    Количество сотрудников: {employees}
    Наличие страховки: {insurance}
    Телефон: {phone}
    Email: {email}
    """)
    
    msg['Subject'] = "Новая заявка: " + name
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    # Отправка
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        return "<h1>Форма успешно отправлена!</h1><a href='/'>Вернуться назад</a>"
    except Exception as e:
        return f"Ошибка при отправке: {e}"

@app.route('/<path:filename>')
def serve_image(filename):
    # Это позволит Flask отдавать файлы (картинки, css и т.д.) из корневой папки
    return send_from_directory('.', filename)
if __name__ == '__main__':
    app.run(debug=True)