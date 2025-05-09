# 🚀 LiveCryptoQuotes

**LiveCryptoQuotes** is a real-time cryptocurrency quote tracker built with Django, Django Channels, and Celery. It fetches live crypto data, processes it asynchronously, and streams it to the frontend using WebSockets for a seamless, dynamic user experience.



## 📌 Features

- 🔄 **Real-Time Quotes** – Live updates using WebSockets.
- ⚡ **Asynchronous Tasks** – Background fetching with Celery and Redis.
- 🔒 **Secure API Integration** – External crypto data pulled securely.
- 📊 **Interactive UI** – Dynamic frontend showing price, change, volume, etc.
- 🧪 **Test Coverage** – Core logic covered with unit and integration tests.

---

## 📂 Project Structure

```

LiveCryptoQuotes/
├── core/                 # Django app handling API and data processing
├── templates/            # HTML templates
├── static/               # Static files (CSS, JS)
├── quotes/               # App for real-time quote management
├── consumers.py          # Django Channels WebSocket consumers
├── celery.py             # Celery config
├── asgi.py               # ASGI entrypoint
├── requirements.txt
├── README.md
└── ...

````

---

## 🛠️ Tech Stack

- **Backend**: Django, Django Channels
- **Async Tasks**: Celery, Redis
- **Frontend**: HTML, CSS, JavaScript
- **WebSockets**: ASGI, Channels
- **Database**: PostgreSQL (can use MySQL or SQLite)
- **API Source**: finnhub / Binance /

---

## ⚙️ Installation

```bash
# Clone the repo
git clone https://github.com/AbrarZaved/LiveCryptoQuotes.git
cd LiveCryptoQuotes

# Create virtual env
python -m venv env
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Migrate DB
python manage.py migrate

# Run Celery
celery -A LiveCryptoQuotes worker --loglevel=info

# Run Django Server
python manage.py runserver
````

---

## 🚀 Running WebSocket Server

Ensure your `asgi.py` is set up for Channels. Then run:

```bash
daphne LiveCryptoQuotes.asgi:application
```

Or, for development:

```bash
python manage.py runserver
```

---

## 🧪 Running Tests

```bash
python manage.py test
```

---

## 📸 Screenshots

Here are some previews of the LiveCryptoQuotes UI:

![LiveCryptoQuotes Screenshot 1](https://images2.imgbox.com/54/48/Mid8IFZv_o.png)
![LiveCryptoQuotes Screenshot 2](https://images2.imgbox.com/59/c6/dG1Rw2XW_o.png)

---

## 📈 Future Enhancements

* 🔔 User-defined price alerts
* 📱 PWA / Mobile App integration
* 📊 Charting with D3.js or Chart.js
* 🧩 Plugin support for custom exchanges
* 👥 User auth and portfolio tracking

---

## 🤝 Contributing

Contributions, issues and feature requests are welcome!

```bash
# Fork it
# Create your feature branch
git checkout -b feature/awesome-feature

# Commit your changes
git commit -m 'Add some feature'

# Push to the branch
git push origin feature/awesome-feature

# Open a pull request
```

---

## 📝 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Abrar Zaved** – [@abrarzaved](https://github.com/AbrarZaved)
💡 Backend Developer | Django | 

---


