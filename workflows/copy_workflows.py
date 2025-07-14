#!/usr/bin/env python3
import json
import shutil
import os
import re

# List of all JSON files that appear to be n8n workflows
json_workflow_files = [
    # Root directory files
    "/projects/trap/Documents/gdrive-copy/12_2___N8n_Lead_Generation (2) - 1xj_wZlMOxHM8tLf_KtIjURxzrTyRBK5P.json",
    "/projects/trap/Documents/gdrive-copy/12_5_Youtube_Faceless_Video_Research - 1cv4PoFv6sFpD_ME8C-UvfN795TWW89dZ.json",
    "/projects/trap/Documents/gdrive-copy/12_6___Finance___Legal_Manager_Agent - 15ah0zYDi8b5ChQ3UYe-DUzf9KVA_fTLb.json",
    "/projects/trap/Documents/gdrive-copy/14_4_Faceless_Video_Generator_Comparison__Minimax_vs_Hunyuan_vs_Kling_ - 1bKZkTSYPfNBU-HVbUycBfimJ6SP7zb16.json",
    "/projects/trap/Documents/gdrive-copy/Common___Send_Threads_Workflow - 1wV1DbMe9s9o7f0nwWuFijbyZJRW4tlHw.json",
    "/projects/trap/Documents/gdrive-copy/Template_1.2___I_Built_an_AI_Agent_to_Automate_SEO_Research___Content_Creation__100__Automated_ - 1oTRIMTdbET-WBSr1skXnUzPwFSsE13LS.json",
    "/projects/trap/Documents/gdrive-copy/Template_12___Build_a_Multichannel_RAG_based_AI_Chatbot_with_Custom_Knowledge_Base_in_20_mins - 1w1jlv0kbw_UNTwNyPELRywS8c67SP8e-.json",
    "/projects/trap/Documents/gdrive-copy/Template_16___These_5_AI_Agent_Workflows_Will_Change_How_You_Automate_EVERYTHING__No_Code__ - 1svYaETPCSw8afB6TeerWAeAN_zJoxxx_.json",
    "/projects/trap/Documents/gdrive-copy/Template_18___Reddit_Newsletter - 1qKgR5D7OblrrOCqcQA9vNF4C__QR8ya4.json",
    "/projects/trap/Documents/gdrive-copy/Template_5.2___How_I_Built_an_AI_Agent_to_Research_YouTube_Video_Ideas__No_Code_ - 1jVeSLDR7_OsY_b_r5GHDGG1LVGFU08yf.json",
    "/projects/trap/Documents/gdrive-copy/Template_7.3___How_I_Built_an_AI_Agent_with_DeepSeek_AI_to_Turn_YouTube_Video_into_Blog_via_Telegram__No_Code_ - 1vtAw-0YxKYlbCLvS7gVO273wurI0ouAe.json",
    "/projects/trap/Documents/gdrive-copy/Template_9.3___Your_Automated_Job_Search___Application_AI_Agent__No_code_with_n8n__LinkedIn__Deepseek___Perplexity_ - 1axjclXhYvcHMcDm8PovabxzFIFt_VQZ8.json",
    "/projects/trap/Documents/gdrive-copy/Template_9___How_I_Built_a_Blog_with_v0_and_an_AI_Agent_to_Repurpose_News_into_Blogs__No_Code_ - 1Q1jhjfRNDp7STu6Fe17rsa3V-HUZfrty.json",
    "/projects/trap/Documents/gdrive-copy/Tutorial_11_3___Hailuoai_Faceless_Video - 1O_Jzv_sg5LUMf0OiArxU_nYhH6awkxfm.json",
    "/projects/trap/Documents/gdrive-copy/Tutorial_14_4___Pinterest_Automation__Get_Free_Traffic_with_n8n__No_Ads_Needed_ - 1HUtR6S6sBPJ5jf4tOiHVtmULSQB1p4m6.json",
    "/projects/trap/Documents/gdrive-copy/Tutorial_15_1___Faceless_AI_Workflow__Cat_Video_Fully_Automated_Template__n8n_No_code_Template_ - 1YQpPPGCEDWKMN82MCoxpwliWkEkYodep.json",
    "/projects/trap/Documents/gdrive-copy/Tutorial_17_2___Faceless_AI_Workflow__Retro_Future_Jazz_Music_Videos__For__5k_mo_Fully_Automated__n8n_No_code_Template_ 2 - 1qZ64JSa6Pl6tOjKFWD9VQkczxcqb67gL.json",
    "/projects/trap/Documents/gdrive-copy/Tutorial_1_4___I_Built_an_AI_Agent_to_Auto_Repurpose_News_into_Engaging_Threads__100__Automated_ - 1BRQOWR5TgnNhfZ7rn6BJn3AKwQ4WR5zF.json",
    "/projects/trap/Documents/gdrive-copy/Tutorial_2___How_I_Built_an_AI_Agent_to_Repurpose_Podcasts_into_Engaging_Threads__100__Automated_ - 1z_3_GxafrMM2f4J5oENxT9Uq-l2Pdbrx.json",
    "/projects/trap/Documents/gdrive-copy/Tutorial_3_1___How_I_Built_an_AI_Agent_to_Automate_Instagram_Reels_in_Threads__X_Twitter_Post_Style__No_Code_ - 1D9dMpcnCq4j1i_Py1UTplRT7TotSNsGL.json",
    "/projects/trap/Documents/gdrive-copy/Tutorial_3_2___How_I_Built_an_AI_Agent_to_Repurpose_YouTube_Videos_into_Twitter_Threads__100__No_Code__ - 1jjL2n6NkFJ0iQw4-zFrwB6YOYMOIRiZJ.json",
    "/projects/trap/Documents/gdrive-copy/Tutorial_3_3___I_Built_an_AI_Agent_for_Content_Research___Auto_Posting__on_LinkedIn__X_Twitter___Threads__No_Code_ - 1hSiARtwva_LDsLCLF5NQ9rdc8WfmItYR.json",
    "/projects/trap/Documents/gdrive-copy/Tutorial_6_1___How_I_Built_an_AI_Agent_with_DeepSeek_AI_to_Create_Faceless_YouTube_Videos__No_Code_ - 1Bgqz1B23ppVSXV-KMBYnhjdLRPHq5qlZ.json",
    "/projects/trap/Documents/gdrive-copy/Tutorial_7_2___How_I_Built_an_AI_Agent_to_Turn_YouTube_Videos_into_My_Own_AI_Avatar_Videos__No_Code_ - 1yTJyTkDAjW5NLQr7rd6nFH2VdnxC82Ou.json",
    "/projects/trap/Documents/gdrive-copy/Tutorial_8_3___An_AI_Agent_to_generate_UNLIMITED_Instagram_Image_Posts - 15SKZVlvghkI3T-l-6n0qdAAZDLqDMgKY.json",
    "/projects/trap/Documents/gdrive-copy/workflow - 1LmlxMQHf8o9j4nSRKgzn5hJgWYjcXNq4.json",
    
    # Subdirectory files
    "/projects/trap/Documents/gdrive-copy/18 - 1kgclMLvdHB1i3x3Ko16Wkmr_ngBgTQZ2.2 Teaching Materials/18_2___Instagram&Threads_Upload.json",
    "/projects/trap/Documents/gdrive-copy/Multi-Stage Agentic RAG - 1kX8c0c8HF9bs9Dw_8Jbr51fx1OYhAsHF/Llama 3.2 Agentic RAG Agents.json",
    "/projects/trap/Documents/gdrive-copy/Tutorial 13 - 1OVlD1v4ZjRmOZrFh0xKGcG1ITpR9Es8Q.2 - json/Tutorial_13_2___Generate_an_image_with_Flux_and_send_it_via_Telegram.json",
    "/projects/trap/Documents/gdrive-copy/Tutorial 13 - 1OVlD1v4ZjRmOZrFh0xKGcG1ITpR9Es8Q.2 - json/Tutorial_13_2___Scheduling_Agent.json",
    "/projects/trap/Documents/gdrive-copy/Tutorial 13 - 1OVlD1v4ZjRmOZrFh0xKGcG1ITpR9Es8Q.2 - json/Tutorial_13_2___Social_Media_AI_Agent.json",
    "/projects/trap/Documents/gdrive-copy/Tutorial 14 - 1gSc9lFEnii6Fj7kjkV3jfpJ6crLlS9zz.1 - Tutorial materials/Tutorial_14_1___Auto_Clip_Video__Local_Host__Public (1).json",
    "/projects/trap/Documents/gdrive-copy/Tutorial 16 - 1mgDP_-aw_TgBTuiKOMBmDoXe39hXDEik.1 - Shared files/Tutorial_16_2-template.json",
    "/projects/trap/Documents/gdrive-copy/common - 1U0nKPzaJpSTth8FkdS_BxziopeBU7xgE/Common___Send_Linkedin.json",
    "/projects/trap/Documents/gdrive-copy/common - 1U0nKPzaJpSTth8FkdS_BxziopeBU7xgE/Common___Send_Threads_Workflow.json",
    "/projects/trap/Documents/gdrive-copy/common - 1U0nKPzaJpSTth8FkdS_BxziopeBU7xgE/Common___Send_X_Twitter_Workflow.json",
]

