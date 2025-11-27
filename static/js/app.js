// File upload handling
const fileInput = document.getElementById('fileInput');
const fileUploadArea = document.getElementById('file-upload-area');
const uploadPrompt = document.getElementById('uploadPrompt');
const fileList = document.getElementById('fileList');
const analyzeBtn = document.getElementById('analyzeBtn');
const loading = document.getElementById('loading');
const results = document.getElementById('results');

let selectedFiles = [];
fileUploadArea.style.display = 'none';

// Mode selection handling
const modeRadios = document.querySelectorAll('input[name="mode"]');
modeRadios.forEach(radio => {
    radio.addEventListener('change', (e) => {
        if (e.target.value === 'live') {
            fileUploadArea.style.display = 'none';
        } else {
            fileUploadArea.style.display = 'block';
        }
    });
});

// File upload events
fileUploadArea.addEventListener('click', () => {
    if (document.querySelector('input[name="mode"]:checked').value === 'files') {
        fileInput.click();
    }
});

fileUploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileUploadArea.classList.add('dragover');
});

fileUploadArea.addEventListener('dragleave', () => {
    fileUploadArea.classList.remove('dragover');
});

fileUploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    fileUploadArea.classList.remove('dragover');
    handleFiles(e.dataTransfer.files);
});

fileInput.addEventListener('change', (e) => {
    handleFiles(e.target.files);
});

function handleFiles(files) {
    selectedFiles = Array.from(files);
    displayFiles();
}

function displayFiles() {
    if (selectedFiles.length === 0) {
        uploadPrompt.style.display = 'block';
        fileList.innerHTML = '';
        return;
    }
    
    uploadPrompt.style.display = 'none';
    fileList.innerHTML = selectedFiles.map((file, index) => `
        <div class="file-item">
            <span>📄 ${file.name}</span>
            <button onclick="removeFile(${index})">×</button>
        </div>
    `).join('');
}

function removeFile(index) {
    selectedFiles.splice(index, 1);
    displayFiles();
}

// Tab switching
const tabButtons = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

tabButtons.forEach(button => {
    button.addEventListener('click', () => {
        const tabName = button.dataset.tab;
        
        tabButtons.forEach(btn => btn.classList.remove('active'));
        tabContents.forEach(content => content.classList.remove('active'));
        
        button.classList.add('active');
        document.getElementById(tabName).classList.add('active');
    });
});

// Analyze button
analyzeBtn.addEventListener('click', async () => {
    const mode = document.querySelector('input[name="mode"]:checked').value;
    const includeWeekends = document.getElementById('includeWeekends').checked;
    
    if (mode === 'files' && selectedFiles.length === 0) {
        alert('Please upload at least one CSV file');
        return;
    }
    
    loading.style.display = 'block';
    results.style.display = 'none';
    analyzeBtn.disabled = true;
    
    const formData = new FormData();
    formData.append('mode', mode);
    formData.append('include_weekends', includeWeekends);
    
    if (mode === 'files') {
        selectedFiles.forEach(file => {
            formData.append('files', file);
        });
    }
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        displayResults(data);
        
        loading.style.display = 'none';
        results.style.display = 'block';
        
        // Scroll to results
        results.scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during analysis');
        loading.style.display = 'none';
    } finally {
        analyzeBtn.disabled = false;
    }
});

function displayResults(data) {
    // Days badge
    document.getElementById('daysBadge').textContent = `${data.days} Days Analyzed`;
    
    // Overview metrics
    document.getElementById('priceImpact').textContent = data.total_price_difference;
    
    const totalToAdd = Object.values(data.rooms_to_add).reduce((acc, building) => {
        return acc + Object.values(building).reduce((sum, val) => sum + val, 0);
    }, 0);
    document.getElementById('roomsToAdd').textContent = totalToAdd;
    
    const totalToRemove = Object.keys(data.rooms_to_remove).length;
    document.getElementById('roomsToRemove').textContent = totalToRemove;
    
    // Delta summary
    document.getElementById('deltaSummary').innerHTML = createTable(data.delta, true);
    
    // Configuration
    document.getElementById('currentConfig').innerHTML = createTable(data.current_config);
    document.getElementById('recommendedConfig').innerHTML = createTable(data.recommended_config);
    document.getElementById('additions').innerHTML = createTable(data.additions);
    document.getElementById('reductions').innerHTML = createTable(data.reductions);
    
    // Locations
    document.getElementById('locationsBefore').innerHTML = createNestedTable(data.locations_before);
    document.getElementById('locationsAfter').innerHTML = createNestedTable(data.locations_after);
    document.getElementById('roomsToAddDetails').innerHTML = createNestedTable(data.rooms_to_add);
    document.getElementById('roomsToRemoveDetails').innerHTML = createObjectTable(data.rooms_to_remove);
    
    // Parts
    document.getElementById('totalPresent').innerHTML = createTable(data.total_present);
    document.getElementById('totalNeeded').innerHTML = createTable(data.total_needed);
    document.getElementById('partsChanges').innerHTML = createTable(data.parts_changes, true);
    
    // Usage stats
    displayUsageStats(data.usage_stats);
}

