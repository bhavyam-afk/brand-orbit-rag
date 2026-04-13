import random

def main():
    # name, niche, location, description, engagement rate, type
    niche = ["fashion", "comedy", "fitness", "travel", "food", "lifestyle", "technology", "gaming", "health", "finance"]
    name = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi", "harry", "soham", "rajat", "rahul", "sameer", "karan", "harshit", "lana", "mishti", "aayushi", "aarushi", "ananya", "garvit", "alex", "mia", "jordan", "taylor", "casey", "morgan", "blake", "ashley", "parker", "reese", "cameron", "madison", "madison", "sydney", "chris", "sam", "james", "john", "patricia", "michael", "jennifer"]
    location = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose", "delhi", "mumbai", "bangalore", "kolkata", "chennai", "hyderabad", "pune", "ahmedabad", "jaipur", "lucknow", "london", "paris", "tokyo", "dubai", "toronto", "sydney", "bangkok", "istanbul", "mexico city", "singapore"]
    type = ["micro", "macro", "nano", "celebrity"]

    templates = {
    "fitness": [
        "Creates content about {topic1} and {topic2}, focusing on {style}.",
        "Shares tips on {topic1}, workouts, and {topic2} for a healthy lifestyle.",
        "Focuses on {topic1} training methods and {topic2} to achieve {style} goals.",
        "Posts daily {topic1} routines combined with {topic2} for optimal health.",
    ],
    "fashion": [
        "Posts about {topic1}, styling tips, and {topic2}.",
        "Focuses on {style} fashion, outfit ideas, and {topic1}.",
        "Shares {topic1} trends and {topic2} shopping guides in {style}.",
        "Creates lookbooks featuring {topic1} pieces and {topic2} accessories.",
    ],
    "technology": [
        "Creates content on {topic1}, gadget reviews, and {topic2}.",
        "Explains {topic1} and shares insights on {topic2}.",
        "Posts about {topic1} innovations and {topic2} in the {style} space.",
        "Discusses {topic1} developments and {topic2} for tech enthusiasts.",
    ],
    "travel": [
        "Documents adventures in {topic1} and {topic2} destinations.",
        "Shares travel tips for {topic1}, budget hacks, and {topic2} experiences.",
        "Explores {topic1} locations with {style} travel photography and {topic2} guides.",
        "Creates content about {topic1} culture and {topic2} attractions.",
    ],
    "food": [
        "Shares {topic1} and {topic2} recipes with a {style} approach.",
        "Posts cooking videos featuring {topic1}, {topic2}, and culinary tips.",
        "Creates content on {topic1} cuisines and {topic2} food trends.",
        "Explores {topic1} ingredients and {topic2} cooking techniques in {style}.",
    ],
    "lifestyle": [
        "Creates content about {topic1} practices and {topic2} for daily life.",
        "Shares tips on {topic1}, home decor, and {topic2} in a {style} way.",
        "Posts about {topic1} goals and {topic2} improvement strategies.",
        "Documents {topic1} routines and {topic2} lifestyle habits.",
    ],
    "comedy": [
        "Creates {style} comedy skits about {topic1} and {topic2}.",
        "Posts funny content on {topic1}, relationships, and {topic2}.",
        "Shares relatable humor about {topic1} culture and {topic2} situations.",
        "Makes comedic videos featuring {topic1} and {topic2} situations.",
    ],
    "gaming": [
        "Streams and reviews {topic1} games with {topic2} gameplay.",
        "Creates content on {topic1} strategies, tips, and {topic2} gaming news.",
        "Posts {style} gaming videos featuring {topic1} and {topic2}.",
        "Discusses {topic1} updates and {topic2} competitive gaming.",
    ],
    "health": [
        "Shares health tips about {topic1} and {topic2} for overall wellness.",
        "Creates educational content on {topic1}, medical updates, and {topic2}.",
        "Posts about {topic1} prevention and {topic2} in a {style} manner.",
        "Discusses {topic1} treatments and {topic2} health awareness.",
    ],
    "finance": [
        "Creates content about {topic1} investing and {topic2} financial planning.",
        "Shares tips on {topic1} wealth building and {topic2} money management.",
        "Posts about {topic1} strategies and {topic2} in the {style} sector.",
        "Discusses {{topic1}} markets and {topic2} investment opportunities.",
    ]
    }
    
    vocab = {
    "fitness": {
        "topic1": ["strength training", "cardio workouts", "yoga", "pilates", "CrossFit", "weight loss", "muscle building"],
        "topic2": ["nutrition plans", "protein diets", "supplement guides", "recovery techniques", "mobility exercises", "HIIT training"],
        "style": ["beginner-friendly", "high intensity", "daily routines", "results-driven", "transformative", "motivating"]
    },
    "fashion": {
        "topic1": ["seasonal trends", "sustainable fashion", "designer collections", "vintage styles", "streetwear", "luxury brands"],
        "topic2": ["styling hacks", "color coordination", "wardrobe essentials", "accessories", "makeup", "beauty tips"],
        "style": ["luxury", "minimalist", "bohemian", "edgy", "classy", "trendy"]
    },
    "technology": {
        "topic1": ["AI technology", "web development", "mobile apps", "cybersecurity", "blockchain", "cloud computing"],
        "topic2": ["coding tutorials", "tech reviews", "startup news", "gadget comparisons", "software updates"],
        "style": ["cutting-edge", "practical", "innovative", "developer-focused", "beginner-friendly"]
    },
    "travel": {
        "topic1": ["Southeast Asia", "Europe", "North America", "hidden gems", "adventure tourism", "cultural exploration"],
        "topic2": ["visa information", "budget travel", "luxury resorts", "local cuisine", "transportation guides"],
        "style": ["luxury", "budget", "adventurous", "cultural", "off-the-beaten-path"]
    },
    "food": {
        "topic1": ["Indian cuisine", "Italian pasta", "Asian takeout", "vegan recipes", "baking", "street food"],
        "topic2": ["restaurant reviews", "cooking techniques", "food pairing", "dietary tips", "kitchen gadgets"],
        "style": ["healthy", "indulgent", "traditional", "fusion", "experimental"]
    },
    "lifestyle": {
        "topic1": ["morning routines", "meditation", "self-care", "productivity", "minimalism", "sustainable living"],
        "topic2": ["organization tips", "personal development", "mental health", "work-life balance", "goal setting"],
        "style": ["holistic", "practical", "spiritual", "modern", "eco-friendly"]
    },
    "comedy": {
        "topic1": ["relationships", "office humor", "family", "dating mishaps", "social situations", "everyday life"],
        "topic2": ["funny observations", "improv", "stand-up clips", "social commentary", "parody", "satire"],
        "style": ["witty", "observational", "absurdist", "dark humor", "slapstick"]
    },
    "gaming": {
        "topic1": ["FPS games", "RPGs", "mobile games", "esports", "retro games", "indie games"],
        "topic2": ["speedruns", "achievements", "Easter eggs", "walkthroughs", "community events", "tournaments"],
        "style": ["competitive", "casual", "speedrunning", "storytelling", "educational"]
    },
    "health": {
        "topic1": ["mental health", "fitness science", "nutrition", "sleep hygiene", "stress management", "disease prevention"],
        "topic2": ["medical research", "wellness tips", "doctor consultations", "supplements", "exercise science"],
        "style": ["evidence-based", "holistic", "accessible", "scientific", "motivational"]
    },
    "finance": {
        "topic1": ["stock market", "cryptocurrency", "real estate", "side hustles", "retirement planning", "passive income"],
        "topic2": ["investing strategies", "tax tips", "budgeting", "wealth accumulation", "debt management"],
        "style": ["educational", "aggressive", "conservative", "practical", "data-driven"]
    }
    }
    
    # Generate 4000 influencers
    influencers = []
    
    for i in range(4000):
        # Select random attributes
        selected_niche = random.choice(niche)
        selected_name = random.choice(name)
        selected_location = random.choice(location)
        engagement_rate = random.randint(0, 100)
        
        # Generate description from templates and vocab
        template = random.choice(templates[selected_niche])
        vocab_set = vocab[selected_niche]
        topic1 = random.choice(vocab_set["topic1"])
        topic2 = random.choice(vocab_set["topic2"])
        style = random.choice(vocab_set["style"])
        description = template.format(topic1=topic1, topic2=topic2, style=style)
        followers = random.randint(1000, 9000000)
        if followers < 100000:
            selected_type = "nano"
        elif followers < 1000000:
            selected_type = "micro"
        elif followers < 6000000:
            selected_type = "macro"   
        else: 
            selected_type = "celebrity"
        
        # Create influencer document
        influencer_doc = {
            "id": i + 1,
            "username": f"@{selected_name}",
            "niche": selected_niche,
            "location": selected_location,
            "type": selected_type,
            "engagement_rate": engagement_rate,
            "description": description,
            "followers": followers,
        }
        influencers.append(influencer_doc)
    
    # Print sample of generated data
    print(f"Generated {len(influencers)} influencers")
    print("\nSample influencer (first one):")
    print(influencers[0])
    
    # Optional: Save to file
    import json
    with open('data/influencers_data.json', 'w') as f:
        json.dump(influencers, f, indent=2)
    print(f"\nData saved to influencers_data.json")

if __name__ == "__main__":
    main()

