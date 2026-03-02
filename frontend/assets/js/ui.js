// UI Module - Handles all UI interactions
const UI = {
    // Modal management
    openModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('show');
        }
    },

    closeModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('show');
        }
    },

    closeAllModals() {
        document.querySelectorAll('.modal').forEach(modal => {
            modal.classList.remove('show');
        });
    },

    // Navigation
    navigateToSection(sectionName) {
        // Hide all sections
        document.querySelectorAll('.content-section').forEach(section => {
            section.classList.remove('active');
        });

        // Show active section
        const section = document.getElementById(`${sectionName}-section`);
        if (section) {
            section.classList.add('active');
        }

        // Update active nav link
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        const activeLink = document.querySelector(`[data-section="${sectionName}"]`);
        if (activeLink) {
            activeLink.classList.add('active');
        }
    },

    // Table rendering
    renderTableRow(data, columns) {
        const row = document.createElement('tr');
        columns.forEach(column => {
            const cell = document.createElement('td');
            const value = data[column];
            
            if (column === 'status') {
                cell.appendChild(createStatusBadge(value));
            } else if (column.includes('price') || column.includes('cost') || column.includes('revenue')) {
                cell.textContent = formatCurrency(value);
            } else if (column.includes('date')) {
                cell.textContent = formatDate(value);
            } else {
                cell.textContent = value || '-';
            }
            
            row.appendChild(cell);
        });
        return row;
    },

    renderTable(containerId, data, columns) {
        const tbody = document.getElementById(containerId);
        if (!tbody) return;
        
        emptyElement(tbody);
        data.forEach(item => {
            tbody.appendChild(this.renderTableRow(item, columns));
        });
    },

    // Form handling
    populateSelect(selectId, options, valueField = 'id', textField = 'name') {
        const select = document.getElementById(selectId);
        if (!select) return;

        emptyElement(select);
        options.forEach(option => {
            const opt = document.createElement('option');
            opt.value = option[valueField];
            opt.textContent = option[textField];
            select.appendChild(opt);
        });
    },

    clearForm(formId) {
        const form = document.getElementById(formId);
        if (form) {
            form.reset();
        }
    },

    populateForm(formId, data) {
        const form = document.getElementById(formId);
        if (!form) return;

        Object.keys(data).forEach(key => {
            const field = form.elements[key];
            if (field) {
                field.value = data[key];
            }
        });
    },

    // Chart rendering
    renderChart(canvasId, type, data, options = {}) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        if (window.charts && window.charts[canvasId]) {
            window.charts[canvasId].destroy();
        }

        if (!window.charts) {
            window.charts = {};
        }

        const mergedOptions = { ...getChartOptions(), ...options };
        window.charts[canvasId] = new Chart(ctx, {
            type,
            data,
            options: mergedOptions
        });

        return window.charts[canvasId];
    },

    renderLineChart(canvasId, labels, datasets, title = '') {
        const data = {
            labels,
            datasets: datasets.map(dataset => ({
                label: dataset.label,
                data: dataset.data,
                backgroundColor: CONFIG.CHARTS.backgroundColor,
                borderColor: CONFIG.CHARTS.borderColor,
                borderWidth: CONFIG.CHARTS.borderWidth,
                tension: CONFIG.CHARTS.tension,
                fill: true
            }))
        };

        return this.renderChart(canvasId, 'line', data, {
            plugins: {
                title: {
                    display: !!title,
                    text: title
                }
            }
        });
    },

    renderBarChart(canvasId, labels, datasets, title = '') {
        const data = {
            labels,
            datasets: datasets.map(dataset => ({
                label: dataset.label,
                data: dataset.data,
                backgroundColor: CONFIG.CHARTS.backgroundColor,
                borderColor: CONFIG.CHARTS.borderColor,
                borderWidth: CONFIG.CHARTS.borderWidth
            }))
        };

        return this.renderChart(canvasId, 'bar', data, {
            plugins: {
                title: {
                    display: !!title,
                    text: title
                }
            }
        });
    },

    renderPieChart(canvasId, labels, data, title = '') {
        const colors = [
            '#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6',
            '#ec4899', '#14b8a6', '#f97316', '#6366f1', '#06b6d4'
        ];

        const chartData = {
            labels,
            datasets: [{
                data,
                backgroundColor: colors.slice(0, labels.length),
                borderWidth: 2,
                borderColor: '#fff'
            }]
        };

        return this.renderChart(canvasId, 'pie', chartData, {
            plugins: {
                title: {
                    display: !!title,
                    text: title
                }
            }
        });
    }
};

// Initialize UI event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            const section = link.getAttribute('data-section');
            if (section && section !== 'logout') {
                e.preventDefault();
                UI.navigateToSection(section);
            }
        });
    });

    // Modal close buttons
    document.querySelectorAll('.close-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const modal = e.target.closest('.modal');
            if (modal) {
                modal.classList.remove('show');
            }
        });
    });

    // Modal backdrop click
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('show');
            }
        });
    });

    // Cancel buttons
    document.querySelectorAll('[id$="CancelBtn"]').forEach(btn => {
        btn.addEventListener('click', () => {
            UI.closeAllModals();
        });
    });

    // Default to dashboard
    UI.navigateToSection('dashboard');
});
