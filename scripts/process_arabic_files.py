import os
import json
import shutil

def process_arabic_files():
    base_dir = 'content'
    i18n_file = 'i18n/ar.json'
    
    # Load existing translations
    translations = {"categories": {}, "images": {}}
    if os.path.exists(i18n_file):
        with open(i18n_file, 'r', encoding='utf-8') as f:
            translations = json.load(f)

    # Known mappings for categories (I can add more if I know them)
    cat_mapping = {
        "حيوانات": "animals",
        "طعام": "food",
        "مركبات": "vehicles",
        "أماكن": "locations",
        "وظائف": "jobs"
    }
    
    # Process Categories
    if os.path.exists(base_dir):
        # List directories
        dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
        
        for d in dirs:
            # Check if it contains Arabic (simple check: not ascii)
            if not all(ord(c) < 128 for c in d):
                arabic_name = d
                english_id = cat_mapping.get(arabic_name)
                
                # If unknown, generate generic ID
                if not english_id:
                    english_id = f"category_{len(translations['categories']) + 1}"
                
                # Rename folder
                old_path = os.path.join(base_dir, arabic_name)
                new_path = os.path.join(base_dir, english_id)
                
                # Handle collision if target exists (merge)
                if os.path.exists(new_path):
                    print(f"Merging {arabic_name} into {english_id}")
                    for item in os.listdir(old_path):
                        shutil.move(os.path.join(old_path, item), os.path.join(new_path, item))
                    os.rmdir(old_path)
                else:
                    print(f"Renaming {arabic_name} to {english_id}")
                    os.rename(old_path, new_path)
                
                # Update translation
                translations["categories"][english_id] = arabic_name

    # Process Images inside Categories
    # Re-list directories as they might have changed
    dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    
    for cat_id in dirs:
        cat_path = os.path.join(base_dir, cat_id)
        files = [f for f in os.listdir(cat_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        for f in files:
            name_without_ext = os.path.splitext(f)[0]
            ext = os.path.splitext(f)[1]
            
            # Check if image name is Arabic
            if not all(ord(c) < 128 for c in name_without_ext):
                arabic_name = name_without_ext
                
                # Generate simple ID (hash or counter? Counter per category is cleaner but global ID is needed for translation map)
                # Let's use a simple transliteration-like or just hash to avoid collisions
                # Actually, just use category_image_counter
                
                # Check if we already have a translation for this (idempotency)
                existing_id = None
                for k, v in translations["images"].items():
                    if v == arabic_name:
                        existing_id = k
                        break
                
                if existing_id:
                    english_id = existing_id
                else:
                    # Create new ID
                    # Try to map common ones? Too many.
                    # Just use catId_imgX
                    count = len([k for k in translations["images"].keys() if k.startswith(f"{cat_id}_")]) + 1
                    english_id = f"{cat_id}_{count}"
                
                # Rename file
                old_file = os.path.join(cat_path, f)
                new_file = os.path.join(cat_path, f"{english_id}{ext}")
                
                if not os.path.exists(new_file):
                    print(f"Renaming {f} to {english_id}{ext}")
                    os.rename(old_file, new_file)
                    translations["images"][english_id] = arabic_name
                else:
                    print(f"Skipping {f}, target {english_id}{ext} exists")

    # Save translations
    with open(i18n_file, 'w', encoding='utf-8') as f:
        json.dump(translations, f, indent=2, ensure_ascii=False)
        
    print("Processing complete!")

if __name__ == "__main__":
    process_arabic_files()
