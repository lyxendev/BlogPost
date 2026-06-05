from openai import OpenAI
import os
from dotenv import load_dotenv

# ==================== LOAD API KEY FROM .env ====================
load_dotenv()  # .env loading

API_KEY = os.getenv("GROQ_API_KEY")

# Check if API key exists
if not API_KEY:
    print(f"❌ API key not found! Please check your .env file.")
    print(f"Create a .env file with: GROQ_API_KEY=your_key_here")
    exit()

# Groq API setup
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=API_KEY
)

def generate_blog_post(topic, tone="friendly", length="medium"):
    """
    Generate a blog post
    topic: Subject (e.g., "Python tips for beginners")
    tone: friendly, professional, humorous
    length: short (~300 words), medium (~600 words), long (~1000 words)
    """
    
    length_map = {
        "short": "3-4 paragraphs (about 300 words)",
        "medium": "5-6 paragraphs (about 600 words)",
        "long": "8-10 paragraphs (about 1000 words)"
    }
    
    prompt = f"""
    You are a professional blogger. Write a blog post about the following topic.
    
    Topic: {topic}
    Tone: {tone}
    Length: {length_map[length]}
    
    Requirements:
    1. Put the title on the first line.
    2. Include an introduction, body, and conclusion.
    3. Include at least 3 actionable tips that readers can apply.
    4. Write in English.
    
    Blog post:
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an expert blogger who writes engaging, helpful blog posts in English."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

def save_blog_post(content, filename=None):
    """Save blog post to a file"""
    if filename is None:
        filename = "blog_post.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ Saved: {filename}")

# Main execution
if __name__ == "__main__":
    print("=" * 50)
    print("📝 Blog Post Generator")
    print("=" * 50)
    
    # Get user input
    topic = input("\n✏️ Enter blog topic: ")
    
    print("\nChoose tone:")
    print("1. Friendly")
    print("2. Professional")
    print("3. Humorous")
    tone_choice = input("Choose (1/2/3): ")
    
    tone_map = {"1": "friendly", "2": "professional", "3": "humorous"}
    tone = tone_map.get(tone_choice, "friendly")
    
    print("\nChoose length:")
    print("1. Short (~300 words)")
    print("2. Medium (~600 words)")
    print("3. Long (~1000 words)")
    length_choice = input("Choose (1/2/3): ")
    
    length_map = {"1": "short", "2": "medium", "3": "long"}
    length = length_map.get(length_choice, "medium")
    
    print("\n⏳ Generating blog post... (10-20 seconds)\n")
    
    # Generate
    try:
        blog_content = generate_blog_post(topic, tone, length)
        print(blog_content)
        print("\n" + "-" * 50)
        
        # Ask to save
        save_choice = input("\n💾 Save to file? (y/n): ")
        if save_choice.lower() == 'y':
            filename = input("Filename (Enter for default): ")
            if not filename:
                filename = f"blog_{topic[:20].replace(' ', '_')}.md"
            if not filename.endswith('.md'):
                filename += '.md'
            save_blog_post(blog_content, filename)
        
        print("\n🎉 Done!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check your API key.")