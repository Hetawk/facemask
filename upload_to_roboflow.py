#!/usr/bin/env python3
"""
Script to upload Face Mask Detection dataset to Roboflow
"""
import os
import subprocess
import sys
from pathlib import Path

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    print("Note: python-dotenv not installed. Will try to read .env manually.")

# Load configuration from environment variables


def load_config():
    """Load configuration from .env file or environment variables"""
    # Try to manually read .env if dotenv is not available
    if not DOTENV_AVAILABLE:
        env_path = Path('.env')
        if env_path.exists():
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()

    config = {
        'api_key': os.getenv('ROBOFLOW_API_KEY'),
        'publishable_key': os.getenv('ROBOFLOW_PUBLISHABLE_KEY'),
        'workspace_id': os.getenv('ROBOFLOW_WORKSPACE_ID'),
        'project_id': os.getenv('ROBOFLOW_PROJECT_ID'),
        'dataset_path': os.getenv('DATASET_PATH', './dataset')
    }

    return config


# Load configuration
config = load_config()
WORKSPACE_ID = config['workspace_id']
PROJECT_ID = config['project_id']
DATASET_PATH = config['dataset_path']
API_KEY = config['api_key']

# Dataset info
CLASS_NAMES = ['WithMask', 'WithoutMask']


def check_roboflow_installed():
    """Check if roboflow CLI is installed"""
    try:
        result = subprocess.run(['roboflow', '--version'],
                                capture_output=True, text=True)
        print(f"✓ Roboflow CLI is installed: {result.stdout.strip()}")
        return True
    except FileNotFoundError:
        print("✗ Roboflow CLI is not installed")
        return False


def install_roboflow():
    """Install roboflow package and python-dotenv"""
    print("\nInstalling roboflow and python-dotenv...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'roboflow', 'python-dotenv'],
                       check=True)
        print("✓ Roboflow and python-dotenv installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install packages: {e}")
        return False


def check_authentication():
    """Check if user is authenticated with Roboflow using API key"""
    print("\nChecking Roboflow authentication...")

    if not API_KEY:
        print("✗ No API key found in .env file")
        return False

    try:
        # Set the API key in the environment
        os.environ['ROBOFLOW_API_KEY'] = API_KEY

        # Try to authenticate using Python API
        from roboflow import Roboflow
        rf = Roboflow(api_key=API_KEY)
        workspace = rf.workspace()
        print(f"✓ Authenticated with Roboflow as: {workspace.name}")
        return True
    except ImportError:
        print("✗ Roboflow Python package not found")
        return False
    except Exception as e:
        print(f"✗ Authentication failed: {e}")
        return False


def authenticate_roboflow():
    """Authenticate with Roboflow using API key from .env"""
    print("\nAuthenticating with Roboflow using API key...")

    if not API_KEY:
        print("✗ No API key found in .env file")
        print("Please add ROBOFLOW_API_KEY to your .env file")
        return False

    try:
        # Set environment variable for roboflow CLI
        os.environ['ROBOFLOW_API_KEY'] = API_KEY

        # Test authentication with Python API
        from roboflow import Roboflow
        rf = Roboflow(api_key=API_KEY)
        workspace = rf.workspace()
        print(f"✓ Authentication successful: {workspace.name}")
        return True
    except ImportError:
        print("✗ Roboflow Python package not found")
        print("Please install it: pip install roboflow")
        return False
    except Exception as e:
        print(f"✗ Authentication failed: {e}")
        return False


def create_data_yaml():
    """Create data.yaml file for the dataset"""
    print("\nCreating data.yaml file...")

    dataset_path = Path(DATASET_PATH)
    yaml_content = f"""# Face Mask Detection Dataset
# Single-Label Classification

# Dataset paths
path: {dataset_path.absolute()}
train: train
val: val
test: test

# Classes
nc: {len(CLASS_NAMES)}
names: {CLASS_NAMES}

# Dataset info
dataset_type: classification
"""

    yaml_path = dataset_path / "data.yaml"

    try:
        with open(yaml_path, 'w') as f:
            f.write(yaml_content)
        print(f"✓ Created data.yaml at: {yaml_path}")
        return True
    except Exception as e:
        print(f"✗ Failed to create data.yaml: {e}")
        return False


def verify_dataset_structure():
    """Verify that the dataset has the correct structure"""
    print("\nVerifying dataset structure...")

    dataset_path = Path(DATASET_PATH)
    splits = ['train', 'test', 'val']

    issues = []

    for split in splits:
        split_path = dataset_path / split
        if not split_path.exists():
            issues.append(f"Missing {split} directory")
            continue

        for class_name in CLASS_NAMES:
            class_path = split_path / class_name
            if not class_path.exists():
                issues.append(f"Missing {split}/{class_name} directory")
            else:
                # Count images
                images = list(class_path.glob('*.png')) + \
                    list(class_path.glob('*.jpg')) + \
                    list(class_path.glob('*.jpeg'))
                print(f"  {split}/{class_name}: {len(images)} images")

    if issues:
        print("\n✗ Dataset structure issues found:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✓ Dataset structure is valid")
        return True