dest_dir = "/home/trap/projects/my-n8n-render/workflows"

def sanitize_filename(filename):
    """Sanitize filename to be filesystem-safe"""
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    filename = re.sub(r'[^\w\s.-]', '_', filename)
    filename = re.sub(r'[-\s]+', '_', filename)
    filename = filename.strip('_')
    # Ensure it's not too long
    if len(filename) > 200:
        name, ext = os.path.splitext(filename)
        filename = name[:200-len(ext)] + ext
    return filename

def is_valid_n8n_workflow(file_path):
    """Check if a JSON file is a valid n8n workflow"""
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
    except (json.JSONDecodeError, Exception) as e:
        print(f"Error reading {file_path}: {e}")
        return False

def copy_workflow_files():
    """Copy all valid n8n workflow files to the destination directory"""
    copied_files = []
    skipped_files = []
    conflict_files = []
    
    for file_path in json_workflow_files:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            skipped_files.append(file_path)
            continue
            
        if not is_valid_n8n_workflow(file_path):
            print(f"Not a valid n8n workflow: {file_path}")
            skipped_files.append(file_path)
            continue
            
        # Extract filename
        filename = os.path.basename(file_path)
        sanitized_filename = sanitize_filename(filename)
        
        # Handle potential conflicts
        dest_file = os.path.join(dest_dir, sanitized_filename)
        if os.path.exists(dest_file):
            base_name = os.path.splitext(sanitized_filename)[0]
            extension = os.path.splitext(sanitized_filename)[1]
            counter = 1
            while os.path.exists(dest_file):
                new_name = f"{base_name}_{counter}{extension}"
                dest_file = os.path.join(dest_dir, new_name)
                counter += 1
            conflict_files.append((file_path, dest_file))
        
        try:
            shutil.copy2(file_path, dest_file)
            copied_files.append((file_path, dest_file))
            print(f"✓ Copied: {filename} -> {os.path.basename(dest_file)}")
        except Exception as e:
            print(f"✗ Failed to copy {filename}: {e}")
            skipped_files.append(file_path)
    
    return copied_files, skipped_files, conflict_files

if __name__ == "__main__":
    print("Starting n8n workflow transfer...")
    
    # Create destination directory if it doesn't exist
    os.makedirs(dest_dir, exist_ok=True)
    
    copied_files, skipped_files, conflict_files = copy_workflow_files()
    
    print(f"\n=== TRANSFER COMPLETE ===")
    print(f"Total files processed: {len(json_workflow_files)}")
    print(f"Files successfully copied: {len(copied_files)}")
    print(f"Files skipped: {len(skipped_files)}")
    print(f"Filename conflicts resolved: {len(conflict_files)}")
    
    if conflict_files:
        print(f"\nRenamed due to conflicts:")
        for src, dst in conflict_files:
            print(f"  {os.path.basename(src)} -> {os.path.basename(dst)}")
    
    print(f"\nAll copied files:")
    for src, dst in copied_files:
        print(f"  {os.path.basename(dst)}")