import random
topics = ["Aloo roasting Samosa", "Chai roasting Coffee", "Smartphone roasting Nokia", "Free Fire roasting PUBG"]
with open("current_topic.txt", "w") as f:
    f.write(random.choice(topics))