function createTable(data, showColors = false) {
    if (Object.keys(data).length === 0) {
        return '<p class="neutral">No data available</p>';
    }
    
    const bowOrder = ['BowOne', 'BowTwo', 'BowFour', 'BowSix', 'BowNine', 'BowTwelve'];
    
    const sortedEntries = Object.entries(data).sort(([keyA], [keyB]) => {
        const indexA = bowOrder.indexOf(keyA);
        const indexB = bowOrder.indexOf(keyB);
        if (indexA !== -1 && indexB !== -1) return indexA - indexB;
        if (indexA !== -1) return -1;
        if (indexB !== -1) return 1;
        return keyA.localeCompare(keyB);
    });
    
    const rows = sortedEntries.map(([key, value]) => {
        let valueClass = '';
        if (showColors) {
            if (value > 0) valueClass = 'positive';
            else if (value < 0) valueClass = 'negative';
            else valueClass = 'neutral';
        }
        
        const displayKey = key.replace(/^Bow/, 'BOW ');
        
        return `
            <tr>
                <td>${displayKey}</td>
                <td class="${valueClass}">${value > 0 && showColors ? '+' : ''}${value}</td>
            </tr>
        `;
    }).join('');
    
    return `
        <table>
            <thead>
                <tr>
                    <th>Item</th>
                    <th>Quantity</th>
                </tr>
            </thead>
            <tbody>
                ${rows}
            </tbody>
        </table>
    `;
}

function createNestedTable(data) {
    if (Object.keys(data).length === 0) {
        return '<p class="neutral">No data available</p>';
    }
    
    const bowOrder = ['BowOne', 'BowTwo', 'BowFour', 'BowSix', 'BowNine', 'BowTwelve'];
    
    const sections = Object.entries(data).map(([location, items]) => {
        let itemsHtml;
        
        if (Array.isArray(items)) {
            const sortedItems = [...items].sort((a, b) => {
                const indexA = bowOrder.indexOf(a);
                const indexB = bowOrder.indexOf(b);
                if (indexA !== -1 && indexB !== -1) return indexA - indexB;
                if (indexA !== -1) return -1;
                if (indexB !== -1) return 1;
                return a.localeCompare(b);
            });
            
            itemsHtml = sortedItems.map(item => {
                const displayItem = item.replace(/^Bow/, 'BOW ');
                return `<li>${displayItem}</li>`;
            }).join('');
            
            return `
                <div style="margin-bottom: 16px;">
                    <strong>${location}</strong>
                    <ul style="margin-left: 20px; margin-top: 8px;">
                        ${itemsHtml}
                    </ul>
                </div>
            `;
        } else {
            const sortedEntries = Object.entries(items)
                .filter(([_, value]) => value > 0)
                .sort(([keyA], [keyB]) => {
                    const indexA = bowOrder.indexOf(keyA);
                    const indexB = bowOrder.indexOf(keyB);
                    if (indexA !== -1 && indexB !== -1) return indexA - indexB;
                    if (indexA !== -1) return -1;
                    if (indexB !== -1) return 1;
                    return keyA.localeCompare(keyB);
                });
            
            const rows = sortedEntries.map(([key, value]) => {
                const displayKey = key.replace(/^Bow/, 'BOW ');
                return `
                    <tr>
                        <td>${displayKey}</td>
                        <td>${value}</td>
                    </tr>
                `;
            }).join('');
            
            if (rows === '') return '';
            
            return `
                <div style="margin-bottom: 24px;">
                    <strong style="display: block; margin-bottom: 12px; font-size: 16px;">${location}</strong>
                    <table>
                        <thead>
                            <tr>
                                <th>Room Type</th>
                                <th>Quantity</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${rows}
                        </tbody>
                    </table>
                </div>
            `;
        }
    }).join('');
    
    return sections || '<p class="neutral">No changes needed</p>';
}

function createObjectTable(data) {
    if (Object.keys(data).length === 0) {
        return '<p class="neutral">No rooms to remove</p>';
    }
    
    const rows = Object.entries(data).map(([key, value]) => `
        <tr>
            <td>${key}</td>
            <td>${value}</td>
        </tr>
    `).join('');
    
    return `
        <table>
            <thead>
                <tr>
                    <th>Location</th>
                    <th>Count</th>
                </tr>
            </thead>
            <tbody>
                ${rows}
            </tbody>
        </table>
    `;
}

