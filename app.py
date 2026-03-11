import pandas as pd

# ফাইল লোড করা
file_name = "Health.xlsx"

try:
    data = pd.read_excel(file_name)
    # কলামের নামের বাড়তি স্পেস মুছে ফেলা
    data.columns = data.columns.str.strip() 
    print("✅ Excel ফাইল কানেক্ট হয়েছে!")
except Exception as e:
    print(f"❌ ফাইল এরর: {e}")

def check_range(val, range_str):
    try:
        if '-' in str(range_str):
            low, high = map(int, str(range_str).split('-'))
            return low <= val <= high
        return int(range_str) == val
    except:
        return False

while True:
    print("\n--- Health Routine Finder ---")
    try:
        user_age = int(input("আপনার বয়স লিখুন: "))
        user_weight = int(input("আপনার ওজন লিখুন: "))

        # এক্সেলের প্রতিটা সারি চেক করে দেখা হচ্ছে আপনার ইনপুট কোন রেঞ্জে পড়ে
        found = False
        for index, row in data.iterrows():
            if check_range(user_age, row['Age']) and check_range(user_weight, row['Weight']):
                print("\n✅ আপনার জন্য পরামর্শ:")
                print(f"উচ্চতা (প্রায়): {row['Height (ft/in)']}")
                print(f"খাবার: {row['Suggested Foods']}")
                print(f"রুটিন: {row['Daily Routine']}")
                found = True
                break
        
        if not found:
            print("\n⚠️ এই বয়স ও ওজনের সঠিক রেঞ্জ এক্সেলে পাওয়া যায়নি।")
            
    except Exception as e:
        print(f"❌ সমস্যা হয়েছে: {e}")

    if input("\nআবার দেখবেন? (yes/no): ").lower() != "yes":
        break