import os
import json
import shutil

def rename_to_english():
    base_dir = 'content'
    i18n_file = 'i18n/ar.json'
    
    # Load existing translations
    if not os.path.exists(i18n_file):
        print("Translation file not found!")
        return
        
    with open(i18n_file, 'r', encoding='utf-8') as f:
        translations = json.load(f)

    # Translation Dictionary (Arabic -> English)
    # Based on the user's content
    arabic_to_english = {
        # Categories
        "أماكن": "locations",
        "وظائف": "jobs",
        "طعام": "food",
        "حيوانات": "animals",
        "مركبات": "vehicles",
        "أشياء وأدوات": "objects",
        
        # Animals
        "فأر": "mouse", "عقرب": "scorpion", "صرصور": "cockroach", "كلب": "dog", 
        "ذبابة": "fly", "قطة": "cat", "أرنب": "rabbit", "نحلة": "bee", 
        "قرد": "monkey", "تمساح": "crocodile", "زرافة": "giraffe", "حمار": "donkey", 
        "فيل": "elephant", "سمكة": "fish", "دجاجة": "chicken", "حصان": "horse", 
        "ديك": "rooster", "نمر": "tiger", "ضفدع": "frog", "ثعبان": "snake", 
        "سلطعون": "crab", "خفاش": "bat", "حوت": "whale", "بقرة": "cow", 
        "أخطبوط": "octopus", "سلحفاة": "turtle", "دولفين": "dolphin",
        
        # Food
        "كرواسون": "croissant", "برتقال": "orange", "عسل": "honey", "صودا": "soda", 
        "شاي": "tea", "تفاح": "apple", "بيتزا": "pizza", "رمان": "pomegranate", 
        "أندومي": "indomie", "سوشي": "sushi", "تمر": "dates", "برجر": "burger", 
        "مانجا": "mango", "دجاج مقلي": "fried_chicken", "أناناس": "pineapple", 
        "كيوي": "kiwi", "جوز هند": "coconut", "بيض": "egg", "عنب": "grapes", 
        "ليمون": "lemon", "شاورما": "shawarma", "أفوكادو": "avocado", "شمام": "melon", 
        "بطاطا مقلية": "fries", "قهوة": "coffee", "فراولة": "strawberry", "عصير": "juice", 
        "موز": "banana", "كرز": "cherry", "بسكويت": "biscuit", "بطيخ": "watermelon", 
        "حزر": "carrot",
        
        # Vehicles
        "هليكوبتر": "helicopter", "دراجة نارية": "motorcycle", "قطار": "train", 
        "منطاد": "balloon", "جرار": "tractor", "دراجة": "bicycle", 
        "مركبة فضائية": "spaceship", "سيارة": "car", "شاحنة": "truck", 
        "طائرة": "plane", "باص": "bus", "تلفريك": "cable_car", "ميترو": "metro", 
        "صاروخ": "rocket", "غواصة": "submarine", "قارب": "boat", "سفينة": "ship", 
        "يخت": "yacht",

        # Locations
        "مسجد": "mosque", "نخلة": "palm_tree", "قلعة": "castle", "حديقة": "park",
        "مخفر شرطة": "police_station", "مستشفى": "hospital", "صيدلية": "pharmacy",
        "نهر": "river", "الأهرامات": "pyramids", "مسبح": "pool", "مطار": "airport",
        "الكعبة المشرفة": "kaaba", "صحراء": "desert", "مطعم": "restaurant",
        "محكمة": "court", "صالون حلاقة": "barber_shop", "غابة": "forest", "بنك": "bank",

        # Objects (category_6)
        "نظارة": "glasses", "ثلاجة": "fridge", "ملعقة": "spoon", "ماكينة خياطة": "sewing_machine",
        "جوال": "mobile", "كتاب": "book", "سلم": "ladder", "شباك": "window",
        "مظلة": "umbrella", "حقيبة ظهر": "backpack", "مفك": "screwdriver", "شامبو": "shampoo",
        "بوق": "trumpet", "مصعد": "elevator", "مطرقة": "hammer", "كمامة": "mask",
        "مصباح يدوي": "flashlight", "جورب": "sock", "سماعة": "headphone", "مرآة": "mirror",
        "ستارة": "curtain", "مال": "money", "سكين": "knife", "أريكة": "sofa",
        "خيمة": "tent", "مكنسة كهربائية": "vacuum", "كرسي": "chair", "سجادة": "carpet",
        "محفظة": "wallet", "مكيف": "ac", "مزهرية": "vase", "كرة قدم": "football",
        "كرة سلة": "basketball", "جسر": "bridge", "آلة حاسبة": "calculator", "مفتاح": "key",
        "رسالة": "letter", "صابونة": "soap", "لوحة": "painting", "مكواة": "iron",
        "طاولة": "table", "منديل": "tissue", "مقص": "scissors", "خلاط": "blender",
        "مصباح": "lamp", "تلفاز": "tv", "إشارة مرور": "traffic_light", "سرير": "bed",
        "براد شاي": "teapot", "علم": "flag", "ذراع تحكم": "controller", "شاحن": "charger",
        "لابتوب": "laptop", "مرساة": "anchor", "عطر": "perfume", "غسالة": "washing_machine",
        "قلم": "pen", "مخدة": "pillow", "كاميرا": "camera", "كرة طائرة": "volleyball"
    }

    new_translations = {"categories": {}, "images": {}}
    
    # Process Categories
    # We need to find the category ID for each category name
    # But currently the category IDs are 'food', 'animals' etc. which is good.
    # Just need to make sure we keep them.
    
    for cat_id, arabic_name in translations["categories"].items():
        # If the ID is already English (e.g. 'food'), keep it.
        # If it's generic (e.g. 'category_6'), try to rename it.
        
        new_id = cat_id
        if cat_id.startswith("category_"):
            english_name = arabic_to_english.get(arabic_name)
            if english_name:
                new_id = english_name
                
                # Rename folder
                old_path = os.path.join(base_dir, cat_id)
                new_path = os.path.join(base_dir, new_id)
                if os.path.exists(old_path) and not os.path.exists(new_path):
                    print(f"Renaming category {cat_id} to {new_id}")
                    os.rename(old_path, new_path)
        
        new_translations["categories"][new_id] = arabic_name

    # Process Images
    # We need to scan the directories again because we might have renamed categories
    
    dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    
    for cat_id in dirs:
        cat_path = os.path.join(base_dir, cat_id)
        files = [f for f in os.listdir(cat_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        for f in files:
            name_without_ext = os.path.splitext(f)[0]
            ext = os.path.splitext(f)[1]
            
            # Find the Arabic name for this file ID
            # The file ID is currently 'name_without_ext' (e.g. 'food_27')
            arabic_name = translations["images"].get(name_without_ext)
            
            if arabic_name:
                english_name = arabic_to_english.get(arabic_name)
                
                if english_name:
                    new_filename = f"{english_name}{ext}"
                    old_path = os.path.join(cat_path, f)
                    new_path = os.path.join(cat_path, new_filename)
                    
                    if old_path != new_path:
                        print(f"Renaming {f} to {new_filename}")
                        os.rename(old_path, new_path)
                        
                    new_translations["images"][english_name] = arabic_name
                else:
                    # Keep as is if no translation found
                    print(f"No translation found for {arabic_name} ({f})")
                    new_translations["images"][name_without_ext] = arabic_name
            else:
                # File exists but not in translations? Should not happen if we just ran the previous script.
                # Maybe it's already English?
                print(f"Warning: No translation entry for file {f}")
                new_translations["images"][name_without_ext] = name_without_ext

    # Save new translations
    with open(i18n_file, 'w', encoding='utf-8') as f:
        json.dump(new_translations, f, indent=2, ensure_ascii=False)
        
    print("Renaming complete!")

if __name__ == "__main__":
    rename_to_english()
