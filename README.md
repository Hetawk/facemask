# Face Mask Detection Dataset - Roboflow Upload

This project contains scripts to upload your Face Mask Detection dataset to Roboflow.

## 📁 Dataset Structure

```
dataset/
├── train/
│   ├── WithMask/
│   └── WithoutMask/
├── val/
│   ├── WithMask/
│   └── WithoutMask/
└── test/
    ├── WithMask/
    └── WithoutMask/
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install roboflow python-dotenv
```

### 2. Configure Environment Variables

The `.env` file is already set up with your credentials:

```env
ROBOFLOW_API_KEY=ZiTfwXqKSN7clsBdZl73
ROBOFLOW_WORKSPACE_ID=project0-ju8av
ROBOFLOW_PROJECT_ID=mask-detection-h1gxk
DATASET_PATH=./dataset
```

⚠️ **Important**: Never commit the `.env` file to version control! (It's already in `.gitignore`)

### 3. Run the Upload Script

```bash
python upload_to_roboflow.py
```

Or:

```bash
./upload_to_roboflow.py
```

## 🔧 What the Script Does

1. ✅ Loads configuration from `.env` file
2. ✅ Validates Roboflow package installation
3. ✅ Verifies dataset structure and counts images
4. ✅ Creates `data.yaml` file for Roboflow
5. ✅ Authenticates using your API key
6. ✅ Uploads all images with proper split tags (train/val/test)
7. ✅ Shows upload progress and summary

## 📊 Features

- **Automatic Authentication**: Uses API key from `.env` (no browser login needed)
- **Progress Tracking**: Shows upload progress for each split
- **Error Handling**: Continues even if individual images fail
- **Class Tagging**: Automatically tags images with their class labels
- **Split Management**: Properly organizes images into train/val/test splits

## 🔑 API Keys

Your `.env` file contains two types of API keys:

- **Private API Key**: `ZiTfwXqKSN7clsBdZl73` (used for uploads and platform APIs)
- **Publishable API Key**: `rf_aqlZnGhlSTODrFULwBeyUg0pllF3` (for client-side inference)

The upload script uses the **Private API Key** for authentication.

## 📝 Files Created

- `.env` - Environment variables (API keys and configuration)
- `.gitignore` - Prevents sensitive files from being committed
- `requirements.txt` - Python dependencies
- `dataset/data.yaml` - Dataset metadata (created during upload)

## 🔒 Security

- The `.env` file contains sensitive API keys
- It's already added to `.gitignore` to prevent accidental commits
- Never share your API keys publicly

## 🆘 Troubleshooting

### Module not found error

```bash
pip install roboflow python-dotenv
```

### Authentication failed

- Check that your API key in `.env` is correct
- Verify you have access to the workspace and project

### Upload fails

- Ensure your internet connection is stable
- Check that image files are valid (PNG, JPG, JPEG)
- Verify dataset structure matches the expected format

## 📚 Resources

- [Roboflow Documentation](https://docs.roboflow.com/)
- [Roboflow Python Package](https://pypi.org/project/roboflow/)
- [Your Roboflow Dashboard](https://app.roboflow.com/)