function displayUsageStats(stats) {
    const container = document.getElementById('usageStats');
    container.innerHTML = '';

    if (!stats || Object.keys(stats).length === 0) {
        container.innerHTML = '<p class="neutral">No usage statistics available</p>';
        return;
    }

    const primary = getComputedStyle(document.documentElement).getPropertyValue('--primary').trim();
    const primaryDark = getComputedStyle(document.documentElement).getPropertyValue('--primary-dark').trim();

    function makeGradient(ctx) {
        const chart = ctx.chart;
        const { chartArea } = chart;
        if (!chartArea) return primary + '55';
        const gradient = chart.ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
        gradient.addColorStop(0, primary + '00');
        gradient.addColorStop(1, primary + '88');
        return gradient;
    }

    const weekdayOrder = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];

    Object.entries(stats).forEach(([roomType, data]) => {
        const utilization = typeof data.percentage === 'number' ? data.percentage : 0;
        const hourlyAvg = data.hourly_avg || {};
        const weekdayAvg = data.weekday_avg || {};
        const timeline = Array.isArray(data.timeline) ? data.timeline : [];

        const recommendation =
            utilization > 70 ? "Increase Capacity" :
            utilization < 25 ? "Reduce / Reallocate" :
            "Healthy Usage";

        const recommendationClass =
            utilization > 70 ? "recommend-tag high" :
            utilization < 25 ? "recommend-tag low" :
            "recommend-tag";

        const card = document.createElement('div');
        card.className = 'usage-card-advanced';
        card.innerHTML = `
            <div class="room-summary">
                <div class="summary-metric">Utilization: <strong>${utilization}%</strong></div>
                <div class="${recommendationClass}">${recommendation}</div>
            </div>
            <h4>${roomType}</h4>
            <canvas id="${roomType}-hourly"></canvas>
            <canvas id="${roomType}-weekday" style="margin-top: 24px;"></canvas>
            <canvas id="${roomType}-distribution" style="margin-top: 24px;"></canvas>
        `;
        container.appendChild(card);

        // ---- Hourly Chart ----
        new Chart(document.getElementById(`${roomType}-hourly`).getContext('2d'), {
            type: 'bar',
            data: {
                labels: Object.keys(hourlyAvg).map(Number).sort((a, b) => a - b),
                datasets: [{
                    label: 'Avg occupancy per hour',
                    data: Object.keys(hourlyAvg).map(h => hourlyAvg[h]),
                    borderColor: primaryDark,
                    borderWidth: 2,
                    borderRadius: 10,
                    backgroundColor: (ctx) => makeGradient(ctx),
                    barPercentage: 0.55,
                    categoryPercentage: 0.55
                }]
            },
            options: { 
                responsive: true, 
                animation: { duration: 900 },
                scales: {
                    x: { title: { display: true, text: 'Hour of Day' } },
                    y: { title: { display: true, text: 'Average Number of People' }, beginAtZero: true }
                }
            }
        });

        // ---- Weekday Chart ----
        const days = weekdayOrder.filter(d => weekdayAvg[d] !== undefined);
        new Chart(document.getElementById(`${roomType}-weekday`).getContext('2d'), {
            type: 'bar',
            data: {
                labels: days,
                datasets: [{
                    label: 'Avg occupancy per day',
                    data: days.map(d => weekdayAvg[d]),
                    borderColor: primaryDark,
                    borderWidth: 2,
                    borderRadius: 10,
                    backgroundColor: (ctx) => makeGradient(ctx),
                    barPercentage: 0.55,
                    categoryPercentage: 0.55
                }]
            },
            options: { 
                responsive: true, 
                animation: { duration: 900 },
                scales: {
                    x: { title: { display: true, text: 'Day of Week' } },
                    y: { title: { display: true, text: 'Average Number of People' }, beginAtZero: true }
                }
            }
        });

        // ✅ NEW — Cumulative Occupancy Distribution
        const occValues = timeline.map(p => p.Occupancy ?? 0);
        const maxOcc = Math.max(...occValues, 0);

        const counts = new Array(maxOcc + 1).fill(0);
        occValues.forEach(v => counts[v]++);

        const total = occValues.length || 1;
        const percentages = counts.map(c => (c / total * 100));

        const cumulative = percentages.map((_, i) =>
            percentages.slice(0, i + 1).reduce((a, b) => a + b, 0)
        );

        new Chart(document.getElementById(`${roomType}-distribution`).getContext('2d'), {
            type: 'line',
            data: {
                labels: cumulative.map((_, i) => `Up to ${i} people`),
                datasets: [{
                    label: 'Cumulative % of time occupancy ≤ level',
                    data: cumulative,
                    borderColor: primaryDark,
                    fill: false,
                    tension: 0.35,
                    borderWidth: 3,
                    pointRadius: 2
                }]
            },
            options: {
                responsive: true,
                animation: { duration: 1000 },
                plugins: { title: { display: true, text: 'Cumulative Occupancy Distribution' } },
                scales: { 
                    x: { title: { display: true, text: 'Occupancy Level' } },
                    y: { title: { display: true, text: 'Percentage of Time' }, beginAtZero: true, ticks: { callback: v => v + '%' } }
                }
            }
        });
    });
}
