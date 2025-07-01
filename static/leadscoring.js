// Lead Scoring System JavaScript

let gradeChart, industryChart;

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    loadAnalytics();
    loadLeads();
    initializeCharts();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // Score form submission
    document.getElementById('scoreForm').addEventListener('submit', function(e) {
        e.preventDefault();
        scoreLead();
    });

    // Add lead form submission
    document.getElementById('addLeadForm').addEventListener('submit', function(e) {
        e.preventDefault();
        addLead();
    });

    // Tab change events
    document.querySelectorAll('[data-bs-toggle="tab"]').forEach(tab => {
        tab.addEventListener('shown.bs.tab', function(e) {
            if (e.target.id === 'dashboard-tab') {
                setTimeout(() => {
                    if (gradeChart) gradeChart.resize();
                    if (industryChart) industryChart.resize();
                }, 100);
            }
        });
    });
}

// Load analytics data
async function loadAnalytics() {
    try {
        const response = await fetch('/api/analytics');
        const data = await response.json();
        
        document.getElementById('totalLeads').textContent = data.total_leads;
        document.getElementById('avgScore').textContent = data.average_score;
        document.getElementById('highQualityLeads').textContent = data.high_quality_leads;
        document.getElementById('conversionRate').textContent = 
            Math.round((data.high_quality_leads / data.total_leads) * 100) + '%';
        
        updateCharts(data);
    } catch (error) {
        console.error('Error loading analytics:', error);
        showAlert('Error loading analytics data', 'danger');
    }
}

// Load leads data
async function loadLeads() {
    try {
        const response = await fetch('/api/leads');
        const leads = await response.json();
        
        const tbody = document.getElementById('leadsTableBody');
        tbody.innerHTML = '';
        
        leads.forEach(lead => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${lead.name}</td>
                <td>${lead.company}</td>
                <td>${capitalizeFirst(lead.industry)}</td>
                <td>${capitalizeFirst(lead.job_title)}</td>
                <td>${lead.score}</td>
                <td><span class="badge score-${lead.grade.toLowerCase()} text-white">${lead.grade}</span></td>
                <td>${formatDate(lead.created_at)}</td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading leads:', error);
        showAlert('Error loading leads data', 'danger');
    }
}

// Score a lead
async function scoreLead() {
    const leadData = {
        company_size: document.getElementById('scoreCompanySize').value,
        industry: document.getElementById('scoreIndustry').value,
        job_title: document.getElementById('scoreJobTitle').value,
        budget: document.getElementById('scoreBudget').value,
        engagement: {
            email_opens: parseInt(document.getElementById('emailOpens').value) || 0,
            email_clicks: parseInt(document.getElementById('emailClicks').value) || 0,
            website_visits: parseInt(document.getElementById('websiteVisits').value) || 0,
            content_downloads: parseInt(document.getElementById('contentDownloads').value) || 0,
            demo_requests: parseInt(document.getElementById('demoRequests').value) || 0,
            pricing_page_views: parseInt(document.getElementById('pricingViews').value) || 0
        }
    };

    try {
        const response = await fetch('/api/leads/score', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(leadData)
        });

        const result = await response.json();
        
        if (response.ok) {
            displayScoreResult(result);
        } else {
            showAlert(result.error || 'Error scoring lead', 'danger');
        }
    } catch (error) {
        console.error('Error scoring lead:', error);
        showAlert('Error scoring lead', 'danger');
    }
}

// Display score result
function displayScoreResult(result) {
    document.getElementById('scoreValue').textContent = result.score;
    
    const gradeElement = document.getElementById('scoreGrade');
    gradeElement.textContent = result.grade;
    gradeElement.className = `score-badge score-${result.grade.toLowerCase()} text-white`;
    
    const breakdown = result.breakdown;
    const breakdownHtml = `
        <div class="small">
            <strong>Score Breakdown:</strong><br>
            Company Size: ${breakdown.company_size}<br>
            Industry: ${breakdown.industry}<br>
            Job Title: ${breakdown.job_title}<br>
            Budget: ${breakdown.budget}<br>
            Engagement: ${breakdown.engagement}
        </div>
    `;
    document.getElementById('scoreBreakdown').innerHTML = breakdownHtml;
    
    document.getElementById('scoreResult').style.display = 'block';
}

// Add a new lead
async function addLead() {
    const leadData = {
        name: document.getElementById('leadName').value,
        email: document.getElementById('leadEmail').value,
        company: document.getElementById('leadCompany').value,
        company_size: document.getElementById('leadCompanySize').value,
        industry: document.getElementById('leadIndustry').value,
        job_title: document.getElementById('leadJobTitle').value,
        budget: document.getElementById('leadBudget').value,
        engagement: {
            email_opens: 0,
            email_clicks: 0,
            website_visits: 0,
            content_downloads: 0,
            demo_requests: 0,
            pricing_page_views: 0
        }
    };

    try {
        const response = await fetch('/api/leads', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(leadData)
        });

        const result = await response.json();
        
        if (response.ok) {
            showAlert('Lead added successfully!', 'success');
            document.getElementById('addLeadForm').reset();
            loadLeads();
            loadAnalytics();
        } else {
            showAlert(result.error || 'Error adding lead', 'danger');
        }
    } catch (error) {
        console.error('Error adding lead:', error);
        showAlert('Error adding lead', 'danger');
    }
}

// Initialize charts
function initializeCharts() {
    const gradeCtx = document.getElementById('gradeChart').getContext('2d');
    const industryCtx = document.getElementById('industryChart').getContext('2d');

    gradeChart = new Chart(gradeCtx, {
        type: 'doughnut',
        data: {
            labels: ['A', 'B', 'C', 'D', 'F'],
            datasets: [{
                data: [0, 0, 0, 0, 0],
                backgroundColor: [
                    '#10b981',
                    '#3b82f6',
                    '#f59e0b',
                    '#f97316',
                    '#ef4444'
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });

    industryChart = new Chart(industryCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Average Score',
                data: [],
                backgroundColor: '#2563eb',
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

// Update charts with new data
function updateCharts(data) {
    // Update grade distribution chart
    if (gradeChart) {
        gradeChart.data.datasets[0].data = [
            data.grade_distribution.A,
            data.grade_distribution.B,
            data.grade_distribution.C,
            data.grade_distribution.D,
            data.grade_distribution.F
        ];
        gradeChart.update();
    }

    // Update industry performance chart
    if (industryChart) {
        const industries = Object.keys(data.industry_averages);
        const scores = Object.values(data.industry_averages);
        
        industryChart.data.labels = industries.map(capitalizeFirst);
        industryChart.data.datasets[0].data = scores;
        industryChart.update();
    }
}

// Utility functions
function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString();
}

function showAlert(message, type) {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at top of container
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}