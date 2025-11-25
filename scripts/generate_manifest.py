import os
import json

def generate_manifest():
    base_dir = 'content'
    manifest = {
        "version": 1,
        "categories": []
    }

    # Ensure content directory exists
    if not os.path.exists(base_dir):
        print(f"Directory '{base_dir}' not found.")
        return

    # Walk through content directory
    # Sort to ensure consistent order
    categories = sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))])
    
    for cat_id in categories:
        cat_path = os.path.join(base_dir, cat_id)
        
        category = {
            "id": cat_id,
            "images": []
        }
        
        # Get images in category
        images = sorted([f for f in os.listdir(cat_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
        
        for img_file in images:
            img_id = os.path.splitext(img_file)[0]
            category["images"].append({
                "id": img_id,
                "file": f"content/{cat_id}/{img_file}"
            })
            
        if category["images"]:
            manifest["categories"].append(category)

    # Write manifest
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    print("Manifest generated successfully!")

if __name__ == "__main__":
    generate_manifest()
