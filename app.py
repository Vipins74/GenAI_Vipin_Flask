from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)

# Lead scoring weights and criteria
SCORING_WEIGHTS = {
    'company_size': {
        'startup': 5,
        'small': 10,
        'medium': 15,
        'large': 20,
        'enterprise': 25
    },
    'industry': {
        'technology': 25,
        'finance': 20,
        'healthcare': 18,
        'manufacturing': 15,
        'retail': 12,
        'education': 10,
        'other': 5
    },
    'job_title': {
        'ceo': 25,
        'cto': 22,
        'vp': 20,
        'director': 18,
        'manager': 15,
        'specialist': 10,
        'other': 5
    },
    'engagement': {
        'email_opens': 2,
        'email_clicks': 5,
        'website_visits': 3,
        'content_downloads': 8,
        'demo_requests': 15,
        'pricing_page_views': 10
    },
    'budget': {
        'no_budget': 0,
        'under_10k': 5,
        '10k_50k': 10,
        '50k_100k': 15,
        'over_100k': 20
    }
}

# Sample leads data
sample_leads = [
    {
        'id': 1,
        'name': 'John Smith',
        'email': 'john.smith@techcorp.com',
        'company': 'TechCorp Inc.',
        'company_size': 'large',
        'industry': 'technology',
        'job_title': 'cto',
        'budget': '50k_100k',
        'engagement': {
            'email_opens': 5,
            'email_clicks': 3,
            'website_visits': 8,
            'content_downloads': 2,
            'demo_requests': 1,
            'pricing_page_views': 4
        },
        'created_at': '2024-01-15'
    },
    {
        'id': 2,
        'name': 'Sarah Johnson',
        'email': 'sarah.j@healthplus.com',
        'company': 'HealthPlus Solutions',
        'company_size': 'medium',
        'industry': 'healthcare',
        'job_title': 'director',
        'budget': '10k_50k',
        'engagement': {
            'email_opens': 3,
            'email_clicks': 1,
            'website_visits': 5,
            'content_downloads': 1,
            'demo_requests': 0,
            'pricing_page_views': 2
        },
        'created_at': '2024-01-20'
    }
]

def calculate_lead_score(lead_data):
    """Calculate lead score based on various criteria"""
    score = 0
    
    # Company size score
    company_size = lead_data.get('company_size', '').lower()
    score += SCORING_WEIGHTS['company_size'].get(company_size, 0)
    
    # Industry score
    industry = lead_data.get('industry', '').lower()
    score += SCORING_WEIGHTS['industry'].get(industry, 0)
    
    # Job title score
    job_title = lead_data.get('job_title', '').lower()
    score += SCORING_WEIGHTS['job_title'].get(job_title, 0)
    
    # Budget score
    budget = lead_data.get('budget', '').lower()
    score += SCORING_WEIGHTS['budget'].get(budget, 0)
    
    # Engagement score
    engagement = lead_data.get('engagement', {})
    for activity, count in engagement.items():
        if activity in SCORING_WEIGHTS['engagement']:
            score += SCORING_WEIGHTS['engagement'][activity] * count
    
    return min(score, 100)  # Cap at 100

def get_lead_grade(score):
    """Convert score to letter grade"""
    if score >= 80:
        return 'A'
    elif score >= 60:
        return 'B'
    elif score >= 40:
        return 'C'
    elif score >= 20:
        return 'D'
    else:
        return 'F'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/leads', methods=['GET'])
def get_leads():
    """Get all leads with scores"""
    leads_with_scores = []
    for lead in sample_leads:
        lead_copy = lead.copy()
        lead_copy['score'] = calculate_lead_score(lead)
        lead_copy['grade'] = get_lead_grade(lead_copy['score'])
        leads_with_scores.append(lead_copy)
    
    # Sort by score descending
    leads_with_scores.sort(key=lambda x: x['score'], reverse=True)
    return jsonify(leads_with_scores)

@app.route('/api/leads/score', methods=['POST'])
def score_lead():
    """Score a new lead"""
    lead_data = request.get_json()
    
    if not lead_data:
        return jsonify({'error': 'No lead data provided'}), 400
    
    score = calculate_lead_score(lead_data)
    grade = get_lead_grade(score)
    
    return jsonify({
        'score': score,
        'grade': grade,
        'breakdown': get_score_breakdown(lead_data)
    })

@app.route('/api/leads', methods=['POST'])
def add_lead():
    """Add a new lead"""
    lead_data = request.get_json()
    
    if not lead_data:
        return jsonify({'error': 'No lead data provided'}), 400
    
    # Add ID and timestamp
    lead_data['id'] = len(sample_leads) + 1
    lead_data['created_at'] = datetime.now().strftime('%Y-%m-%d')
    
    # Calculate score
    lead_data['score'] = calculate_lead_score(lead_data)
    lead_data['grade'] = get_lead_grade(lead_data['score'])
    
    sample_leads.append(lead_data)
    
    return jsonify(lead_data), 201

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get lead scoring analytics"""
    leads_with_scores = []
    for lead in sample_leads:
        lead_copy = lead.copy()
        lead_copy['score'] = calculate_lead_score(lead)
        lead_copy['grade'] = get_lead_grade(lead_copy['score'])
        leads_with_scores.append(lead_copy)
    
    # Calculate analytics
    total_leads = len(leads_with_scores)
    avg_score = sum(lead['score'] for lead in leads_with_scores) / total_leads if total_leads > 0 else 0
    
    grade_distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
    for lead in leads_with_scores:
        grade_distribution[lead['grade']] += 1
    
    industry_scores = {}
    for lead in leads_with_scores:
        industry = lead['industry']
        if industry not in industry_scores:
            industry_scores[industry] = []
        industry_scores[industry].append(lead['score'])
    
    industry_avg = {industry: sum(scores)/len(scores) for industry, scores in industry_scores.items()}
    
    return jsonify({
        'total_leads': total_leads,
        'average_score': round(avg_score, 2),
        'grade_distribution': grade_distribution,
        'industry_averages': industry_avg,
        'high_quality_leads': len([l for l in leads_with_scores if l['score'] >= 60])
    })

def get_score_breakdown(lead_data):
    """Get detailed score breakdown"""
    breakdown = {}
    
    # Company size
    company_size = lead_data.get('company_size', '').lower()
    breakdown['company_size'] = SCORING_WEIGHTS['company_size'].get(company_size, 0)
    
    # Industry
    industry = lead_data.get('industry', '').lower()
    breakdown['industry'] = SCORING_WEIGHTS['industry'].get(industry, 0)
    
    # Job title
    job_title = lead_data.get('job_title', '').lower()
    breakdown['job_title'] = SCORING_WEIGHTS['job_title'].get(job_title, 0)
    
    # Budget
    budget = lead_data.get('budget', '').lower()
    breakdown['budget'] = SCORING_WEIGHTS['budget'].get(budget, 0)
    
    # Engagement
    engagement_score = 0
    engagement = lead_data.get('engagement', {})
    for activity, count in engagement.items():
        if activity in SCORING_WEIGHTS['engagement']:
            engagement_score += SCORING_WEIGHTS['engagement'][activity] * count
    breakdown['engagement'] = engagement_score
    
    return breakdown

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)