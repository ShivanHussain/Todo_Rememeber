# ToDo Remember - Flask + MongoDB App

A simple **ToDo application** built with **Flask** and **MongoDB**, with a clean UI, emoji support, and task management features. Fully ready for local development and cloud deployment (Render).

---

## **Features**

* Add, update, delete tasks
* Track task status: `Start → Pending → Complete`
* Update task description inline
* Spinner for UI feedback
* Emoji support in task titles and UI
* Responsive and clean design
* Backend APIs for integration
* MongoDB Atlas integration

---

## **Folder Structure**

```
todo/
│
├─ app.py                 # Flask app entry point
├─ database.py            # MongoDB connection setup
├─ models/
│   └─ task_model.py      # CRUD operations for tasks
├─ templates/
│   └─ index.html         # HTML template
├─ static/
│   ├─ style.css          # CSS styles
│   └─ favicon.png        # Browser tab icon (optional)
├─ requirements.txt       # Python dependencies
├─ Procfile               # For Render deployment
├─ .env                   # Environment variables (MONGO_URI)
└─ .gitignore             # Files to ignore in Git
```

---

## **Setup & Local Development**

### 1️⃣ Clone the repository

```bash
git clone https://github.com/ShivanHussain/todo-flask-app.git
cd todo-flask-app
```

### 2️⃣ Create a virtual environment (optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set up environment variables

Create a `.env` file in project root:

```
MONGO_URI=your_mongodb_connection_string
```

> Example for MongoDB Atlas:
> `mongodb+srv://username:password@cluster.mongodb.net/task?retryWrites=true&w=majority`

### 5️⃣ Run locally

```bash
python3 app.py
```

Open browser: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## **APIs**

* `GET /tasks` → List all tasks
* `POST /tasks` → Add new task (`JSON: {title, description, status}`)
* `GET /tasks/<task_id>` → Get task by ID
* `PUT /tasks/<task_id>` → Update task (`JSON: {title/description/status}`)
* `DELETE /tasks/<task_id>` → Delete task

---

## **Deployment on Render**

1. Push project to GitHub
2. Go to [Render](https://render.com/) → New **Web Service**
3. Connect GitHub repo
4. Set **Build Command**: `pip install -r requirements.txt`
5. Set **Start Command**: `gunicorn app:app`
6. Set environment variable:

```
MONGO_URI=your_mongodb_connection_string
```

7. Deploy → your app will be live at a public URL.

---

## **Technologies Used**

* Python 3.10+
* Flask
* MongoDB Atlas
* Jinja2 Templates
* HTML, CSS
* JavaScript (for spinner)
* Gunicorn (production server)
* Render (cloud hosting)

---

## **License**

This project is licensed under MIT License.
