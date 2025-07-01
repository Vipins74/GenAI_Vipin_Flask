# Lead Scoring System

A comprehensive web-based lead scoring system that helps sales teams prioritize prospects based on multiple criteria including company size, industry, job title, budget, and engagement metrics.

## Features

### 🎯 **Lead Scoring Engine**
- Multi-factor scoring algorithm based on:
  - Company size (Startup to Enterprise)
  - Industry relevance (Technology, Finance, Healthcare, etc.)
  - Job title seniority (CEO, CTO, VP, Director, etc.)
  - Budget range (No budget to $100k+)
  - Engagement metrics (email opens, clicks, website visits, content downloads, demo requests)

### 📊 **Analytics Dashboard**
- Real-time metrics and KPIs
- Grade distribution visualization (A-F scoring)
- Industry performance analysis
- Conversion rate tracking
- Interactive charts and graphs

### 👥 **Lead Management**
- View all leads with scores and grades
- Add new leads with automatic scoring
- Sort leads by score (highest priority first)
- Detailed lead information display

### 🧮 **Lead Scoring Calculator**
- Interactive form to score potential leads
- Real-time score calculation
- Detailed breakdown of score components
- Grade assignment (A-F scale)

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **UI Framework**: Bootstrap 5
- **Charts**: Chart.js
- **Icons**: Font Awesome
- **Data Processing**: Native Python

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd lead-scoring-system
   ```

2. **Easy startup (recommended)**
   ```bash
   ./start.sh
   ```

3. **Manual setup (alternative)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python app.py
   ```

4. **Access the application**
   Open your browser and navigate to: `http://localhost:5000`

5. **Run API demo (optional)**
   ```bash
   # In a new terminal (while the app is running)
   python demo.py
   ```

## Scoring Algorithm

### Scoring Weights

| Category | Weight Range | Description |
|----------|--------------|-------------|
| **Company Size** | 5-25 points | Startup (5) to Enterprise (25) |
| **Industry** | 5-25 points | Technology (25), Finance (20), Healthcare (18), etc. |
| **Job Title** | 5-25 points | CEO (25), CTO (22), VP (20), Director (18), etc. |
| **Budget** | 0-20 points | No budget (0) to Over $100k (20) |
| **Engagement** | Variable | Email opens (2 each), Demo requests (15 each), etc. |

### Grade Scale
- **A Grade**: 80-100 points (Hot leads)
- **B Grade**: 60-79 points (Warm leads)
- **C Grade**: 40-59 points (Cold leads)
- **D Grade**: 20-39 points (Low priority)
- **F Grade**: 0-19 points (Unqualified)

## API Endpoints

### GET `/api/leads`
Returns all leads with calculated scores and grades.

### POST `/api/leads`
Adds a new lead to the system.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@company.com",
  "company": "Tech Corp",
  "company_size": "large",
  "industry": "technology",
  "job_title": "cto",
  "budget": "50k_100k"
}
```

### POST `/api/leads/score`
Calculates score for lead data without saving.

### GET `/api/analytics`
Returns analytics data including metrics and distributions.

## Usage Guide

### 1. Dashboard View
- Overview of key metrics
- Visual analytics with charts
- Quick insights into lead quality distribution

### 2. Leads Management
- View all leads sorted by score
- Monitor lead grades and creation dates
- Refresh data in real-time

### 3. Score Calculator
- Input lead characteristics
- Get instant score calculation
- View detailed breakdown of score components

### 4. Add New Leads
- Simple form to add prospects
- Automatic score calculation
- Required fields validation

## Customization

### Adjusting Scoring Weights
Modify the `SCORING_WEIGHTS` dictionary in `app.py`:

```python
SCORING_WEIGHTS = {
    'company_size': {
        'startup': 5,
        'small': 10,
        # ... customize values
    },
    # ... other categories
}
```

### Adding New Industries
Update the industry options in both:
- `SCORING_WEIGHTS['industry']` in `app.py`
- HTML select options in `templates/index.html`

### Modifying Grade Thresholds
Adjust the `get_lead_grade()` function in `app.py`:

```python
def get_lead_grade(score):
    if score >= 80:  # Customize threshold
        return 'A'
    # ... other grades
```

## Sample Data

The system includes sample leads for demonstration:
- **John Smith** (TechCorp Inc.) - High-scoring technology lead
- **Sarah Johnson** (HealthPlus Solutions) - Medium-scoring healthcare lead

## Development

### Project Structure
```
lead-scoring-system/
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   └── leadscoring.js    # Frontend JavaScript
├── README.md             # Project documentation
└── .gitignore           # Git ignore rules
```

### Adding Features
1. **New Scoring Criteria**: Update `SCORING_WEIGHTS` and calculation logic
2. **Additional Analytics**: Extend `/api/analytics` endpoint
3. **Lead Import**: Add CSV/Excel import functionality
4. **Export Features**: Add data export capabilities

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues:
1. Check the documentation above
2. Review the code comments
3. Create an issue in the repository

---

**Built with ❤️ for better lead management**
