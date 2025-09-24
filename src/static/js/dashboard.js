// Dashboard JavaScript functionality
let map;
let markers = [];

// Initialize the dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeMap();
    initializeChart();
    initializeReportForm();
    loadCrimeData();
});

// Initialize Leaflet map
function initializeMap() {
    // Default to Lagos, Nigeria
    map = L.map('crime-map').setView([6.6018, 3.3515], 10);
    
    // Add tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    
    console.log('Map initialized');
}

// Initialize Chart.js statistics
function initializeChart() {
    const ctx = document.getElementById('crime-stats-chart').getContext('2d');
    const stats = window.crimeData.statistics;
    
    if (Object.keys(stats).length === 0) {
        // Show empty state
        ctx.fillStyle = '#6c757d';
        ctx.font = '16px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('No data available', ctx.canvas.width / 2, ctx.canvas.height / 2);
        return;
    }
    
    const labels = Object.keys(stats);
    const data = Object.values(stats);
    const colors = [
        '#dc3545', '#fd7e14', '#28a745', '#007bff', 
        '#6f42c1', '#e83e8c', '#20c997', '#ffc107'
    ];
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors.slice(0, labels.length),
                borderWidth: 2,
                borderColor: '#2c3e50'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#fff',
                        padding: 20
                    }
                }
            }
        }
    });
    
    console.log('Chart initialized with data:', stats);
}

// Load and display crime data on map
function loadCrimeData() {
    const reports = window.crimeData.reports;
    
    if (!reports || reports.length === 0) {
        console.log('No crime reports to display');
        return;
    }
    
    // Clear existing markers
    markers.forEach(marker => map.removeLayer(marker));
    markers = [];
    
    // Add markers for each report
    reports.forEach(report => {
        if (report.latitude && report.longitude) {
            const marker = L.circleMarker([report.latitude, report.longitude], {
                color: getCrimeColor(report.category),
                fillColor: getCrimeColor(report.category),
                fillOpacity: 0.8,
                radius: 8,
                weight: 2
            });
            
            // Create popup content
            const popupContent = `
                <div>
                    <h6><strong>${report.category || 'Unknown'}</strong></h6>
                    <p class="mb-1">${report.original_text ? (report.original_text.length > 100 ? report.original_text.substring(0, 100) + '...' : report.original_text) : 'No description'}</p>
                    <small class="text-muted">
                        <i class="fas fa-clock"></i> ${new Date(report.timestamp).toLocaleString()}<br>
                        <i class="fas fa-shield-alt"></i> Trust: ${Math.round(report.trust_score * 100)}%
                    </small>
                </div>
            `;
            
            marker.bindPopup(popupContent);
            marker.addTo(map);
            markers.push(marker);
        }
    });
    
    // Fit map to show all markers if any exist
    if (markers.length > 0) {
        const group = new L.featureGroup(markers);
        map.fitBounds(group.getBounds().pad(0.1));
    }
    
    console.log(`Loaded ${markers.length} crime markers`);
}

// Get color based on crime category
function getCrimeColor(category) {
    const colors = {
        'Robbery': '#dc3545',
        'Theft': '#fd7e14',
        'Assault': '#e83e8c',
        'Vandalism': '#6f42c1',
        'Fraud': '#20c997',
        'Burglary': '#ffc107'
    };
    return colors[category] || '#6c757d';
}

// Initialize report form functionality
function initializeReportForm() {
    const getLocationBtn = document.getElementById('get-location');
    const submitBtn = document.getElementById('submit-report');
    const form = document.getElementById('crime-report-form');
    const latInput = document.getElementById('latitude');
    const lngInput = document.getElementById('longitude');
    const statusDiv = document.getElementById('location-status');
    
    // Get current location
    getLocationBtn.addEventListener('click', function() {
        if (!navigator.geolocation) {
            showLocationStatus('Geolocation is not supported by this browser.', 'error');
            return;
        }
        
        showLocationStatus('Getting your location...', 'loading');
        
        navigator.geolocation.getCurrentPosition(
            function(position) {
                latInput.value = position.coords.latitude.toFixed(6);
                lngInput.value = position.coords.longitude.toFixed(6);
                showLocationStatus('Location captured successfully!', 'success');
            },
            function(error) {
                let message = 'Unable to get location: ';
                switch(error.code) {
                    case error.PERMISSION_DENIED:
                        message += 'Permission denied.';
                        break;
                    case error.POSITION_UNAVAILABLE:
                        message += 'Position unavailable.';
                        break;
                    case error.TIMEOUT:
                        message += 'Request timeout.';
                        break;
                    default:
                        message += 'Unknown error.';
                        break;
                }
                showLocationStatus(message, 'error');
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 600000
            }
        );
    });
    
    // Submit report
    submitBtn.addEventListener('click', function() {
        const description = document.getElementById('incident-description').value.trim();
        
        if (!description) {
            alert('Please provide an incident description.');
            return;
        }
        
        const reportData = {
            report: description,
            latitude: parseFloat(latInput.value) || 0,
            longitude: parseFloat(lngInput.value) || 0
        };
        
        submitReport(reportData);
    });
}

// Show location status
function showLocationStatus(message, type) {
    const statusDiv = document.getElementById('location-status');
    const iconClass = type === 'success' ? 'fa-check-circle text-success' : 
                     type === 'error' ? 'fa-exclamation-circle text-danger' : 
                     'fa-spinner fa-spin text-info';
    
    statusDiv.innerHTML = `
        <small class="${type === 'success' ? 'text-success' : type === 'error' ? 'text-danger' : 'text-info'}">
            <i class="fas ${iconClass} me-1"></i>
            ${message}
        </small>
    `;
}

// Submit crime report to backend
function submitReport(reportData) {
    const submitBtn = document.getElementById('submit-report');
    const originalText = submitBtn.innerHTML;
    
    // Show loading state
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
    
    // Show loading modal
    const loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
    loadingModal.show();
    
    fetch('/api/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(reportData)
    })
    .then(response => response.json())
    .then(data => {
        loadingModal.hide();
        
        if (data.success) {
            // Close the report modal
            const reportModal = bootstrap.Modal.getInstance(document.getElementById('reportModal'));
            reportModal.hide();
            
            // Reset form
            document.getElementById('crime-report-form').reset();
            document.getElementById('location-status').innerHTML = '';
            
            // Show success message
            showAlert('Report submitted successfully! The page will reload to show updated data.', 'success');
            
            // Reload page to show new data
            setTimeout(() => {
                window.location.reload();
            }, 2000);
        } else {
            showAlert(data.message || 'Report could not be processed. Please try again.', 'warning');
        }
    })
    .catch(error => {
        loadingModal.hide();
        console.error('Error submitting report:', error);
        showAlert('Error submitting report. Please check your connection and try again.', 'danger');
    })
    .finally(() => {
        // Reset button state
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
    });
}

// Show alert message
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at the top of the container
    const container = document.querySelector('.container-fluid');
    container.insertBefore(alertDiv, container.firstChild.nextSibling);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Utility function to refresh data without page reload (if needed)
function refreshDashboard() {
    fetch('/api/reports')
        .then(response => response.json())
        .then(data => {
            if (Array.isArray(data)) {
                window.crimeData.reports = data;
                loadCrimeData();
                console.log('Dashboard data refreshed');
            }
        })
        .catch(error => {
            console.error('Error refreshing dashboard:', error);
        });
}
