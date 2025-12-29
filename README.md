# 🚀 Synchora AI

### Real‑Time Object Detection & Scene Narration Platform

---

## 🌟 What is Synchora AI?

**Synchora AI** is a real‑time computer vision backend that combines **YOLOv3 object detection**, **Node.js APIs**, and **Generative AI (Gemini)** to:

* Detect objects in images
* Return structured detection data (JSON)
* Convert detections into **natural spoken scene descriptions**

It is designed for:

* Assistive vision systems
* Smart surveillance & monitoring
* AI‑powered narration tools
* Research & academic projects

---

## 🧠 Core Technologies Used

| Layer            | Technology                   |
| ---------------- | ---------------------------- |
| Object Detection | YOLOv3 (OpenCV DNN)          |
| Backend API      | Node.js + Express            |
| Image Handling   | Multer (in‑memory uploads)   |
| AI Narration     | Google Gemini API            |
| Language Bridge  | child_process (stdin/stdout) |
| Hosting          | Cloudflared / Tunnel         |

---

## 🏗️ System Architecture

```
Client (Web / Mobile)
        │
        ▼
Node.js API (/upload)
        │
        ▼
Python (YOLOv3 detect.py)
        │
        ▼
Detection JSON
        │
        ▼
Gemini AI → Scene Narration
        │
        ▼
Final API Response
```

---

## ⚙️ How It Works (Step‑by‑Step)

### 1️⃣ Image Upload

* Client sends an image to `/upload`
* Multer stores image **in memory** (fast, no disk I/O)

### 2️⃣ Python Detection Process

* Node.js spawns `detect.py`
* Image buffer is sent via **stdin**
* YOLOv3 processes the image
* Returns detection JSON via **stdout**

### 3️⃣ Detection Output Format

```json
{
  "success": true,
  "detections": [
    {
      "class": "person",
      "confidence": 0.82,
      "bbox": { "x": 120, "y": 60, "width": 180, "height": 300 }
    }
  ],
  "count": 1
}
```

⚠️ Output layout is **fixed and stable** to avoid Node‑side changes.

### 4️⃣ Scene Narration (Gemini)

* Detection JSON is converted into a **spoken‑style description**
* Example:

> "It looks like a street scene. A person is standing in the middle. Be careful of traffic nearby."

---

## 📁 Project Structure

```
SYNCHORA-SERVER/
│
├── detect.py            # YOLOv3 detection engine
├── index.js             # Node.js API server
├── yolov3.cfg
├── yolov3.weights
├── coco.names
├── requirements.txt
├── package.json
├── .env
└── README.md
```

---

## 🧪 Setup Guide (Local Machine)

### ✅ Prerequisites

* Node.js ≥ 18
* Python ≥ 3.8
* OpenCV
* Google Gemini API Key

---

### 🔹 Python Setup

```bash
pip install -r requirements.txt
```

**requirements.txt**

```
opencv-python
numpy
pillow
```

---

### 🔹 Node.js Setup

```bash
npm install
```

Create `.env` file:

```
GEMINI_KEY=your_api_key_here
PORT=3000
```

---

### ▶️ Run Locally

```bash
node index.js
```

API available at:

```
http://localhost:3000/upload
```

---

## ☁️ Hosting with Cloudflared (NO VPS Needed)

Cloudflared lets you expose your **local server securely** without port forwarding.

---

### 🔐 Step 1: Install Cloudflared

#### Windows

* Download Cloudflared
* Add to PATH

Verify:

```bash
cloudflared --version
```

---

### 🚇 Step 2: Create a Tunnel

```bash
cloudflared tunnel login
```

Then:

```bash
cloudflared tunnel create synchora-ai
```

---

### 🌍 Step 3: Run Tunnel (Quick Method)

```bash
cloudflared tunnel --url http://localhost:3000
```

You’ll get a **public HTTPS URL** like:

```
https://synchora-ai.trycloudflare.com
```

🎉 Your YOLOv3 API is now live!

---

### 🔁 Persistent Tunnel (Recommended)

Create config file:

```yaml
tunnel: synchora-ai
credentials-file: C:\Users\<you>\.cloudflared\synchora-ai.json

ingress:
  - hostname: ai.yourdomain.com
    service: http://localhost:3000
  - service: http_status:404
```

Run:

```bash
cloudflared tunnel run synchora-ai
```

---

## 🔒 Security & Performance Highlights

* ⏱️ Python process timeout (30s)
* 🧠 Memory‑only image handling
* 🛑 MIME type validation
* 🧯 Graceful process termination
* 📊 Server health logging

---

## 🎯 Why This Architecture Works

✅ Language‑agnostic
✅ Model‑independent
✅ Easy to scale
✅ Deployment‑friendly
✅ Works on CPU

---

## 🚀 Future Enhancements

* GPU acceleration (CUDA)
* Video stream inference
* Docker + Kubernetes
* User authentication
* Rate limiting

---

## 🧑‍💻 Author

**Sonu Chowdhury**
Built with vision, precision, and scalability in mind.

---

✨ *Synchora AI — Where Vision Meets Intelligence*
