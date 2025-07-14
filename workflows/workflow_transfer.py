#!/usr/bin/env python3
import os
import json
import shutil
from pathlib import Path
import re

# Source and destination directories
source_dir = "/projects/trap/Documents/gdrive-copy"
dest_dir = "/projects/trap/projects/my-n8n-render/workflows"

# List to store all JSON files found
json_files = []
workflow_files = []
skipped_files = []
conflict_files = []

# Walk through the source directory to find all JSON files
for root, dirs, files in os.walk(source_dir):
    for file in files:
        if file.endswith('.json'):
            json_files.append(os.path.join(root, file))

print(f"Found {len(json_files)} JSON files:")

# Function to validate if a JSON file is an n8n workflow
def is_n8n_workflow(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Check for n8n workflow structure
        if isinstance(data, dict) and 'nodes' in data:
            # Additional checks for n8n specific fields
            if 'connections' in data or 'active' in data or 'settings' in data:
                return True
            # Check if nodes have n8n-specific structure
            if data['nodes'] and isinstance(data['nodes'], list):
                for node in data['nodes']:
                    if isinstance(node, dict) and 'type' in node and 'id' in node:
                        return True
        return False
    except (json.JSONDecodeError, Exception):
        return False

# Function to sanitize filename for filesystem
def sanitize_filename(filename):
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    filename = re.sub(r'[^\w\s-]', '_', filename)
    filename = re.sub(r'[-\s]+', '_', filename)
    return filename.strip('_')

# Validate and process each JSON file
for file_path in json_files:
    print(f"\nProcessing: {file_path}")
    
    if is_n8n_workflow(file_path):
        # Extract filename from path
        filename = os.path.basename(file_path)
        
        # Create sanitized filename
        sanitized_name = sanitize_filename(filename)
        
        # Check if file already exists in destination
        dest_file = os.path.join(dest_dir, sanitized_name)
        if os.path.exists(dest_file):
            # Create a unique name by adding a counter
            base_name = os.path.splitext(sanitized_name)[0]
            extension = os.path.splitext(sanitized_name)[1]
            counter = 1
            while os.path.exists(dest_file):
                new_name = f"{base_name}_{counter}{extension}"
                dest_file = os.path.join(dest_dir, new_name)
                counter += 1
            conflict_files.append((file_path, dest_file))
        
        workflow_files.append((file_path, dest_file))
        print(f"  ✓ Valid n8n workflow: {filename}")
    else:
        skipped_files.append(file_path)
        print(f"  ✗ Not a valid n8n workflow: {os.path.basename(file_path)}")

print(f"\n=== SUMMARY ===")
print(f"Total JSON files found: {len(json_files)}")
print(f"Valid n8n workflows: {len(workflow_files)}")
print(f"Skipped files: {len(skipped_files)}")
print(f"Filename conflicts resolved: {len(conflict_files)}")

print(f"\nValid n8n workflows to copy:")
for src, dst in workflow_files:
    print(f"  {os.path.basename(src)} -> {os.path.basename(dst)}")

print(f"\nFiles that will be skipped:")
for file in skipped_files:
    print(f"  {os.path.basename(file)}")

if conflict_files:
    print(f"\nFilename conflicts resolved:")
    for src, dst in conflict_files:
        print(f"  {os.path.basename(src)} -> {os.path.basename(dst)}")

# Now copy the files
print(f"\n=== COPYING FILES ===")
copied_files = []
for src, dst in workflow_files:
    try:
        shutil.copy2(src, dst)
        copied_files.append(dst)
        print(f"  ✓ Copied: {os.path.basename(src)} -> {os.path.basename(dst)}")
    except Exception as e:
        print(f"  ✗ Failed to copy {os.path.basename(src)}: {e}")

print(f"\n=== FINAL SUMMARY ===")
print(f"Total files processed: {len(json_files)}")
print(f"Valid n8n workflows found: {len(workflow_files)}")
print(f"Files successfully copied: {len(copied_files)}")
print(f"Files skipped (not n8n workflows): {len(skipped_files)}")