def upload_dataset():
    """Upload the dataset to Roboflow using Python API"""
    print("\n" + "="*60)
    print("UPLOADING DATASET TO ROBOFLOW")
    print("="*60)

    dataset_path = Path(DATASET_PATH).absolute()

    try:
        from roboflow import Roboflow

        # Initialize Roboflow with API key
        rf = Roboflow(api_key=API_KEY)
        workspace = rf.workspace(WORKSPACE_ID)
        project = workspace.project(PROJECT_ID)

        print(f"\nProject: {project.name}")
        print(f"Workspace: {workspace.name}")
        print(f"Dataset path: {dataset_path}")
        print("\nUploading images...")
        print("This may take a while depending on your dataset size...")
        print("Please be patient.\n")

        # Upload images for each split
        splits = ['train', 'val', 'test']
        total_uploaded = 0

        for split in splits:
            print(f"\n{'='*50}")
            print(f"Uploading {split} split...")
            print(f"{'='*50}")

            for class_name in CLASS_NAMES:
                class_path = dataset_path / split / class_name
                if not class_path.exists():
                    print(
                        f"  Skipping {split}/{class_name} - directory not found")
                    continue

                # Get all images
                images = list(class_path.glob('*.png')) + \
                    list(class_path.glob('*.jpg')) + \
                    list(class_path.glob('*.jpeg'))

                print(
                    f"\n  Uploading {len(images)} images from {split}/{class_name}...")

                for idx, image_path in enumerate(images, 1):
                    try:
                        # Upload image with tag for the class
                        project.upload(
                            image_path=str(image_path),
                            split=split,
                            tag_names=[class_name]
                        )
                        total_uploaded += 1

                        # Print progress every 10 images
                        if idx % 10 == 0 or idx == len(images):
                            print(
                                f"    Progress: {idx}/{len(images)} images uploaded")

                    except Exception as e:
                        print(f"    ✗ Failed to upload {image_path.name}: {e}")

        print("\n" + "="*60)
        print(f"✓ UPLOAD COMPLETE!")
        print(f"  Total images uploaded: {total_uploaded}")
        print("="*60)
        return True

    except ImportError:
        print("✗ Roboflow Python package not found")
        print("Please install it: pip install roboflow")
        return False
    except Exception as e:
        print("\n" + "="*60)
        print(f"✗ UPLOAD FAILED: {e}")
        print("="*60)
        return False


def main():
    """Main function to orchestrate the upload process"""
    print("="*60)
    print("ROBOFLOW DATASET UPLOAD SCRIPT")
    print("Face Mask Detection Dataset")
    print("="*60)

    # Step 0: Validate configuration
    if not API_KEY:
        print("\n✗ Error: ROBOFLOW_API_KEY not found in .env file")
        print("Please create a .env file with your API key")
        return False

    if not WORKSPACE_ID or not PROJECT_ID:
        print("\n✗ Error: Missing workspace or project ID in .env file")
        return False

    print(f"\n✓ Configuration loaded from .env")
    print(f"  Workspace: {WORKSPACE_ID}")
    print(f"  Project: {PROJECT_ID}")

    # Step 1: Check if roboflow is installed
    try:
        import roboflow
        print(f"✓ Roboflow package is installed")
    except ImportError:
        print("✗ Roboflow package is not installed")
        response = input("\nWould you like to install roboflow now? (y/n): ")
        if response.lower() == 'y':
            if not install_roboflow():
                print(
                    "\nPlease install roboflow manually: pip install roboflow python-dotenv")
                return False
        else:
            print("\nPlease install roboflow: pip install roboflow python-dotenv")
            return False

    # Step 2: Verify dataset structure
    if not verify_dataset_structure():
        print("\nPlease fix the dataset structure before uploading.")
        return False

    # Step 3: Create data.yaml
    if not create_data_yaml():
        return False

    # Step 4: Check authentication
    if not check_authentication():
        print("\n✗ Authentication failed. Please check your API key in .env file")
        return False

    # Step 5: Confirm upload
    print(f"\nReady to upload dataset to:")
    print(f"  Workspace: {WORKSPACE_ID}")
    print(f"  Project: {PROJECT_ID}")
    print(f"  Dataset path: {Path(DATASET_PATH).absolute()}")

    response = input("\nProceed with upload? (y/n): ")
    if response.lower() != 'y':
        print("\nUpload cancelled.")
        return False

    # Step 6: Upload
    return upload_dataset()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
