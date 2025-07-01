#!/usr/bin/env python3
"""
Lead Scoring System Demo Script

This script demonstrates the API functionality of the lead scoring system.
Make sure the Flask application is running on localhost:5000 before running this demo.
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def print_header(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_json(data):
    print(json.dumps(data, indent=2))

def demo_get_leads():
    print_header("DEMO: Getting All Leads")
    
    try:
        response = requests.get(f"{BASE_URL}/api/leads")
        if response.status_code == 200:
            leads = response.json()
            print(f"Found {len(leads)} leads:")
            for lead in leads:
                print(f"  • {lead['name']} ({lead['company']}) - Score: {lead['score']} (Grade {lead['grade']})")
        else:
            print(f"Error: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the application.")
        print("   Make sure the Flask app is running on localhost:5000")
        return False
    return True

def demo_score_lead():
    print_header("DEMO: Scoring a New Lead")
    
    # Sample lead data for scoring
    lead_data = {
        "company_size": "enterprise",
        "industry": "technology", 
        "job_title": "ceo",
        "budget": "over_100k",
        "engagement": {
            "email_opens": 10,
            "email_clicks": 8,
            "website_visits": 15,
            "content_downloads": 5,
            "demo_requests": 2,
            "pricing_page_views": 12
        }
    }
    
    print("Scoring lead with data:")
    print_json(lead_data)
    
    try:
        response = requests.post(f"{BASE_URL}/api/leads/score", json=lead_data)
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Lead Score: {result['score']}/100 (Grade {result['grade']})")
            print("\nScore Breakdown:")
            for category, points in result['breakdown'].items():
                print(f"  • {category.replace('_', ' ').title()}: {points} points")
        else:
            print(f"Error: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the application.")

def demo_add_lead():
    print_header("DEMO: Adding a New Lead")
    
    # Sample new lead
    new_lead = {
        "name": "Alice Johnson",
        "email": "alice.johnson@innovate.com",
        "company": "Innovate Solutions",
        "company_size": "medium",
        "industry": "finance",
        "job_title": "vp",
        "budget": "10k_50k"
    }
    
    print("Adding new lead:")
    print_json(new_lead)
    
    try:
        response = requests.post(f"{BASE_URL}/api/leads", json=new_lead)
        if response.status_code == 201:
            result = response.json()
            print(f"\n✅ Lead added successfully!")
            print(f"   Score: {result['score']}/100 (Grade {result['grade']})")
        else:
            print(f"Error: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the application.")

def demo_analytics():
    print_header("DEMO: Analytics Dashboard")
    
    try:
        response = requests.get(f"{BASE_URL}/api/analytics")
        if response.status_code == 200:
            analytics = response.json()
            print("📊 Current Analytics:")
            print(f"  • Total Leads: {analytics['total_leads']}")
            print(f"  • Average Score: {analytics['average_score']}")
            print(f"  • High Quality Leads: {analytics['high_quality_leads']}")
            
            print(f"\n📈 Grade Distribution:")
            for grade, count in analytics['grade_distribution'].items():
                if count > 0:
                    print(f"  • Grade {grade}: {count} leads")
            
            print(f"\n🏭 Industry Performance:")
            for industry, avg_score in analytics['industry_averages'].items():
                print(f"  • {industry.title()}: {avg_score:.1f} avg score")
        else:
            print(f"Error: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the application.")

def main():
    print("🎯 Lead Scoring System Demo")
    print("=" * 60)
    print("This demo showcases the API functionality of the lead scoring system.")
    print("Make sure the Flask application is running before continuing.")
    print("\nStarting demo in 3 seconds...")
    
    time.sleep(3)
    
    # Run demos
    if demo_get_leads():
        demo_score_lead()
        demo_add_lead()
        demo_analytics()
        
        print_header("DEMO COMPLETE")
        print("🎉 Demo completed successfully!")
        print("🌐 Visit http://localhost:5000 to see the web interface")
        print("📖 Check README.md for more information")

if __name__ == "__main__":
    main()