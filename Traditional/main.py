# Entry point & CLI
from config import *
from agents.gemini_agent import GeminiAgent
from agents.docs_agent import DocsAgent

def main():
    print("🤖 Agentic AI Documentation Assistant")
    print("=" * 50)
    
    # Initialize agents
    gemini = GeminiAgent(GEMINI_API_KEY, MODEL_NAME)
    docs = DocsAgent(SERVICE_ACCOUNT_FILE, SCOPES)

    print(f"📧 Service Account: {docs.sa_email}")
    print("Share your Google Doc with this email!")
    
    while True:
        topic = input("\n📝 Enter work topic (or 'quit'): ").strip()
        if topic.lower() == 'quit':
            break
        
        details = input("🔍 Additional details (optional): ").strip()
        
        print("🧠 Generating documentation...")
        
        # Step 1: Generate content
        doc_data = gemini.generate_work_documentation(topic, details)
        print(doc_data)
        # Step 2: Write to Docs
        print("📄 Writing to Google Docs...")
        success = docs.write_daily_entry(DOC_ID, doc_data)
        
        if success:
            print("🎉 Daily documentation complete!")
        else:
            print("❌ Failed to write to Docs. Check permissions.")

if __name__ == "__main__":
    main()
