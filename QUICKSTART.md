# Quick Reference Guide

## 🚀 Setup & Upload (3 Steps)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Test Configuration (Optional but Recommended)

```bash
python test_setup.py
```

### Step 3: Upload Dataset

```bash
python upload_to_roboflow.py
```

---

## 📋 Files Overview

| File                    | Purpose                                           |
| ----------------------- | ------------------------------------------------- |
| `.env`                  | Your API keys and configuration (🔒 Keep secret!) |
| `upload_to_roboflow.py` | Main upload script                                |
| `test_setup.py`         | Test your configuration before upload             |
| `requirements.txt`      | Python dependencies                               |
| `.gitignore`            | Prevents committing sensitive files               |
| `README.md`             | Full documentation                                |

---

## 🔑 Your Configuration (.env)

```env
ROBOFLOW_API_KEY=ZiTfwXqKSN7clsBdZl73
ROBOFLOW_WORKSPACE_ID=project0-ju8av
ROBOFLOW_PROJECT_ID=mask-detection-h1gxk
DATASET_PATH=./dataset
```

---

## 📊 Dataset Info

- **Classes**: WithMask, WithoutMask
- **Splits**: train, val, test
- **Format**: Classification (Single-Label)

---

## 🆘 Quick Troubleshooting

**Import errors?**

```bash
pip install roboflow python-dotenv
```

**Authentication failed?**

- Check API key in `.env` is correct
- Ensure no extra spaces in `.env` file

**Upload slow?**

- Normal for large datasets
- Check internet connection
- Script shows progress every 10 images

---

## 📞 Need Help?

- [Roboflow Docs](https://docs.roboflow.com/)
- [Your Dashboard](https://app.roboflow.com/)
- Check `README.md` for detailed info
