#!/usr/bin/env python3
"""
Quick test script to verify .env configuration and Roboflow connection
"""
import os
from pathlib import Path


def test_env_file():
    """Test if .env file exists and is readable"""
    print("="*60)
    print("TESTING ENVIRONMENT CONFIGURATION")
    print("="*60)

    env_path = Path('.env')
    if not env_path.exists():
        print("\n✗ .env file not found!")
        return False

    print("\n✓ .env file found")

    # Try to load manually
    config = {}
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()

    required_keys = [
        'ROBOFLOW_API_KEY',
        'ROBOFLOW_WORKSPACE_ID',
        'ROBOFLOW_PROJECT_ID',
        'DATASET_PATH'
    ]

    print("\nConfiguration:")
    all_present = True
    for key in required_keys:
        value = config.get(key, '')
        if value:
            # Mask API key for security
            if 'API_KEY' in key:
                display_value = value[:8] + '...' if len(value) > 8 else '***'
            else:
                display_value = value
            print(f"  ✓ {key}: {display_value}")
        else:
            print(f"  ✗ {key}: NOT SET")
            all_present = False

    return all_present


def test_packages():
    """Test if required packages are installed"""
    print("\n" + "="*60)
    print("TESTING PACKAGE INSTALLATION")
    print("="*60 + "\n")

    packages = {
        'roboflow': 'Roboflow SDK',
        'dotenv': 'python-dotenv'
    }

    all_installed = True
    for module_name, package_name in packages.items():
        try:
            __import__(module_name)
            print(f"✓ {package_name} is installed")
        except ImportError:
            print(f"✗ {package_name} is NOT installed")
            all_installed = False

    return all_installed


def test_connection():
    """Test connection to Roboflow"""
    print("\n" + "="*60)
    print("TESTING ROBOFLOW CONNECTION")
    print("="*60 + "\n")

    try:
        from dotenv import load_dotenv
        load_dotenv()

        api_key = os.getenv('ROBOFLOW_API_KEY')
        if not api_key:
            print("✗ API key not found in environment")
            return False

        from roboflow import Roboflow
        rf = Roboflow(api_key=api_key)
        workspace = rf.workspace()

        print(f"✓ Successfully connected to Roboflow")
        print(f"  Workspace: {workspace.name}")

        # Try to access the project
        workspace_id = os.getenv('ROBOFLOW_WORKSPACE_ID')
        project_id = os.getenv('ROBOFLOW_PROJECT_ID')

        if workspace_id and project_id:
            try:
                project = rf.workspace(workspace_id).project(project_id)
                print(f"  Project: {project.name}")
                print(f"  Project Type: {project.type}")
                return True
            except Exception as e:
                print(f"  ⚠ Could not access project: {e}")
                return True  # Connection works, just can't access specific project

        return True

    except ImportError as e:
        print(f"✗ Missing package: {e}")
        return False
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False


def test_dataset_structure():
    """Test if dataset structure is valid"""
    print("\n" + "="*60)
    print("TESTING DATASET STRUCTURE")
    print("="*60 + "\n")

    from dotenv import load_dotenv
    load_dotenv()

    dataset_path = Path(os.getenv('DATASET_PATH', './dataset'))

    if not dataset_path.exists():
        print(f"✗ Dataset path not found: {dataset_path}")
        return False

    print(f"✓ Dataset path exists: {dataset_path.absolute()}\n")

    splits = ['train', 'val', 'test']
    classes = ['WithMask', 'WithoutMask']

    total_images = 0
    for split in splits:
        split_path = dataset_path / split
        if not split_path.exists():
            print(f"  ✗ Missing {split}/ directory")
            continue

        print(f"  {split}/")
        for class_name in classes:
            class_path = split_path / class_name
            if not class_path.exists():
                print(f"    ✗ Missing {class_name}/ directory")
                continue

            images = list(class_path.glob('*.png')) + \
                list(class_path.glob('*.jpg')) + \
                list(class_path.glob('*.jpeg'))

            count = len(images)
            total_images += count
            print(f"    ✓ {class_name}/: {count} images")

    print(f"\n✓ Total images found: {total_images}")
    return total_images > 0


def main():
    """Run all tests"""
    print("\n" + "╔" + "="*58 + "╗")
    print("║" + " "*15 + "ROBOFLOW SETUP TEST" + " "*24 + "║")
    print("╚" + "="*58 + "╝\n")

    results = {
        'Environment Configuration': test_env_file(),
        'Package Installation': test_packages(),
        'Dataset Structure': test_dataset_structure(),
        'Roboflow Connection': test_connection()
    }

    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}: {test_name}")

    all_passed = all(results.values())

    print("\n" + "="*60)
    if all_passed:
        print("✓ ALL TESTS PASSED!")
        print("You're ready to upload your dataset!")
        print("\nRun: python upload_to_roboflow.py")
    else:
        print("✗ SOME TESTS FAILED")
        print("Please fix the issues above before uploading.")

        if not results['Package Installation']:
            print("\nTo fix: pip install -r requirements.txt")
    print("="*60 + "\n")

    return all_passed


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
