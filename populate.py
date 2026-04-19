import random
import json

def get_type_and_engagement(followers):
    if followers < 10000:
        return "nano", round(random.uniform(0.08, 0.18), 4)
    elif followers < 100000:
        return "micro", round(random.uniform(0.05, 0.12), 4)
    elif followers < 1000000:
        return "macro", round(random.uniform(0.02, 0.06), 4)
    else:
        return "celebrity", round(random.uniform(0.01, 0.03), 4)


def main():

    niche = [
        "fashion", "comedy", "fitness", "travel", "food",
        "lifestyle", "technology", "gaming", "health", "finance",
        "beauty", "education", "sports", "parenting", "motivation"
    ]

    name = [
        "Alice","Bob","Charlie","David","Eve","Frank","Grace","Heidi","harry","soham",
        "rajat","rahul","sameer","karan","harshit","lana","mishti","aayushi","aarushi",
        "ananya","garvit","alex","mia","jordan","taylor","casey","morgan","blake",
        "ashley","parker","reese","cameron","sydney","chris","sam","james","john",
        "patricia","michael","jennifer"
    ]

    location = [
        "New York","Los Angeles","Chicago","Houston","Phoenix",
        "Delhi","Mumbai","Bangalore","Kolkata","Chennai",
        "London","Paris","Tokyo","Dubai","Toronto","Sydney"
    ]

    # 🔥 EXPANDED TEMPLATES
    templates = {
        "fashion": [
            "Creates {style} outfits featuring {topic1} and {topic2}.",
            "Shares fashion inspiration around {topic1} with {topic2} styling.",
            "Focuses on {style} fashion with {topic1} and {topic2} trends.",
            "Posts daily outfit ideas using {topic1} and {topic2}.",
        ],
        "fitness": [
            "Helps audience with {topic1} and {topic2} in a {style} way.",
            "Shares {topic1} workouts and {topic2} routines.",
            "Builds fitness journeys through {topic1} and {topic2}.",
            "Posts {style} fitness plans around {topic1} and {topic2}.",
        ],
        "technology": [
            "Explains {topic1} and reviews {topic2} in a {style} manner.",
            "Creates content on {topic1}, tools, and {topic2}.",
            "Shares insights on {topic1} with {topic2} tutorials.",
        ],
        "food": [
            "Creates {style} recipes using {topic1} and {topic2}.",
            "Shares cooking tips about {topic1} and {topic2}.",
            "Explores {topic1} dishes and {topic2} techniques.",
        ],
        "gaming": [
            "Streams {topic1} and shares {topic2} gameplay.",
            "Creates {style} gaming content around {topic1}.",
            "Posts guides on {topic1} and {topic2}.",
        ],
        "finance": [
            "Educates about {topic1} and {topic2} in a {style} way.",
            "Shares tips on {topic1} and {topic2}.",
            "Breaks down {topic1} strategies and {topic2}.",
        ],
        "beauty": [
            "Shares {topic1} tutorials and {topic2} tips.",
            "Creates {style} beauty content around {topic1}.",
        ],
        "travel": [
            "Documents {style} trips featuring {topic1} and {topic2}.",
            "Explores luxury destinations with {topic1} and {topic2} experiences.",
            "Shares travel guides for {topic1} and {topic2} stays.",
        ],
        "lifestyle": [
            "Creates {style} lifestyle content around {topic1} and {topic2}.",
            "Shares daily routines focused on {topic1} and {topic2}.",
            "Posts {topic1} tips paired with {topic2} inspiration.",
        ],
        "comedy": [
            "Posts funny sketches about {topic1} and {topic2}.",
            "Shares {style} comedy takes on {topic1} trends.",
            "Creates humorous content around {topic1} and {topic2}.",
        ],
        "health": [
            "Offers {topic1} advice and {topic2} wellness tips.",
            "Shares {style} health routines with {topic1} and {topic2}.",
            "Explains {topic1} and {topic2} for better wellbeing.",
        ],
        "education": [
            "Teaches {topic1} concepts and {topic2}.",
            "Simplifies {topic1} using {style} learning methods.",
        ],
        "sports": [
            "Covers {topic1} and {topic2} training.",
            "Shares {style} sports content around {topic1}.",
        ],
        "parenting": [
            "Shares parenting tips about {topic1} and {topic2}.",
            "Creates {style} family content around {topic1}.",
        ],
        "motivation": [
            "Inspires people using {topic1} and {topic2}.",
            "Shares {style} motivational content on {topic1}.",
        ]
    }

    # 🔥 EXPANDED VOCAB
    vocab = {
        "fashion": {
            "topic1": ["streetwear", "luxury brands", "vintage styles", "seasonal outfits"],
            "topic2": ["accessories", "makeup", "styling hacks", "wardrobe tips"],
            "style": ["minimalist", "trendy", "edgy", "classy"]
        },
        "fitness": {
            "topic1": ["gym workouts", "yoga", "cardio", "strength training"],
            "topic2": ["nutrition", "fat loss", "muscle gain", "mobility"],
            "style": ["intense", "beginner-friendly", "daily", "scientific"]
        },
        "technology": {
            "topic1": ["AI", "web dev", "apps", "cybersecurity"],
            "topic2": ["coding", "reviews", "tutorials", "tools"],
            "style": ["simple", "deep", "practical"]
        },
        "food": {
            "topic1": ["Indian food", "Italian", "vegan", "street food"],
            "topic2": ["recipes", "cooking tips", "restaurant reviews"],
            "style": ["healthy", "fusion", "traditional"]
        },
        "gaming": {
            "topic1": ["FPS games", "RPGs", "mobile gaming"],
            "topic2": ["tips", "streams", "walkthroughs"],
            "style": ["competitive", "casual"]
        },
        "finance": {
            "topic1": ["stocks", "crypto", "real estate"],
            "topic2": ["investing", "saving", "budgeting"],
            "style": ["educational", "practical"]
        },
        "beauty": {
            "topic1": ["skincare", "makeup", "haircare"],
            "topic2": ["tutorials", "product reviews"],
            "style": ["glam", "natural"]
        },
        "travel": {
            "topic1": ["luxury resorts", "destination guides", "city escapes"],
            "topic2": ["fine dining", "adventure tours", "cultural stays"],
            "style": ["luxurious", "scenic", "curated"]
        },
        "lifestyle": {
            "topic1": ["home decor", "wellness habits", "daily routines"],
            "topic2": ["self-care", "minimalism", "productivity"],
            "style": ["cozy", "modern", "balanced"]
        },
        "comedy": {
            "topic1": ["relatable jokes", "satire", "sketches"],
            "topic2": ["pop culture", "everyday life", "viral trends"],
            "style": ["funny", "quirky", "energetic"]
        },
        "health": {
            "topic1": ["wellness", "nutrition", "mental health"],
            "topic2": ["fitness", "sleep", "healthy habits"],
            "style": ["supportive", "informative", "uplifting"]
        },
        "education": {
            "topic1": ["math", "coding", "science"],
            "topic2": ["tips", "explanations"],
            "style": ["easy", "interactive"]
        },
        "sports": {
            "topic1": ["cricket", "football", "gym"],
            "topic2": ["training", "matches"],
            "style": ["professional", "casual"]
        },
        "parenting": {
            "topic1": ["kids growth", "daily parenting"],
            "topic2": ["tips", "family life"],
            "style": ["realistic", "informative"]
        },
        "motivation": {
            "topic1": ["success", "discipline"],
            "topic2": ["mindset", "growth"],
            "style": ["inspirational", "practical"]
        }
    }

    influencers = []

    for i in range(1500):  # ✅ reduced size 

        selected_niche = random.choice(niche)
        selected_name = random.choice(name)
        selected_location = random.choice(location)

        followers = random.randint(1000, 5000000)

        # ✅ Type + engagement logic
        selected_type, engagement_rate = get_type_and_engagement(followers)

        # fallback if niche not in template dict
        if selected_niche not in templates:
            selected_niche = "lifestyle"

        template = random.choice(templates[selected_niche])
        vocab_set = vocab[selected_niche]

        topic1 = random.choice(vocab_set["topic1"])
        topic2 = random.choice(vocab_set["topic2"])
        style = random.choice(vocab_set["style"])

        description = template.format(
            topic1=topic1,
            topic2=topic2,
            style=style
        )

        influencer_doc = {
            "id": i + 1,
            "username": f"@{selected_name}",
            "niche": selected_niche,
            "location": selected_location,
            "type": selected_type,
            "followers": followers,
            "engagement_rate": engagement_rate,
            "description": description
        }

        influencers.append(influencer_doc)

    print(f"Generated {len(influencers)} influencers")
    print(influencers[0])

    with open('data/influencers_data.json', 'w') as f:
        json.dump(influencers, f, indent=2)

    print("Data saved successfully")


if __name__ == "__main__":
    main()