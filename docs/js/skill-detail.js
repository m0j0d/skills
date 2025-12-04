// Get skill name from URL parameter
function getSkillName() {
    const params = new URLSearchParams(window.location.search);
    return params.get('skill') || window.location.pathname.split('/').pop().replace('.html', '');
}

// Cache buster for fetch requests
const cacheBuster = Date.now();

// Load validation report for a specific skill
async function loadSkillReport(skillName) {
    try {
        const response = await fetch(`../test-results/${skillName}/basic.json?v=${cacheBuster}`);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`Failed to load validation report for ${skillName}:`, error);
        throw error;
    }
}

// Load security results
async function loadSecurityResults(skillName) {
    try {
        const response = await fetch(`../test-results/${skillName}/security.json?v=${cacheBuster}`);
        if (!response.ok) return null;
        return await response.json();
    } catch (error) {
        return null;
    }
}

// Render skill header
function renderHeader(report) {
    document.getElementById('skillName').textContent = report.skill_name || 'Unknown';
    document.getElementById('totalScore').textContent = report.total || 0;
    const grade = report.grade || 'F';
    document.getElementById('grade').textContent = grade;
    document.getElementById('grade').className = `grade-badge grade-${grade.toLowerCase()}`;
    if (report.description) {
        const descElement = document.getElementById('skillDescription');
        if (descElement) {
            descElement.textContent = report.description;
            descElement.style.display = 'block';
        }
    }
}

// Render category breakdown
function renderCategory(categoryId, categoryData) {
    const container = document.getElementById(categoryId);
    const breakdown = categoryData.breakdown;
    let html = `<div class="category-header"><h3>${categoryId.charAt(0).toUpperCase() + categoryId.slice(1)}</h3><div class="category-score">${categoryData.score}/${categoryData.max}</div></div><div class="category-items">`;
    const skipKeys = ['function_count', 'organization_bonus', 'frontmatter_details', 'documentation_details', 'type_hints_details', 'error_handling_details', 'organization_details'];
    for (const [key, value] of Object.entries(breakdown)) {
        if (typeof value === 'number' && !skipKeys.includes(key)) {
            const maxValue = getMaxValue(categoryId, key);
            const displayValue = Math.min(value, maxValue);
            const status = displayValue === maxValue ? 'pass' : (displayValue > 0 ? 'partial' : 'fail');
            const icon = status === 'pass' ? '✓' : (status === 'partial' ? '◐' : '✗');
            const tooltip = getBreakdownTooltip(key, breakdown);
            const tooltipAttr = tooltip ? ` data-tooltip="${escapeHtml(tooltip)}"` : '';
            html += `<div class="breakdown-item status-${status}"${tooltipAttr}><span class="item-icon">${icon}</span><span class="item-label">${formatLabel(key)}</span><span class="item-score">${displayValue}/${maxValue}</span></div>`;
        }
    }
    html += `</div>`;
    container.innerHTML = html;
}

// Get tooltip text for breakdown items
function getBreakdownTooltip(key, breakdown) {
    if (key === 'valid_frontmatter' && breakdown.frontmatter_details) {
        if (breakdown.valid_frontmatter < 2) return breakdown.frontmatter_details;
        return null;
    }
    if (key === 'has_functions' && breakdown.function_count !== undefined) {
        if (breakdown.has_functions < 2) {
            const count = breakdown.function_count || 0;
            if (count === 0) return 'No callable functions found';
            if (count < 3) return `Only ${count} function(s) found (3+ recommended)`;
        }
        return null;
    }
    if (key === 'documentation' && breakdown.documentation_details) {
        if (breakdown.documentation < 4) {
            const details = breakdown.documentation_details;
            let issues = [];
            if (details.length < 2000) issues.push(`Only ${details.length} chars (need 2000+)`);
            if (details.missing_sections && details.missing_sections.length > 0) {
                issues.push('Missing: ' + details.missing_sections.join(', '));
            }
            return issues.length > 0 ? issues.join('\n') : null;
        }
        return null;
    }
    if (key === 'type_hints' && breakdown.type_hints_details) {
        if (breakdown.type_hints_details.without_hints && breakdown.type_hints_details.without_hints.length > 0) {
            return 'Missing hints: ' + breakdown.type_hints_details.without_hints.join(', ');
        }
        return null;
    }
    if (key === 'error_handling' && breakdown.error_handling_details) {
        if (breakdown.error_handling_details.without_handling && breakdown.error_handling_details.without_handling.length > 0) {
            return 'Missing: ' + breakdown.error_handling_details.without_handling.join(', ');
        }
        return null;
    }
    if (key === 'skill_md_exists' && breakdown.skill_md_exists < 3) return 'SKILL.md file incomplete or missing required sections';
    if (key === 'scripts_dir' && breakdown.scripts_dir < 3) return 'scripts/ directory incomplete or missing required files';
    if (key === 'importable' && breakdown.importable < 3) return 'Module import failed - check for missing dependencies';
    if (key === 'no_syntax_errors' && breakdown.no_syntax_errors < 3) return 'Syntax errors found in Python files';
    return null;
}

// Get maximum value for a breakdown item
function getMaxValue(category, key) {
    const maxValues = {
        structure: { skill_md_exists: 3, valid_frontmatter: 2, scripts_dir: 3, has_implementation: 2 },
        functionality: { no_syntax_errors: 3, importable: 3, has_functions: 2, has_docstrings: 2 },
        quality: { documentation: 4, examples: 2, type_hints: 2, error_handling: 2 },
        mcp_compare: { matched: 10, documented_only: 0, implemented_only: 10 }
    };
    return maxValues[category]?.[key] || 2;
}

// Format label
function formatLabel(label) {
    const specialCases = {
        'skill_md_exists': 'SKILL.md exists', 'valid_frontmatter': 'Valid frontmatter', 'scripts_dir': 'scripts/ directory',
        'has_implementation': 'Has implementation', 'no_syntax_errors': 'No syntax errors', 'importable': 'Modules importable',
        'has_functions': 'Has functions', 'has_docstrings': 'Has docstrings', 'documentation': 'Documentation',
        'examples': 'Code examples', 'type_hints': 'Type hints', 'error_handling': 'Error handling'
    };
    if (specialCases[label]) return specialCases[label];
    return label.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

// Render function analysis
function renderFunctionAnalysis(report) {
    const container = document.getElementById('functionAnalysis');
    if (!report.function_analysis) {
        container.innerHTML = `<div class="category-header"><h3>Functions</h3><div class="category-score">0/10</div></div><p class="no-items">No function analysis available</p>`;
        return;
    }
    const comparison = report.function_analysis.comparison;
    const functionality = report.scores?.functionality?.breakdown || {};

    // Count actual functions from comparison data
    const implementedCount = (comparison.matched || []).length;
    const stubCount = functionality.stub_count || 0;
    const notImplementedCount = stubCount > 0 ? (comparison.implemented_only || []).length : 0;

    // Calculate score: ((90 * ratio) + (ratio * 10)) / 10
    // Examples: 10/10 = (90*1 + 1*10)/10 = 10; 9/10 = (90*0.9 + 0.9*10)/10 = 9; 5/10 = (90*0.5 + 0.5*10)/10 = 5
    const totalFunctions = implementedCount + notImplementedCount;
    let score;
    if (totalFunctions > 0) {
        const ratio = implementedCount / totalFunctions;
        score = ((90 * ratio + ratio * 10) / 10).toFixed(1);
    } else {
        score = ((90 + 10) / 10).toFixed(1); // All implemented, no stubs: max 10.0
    }

    const funcDetailsMap = {};
    if (comparison.all_implemented) comparison.all_implemented.forEach(func => funcDetailsMap[func.name] = func);
    const createFuncItem = (funcName, className) => {
        const details = funcDetailsMap[funcName];
        if (details) {
            const tooltip = `${funcName}${details.signature || '()'}\n\n${details.file}:${details.line}`;
            return `<span class="${className}" title="${tooltip}">${funcName}</span>`;
        }
        return `<span class="${className}">${funcName}</span>`;
    };

    // Implemented functions
    let implementedHtml = '';
    if (comparison.matched && comparison.matched.length > 0) {
        implementedHtml = `<div class="func-list"><h4>✓ Implemented (${comparison.matched.length})</h4><div class="func-items">${comparison.matched.map(func => createFuncItem(func, 'func-matched')).join('')}</div></div>`;
    }

    // Not implemented (stubs)
    let notImplementedHtml = '';
    if (stubCount > 0 && comparison.implemented_only && comparison.implemented_only.length > 0) {
        notImplementedHtml = `<div class="func-list">
            <h4>Not Implemented (${stubCount})</h4>
            <div class="func-items">${comparison.implemented_only.map(func => createFuncItem(func, 'func-stub')).join('')}</div>
        </div>`;
    }

    const functionsHtml = `<div class="func-lists">${implementedHtml}${notImplementedHtml}</div>`;
    container.innerHTML = `<div class="category-header"><h3>Functions</h3><div class="category-score">${score}/10</div></div>${functionsHtml}`;
}

// Load integration test results
async function loadIntegrationResults(skillName) {
    try {
        const response = await fetch(`../test-results/${skillName}/integration.json?v=${cacheBuster}`);
        if (!response.ok) return null;
        return await response.json();
    } catch (error) {
        return null;
    }
}

// Render integration tests
function renderIntegrationTests(integration) {
    const container = document.getElementById('integrationTests');
    if (!container) return;
    if (!integration || !integration.categories || integration.categories.length === 0) {
        container.innerHTML = `<div class="category-header"><h3>Integration</h3><div class="category-score">0/30</div></div><p class="no-items">No integration tests available</p>`;
        return;
    }
    const score = integration.score || 0;
    let html = `<div class="category-header"><h3>Integration</h3><div class="category-score">${score}/30</div></div><div class="integration-summary"><div class="summary-stat"><span class="stat-value">${integration.tests.total}</span><span class="stat-label">Total Tests</span></div><div class="summary-stat"><span class="stat-value">${integration.tests.passed}</span><span class="stat-label">Passed</span></div><div class="summary-stat"><span class="stat-value">${integration.tests.failed}</span><span class="stat-label">Failed</span></div><div class="summary-stat"><span class="stat-value">${integration.elapsed_seconds}s</span><span class="stat-label">Duration</span></div></div><div class="test-categories">`;
    for (const category of integration.categories) {
        const statusClass = category.failed === 0 ? 'category-pass' : 'category-fail';
        html += `<div class="test-category ${statusClass}"><div class="category-title" onclick="this.parentElement.classList.toggle('expanded')"><span class="expand-icon">▶</span><span class="category-name">${category.name.replace(/^Test/, '').replace(/([A-Z])/g, ' $1').trim()}</span><span class="category-count">${category.passed}/${category.passed + category.failed}</span></div><div class="category-tests"><ul>`;
        for (const test of category.tests) {
            const icon = test.outcome === 'passed' ? '✓' : '✗';
            const testClass = test.outcome === 'passed' ? 'test-pass' : 'test-fail';
            // Build tooltip with method, snippet, and assertions
            let tooltip = '';
            if (test.method || test.snippet || test.assertions) {
                const parts = [];
                if (test.method) parts.push(`Method: ${test.method}`);
                if (test.snippet) parts.push(`Call: ${test.snippet}`);
                if (test.assertions && test.assertions.length > 0) {
                    parts.push(`Assertions:\n  ${test.assertions.join('\n  ')}`);
                }
                tooltip = parts.join('\n\n');
            }
            const tooltipAttr = tooltip ? ` data-tooltip="${escapeHtml(tooltip)}"` : '';
            html += `<li class="${testClass}"${tooltipAttr}><span class="test-icon">${icon}</span><span class="test-name">${test.name.replace(/^test_/, '').replace(/_/g, ' ')}</span><span class="test-duration">${test.duration}ms</span></li>`;
        }
        html += `</ul></div></div>`;
    }
    html += '</div>';
    container.innerHTML = html;
}

// Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML.replace(/"/g, '&quot;');
}

// Render security card
function renderSecurity(security) {
    const container = document.getElementById('security');
    if (!container) return;
    if (!security) {
        container.innerHTML = `<div class="category-header"><h3>Security</h3><div class="category-score">0/30</div></div><div class="category-items"><p class="no-items">No security scan results</p></div>`;
        return;
    }
    const score = security.score || 0;
    const findings = security.findings || {};
    const highScore = Math.max(0, 15 - ((findings.high || 0) * 15));
    const mediumScore = Math.max(0, 10 - ((findings.medium || 0) * 5));
    const lowScore = Math.max(0, 5 - ((findings.low || 0) * 1));
    const highTooltip = 'Critical vulnerabilities\nSQL injection, command injection,\nhardcoded secrets, etc.\n\n-15 pts per finding';
    const mediumTooltip = 'Potential security issues\nInsecure defaults, weak crypto,\nmissing input validation\n\n-5 pts per finding';
    const lowTooltip = 'Code quality concerns\nUnused variables, complexity,\nstyle issues\n\n-1 pt per finding';
    container.innerHTML = `<div class="category-header"><h3>Security</h3><div class="category-score">${score}/30</div></div><div class="category-items"><div class="breakdown-item ${highScore === 15 ? 'status-pass' : 'status-fail'}" data-tooltip="${highTooltip}"><span class="item-icon">${highScore === 15 ? '✓' : '✗'}</span><span class="item-label">No critical issues</span><span class="item-score">${highScore}/15</span></div><div class="breakdown-item ${mediumScore === 10 ? 'status-pass' : 'status-partial'}" data-tooltip="${mediumTooltip}"><span class="item-icon">${mediumScore === 10 ? '✓' : '◐'}</span><span class="item-label">No warnings</span><span class="item-score">${mediumScore}/10</span></div><div class="breakdown-item ${lowScore === 5 ? 'status-pass' : 'status-partial'}" data-tooltip="${lowTooltip}"><span class="item-icon">${lowScore === 5 ? '✓' : '◐'}</span><span class="item-label">No info issues</span><span class="item-score">${lowScore}/5</span></div></div>`;
}

// Main initialization
async function init() {
    const skillName = getSkillName();
    try {
        const report = await loadSkillReport(skillName);
        const security = await loadSecurityResults(skillName);
        const integration = await loadIntegrationResults(skillName);

        // Calculate Functions score using new formula
        let functionsScore = 10; // default if no function analysis
        if (report.function_analysis?.comparison) {
            const comparison = report.function_analysis.comparison;
            const functionality = report.scores?.functionality?.breakdown || {};
            const implementedCount = (comparison.matched || []).length;
            const stubCount = functionality.stub_count || 0;
            const notImplementedCount = stubCount > 0 ? (comparison.implemented_only || []).length : 0;
            const totalFunctions = implementedCount + notImplementedCount;

            if (totalFunctions > 0) {
                const ratio = implementedCount / totalFunctions;
                functionsScore = (90 * ratio + ratio * 10) / 10;
            } else {
                functionsScore = (90 + 10) / 10; // Max 10.0
            }
        }

        // Calculate component scores
        const structureScore = report.scores?.structure?.score || 0;
        const functionalityScore = report.scores?.functionality?.score || 0;
        const qualityScore = report.scores?.quality?.score || 0;
        const securityScore = security?.score || 0;
        const integrationScore = integration?.score || 0;

        // Overall = (sum of components) × (functions_score / 10)
        const componentSum = functionsScore + structureScore + functionalityScore + qualityScore + securityScore + integrationScore;
        const totalScore = componentSum * (functionsScore / 10);

        let grade = 'F';
        if (totalScore >= 90) grade = 'A';
        else if (totalScore >= 80) grade = 'B';
        else if (totalScore >= 70) grade = 'C';
        else if (totalScore >= 60) grade = 'D';
        report.total = totalScore.toFixed(1);
        report.grade = grade;
        renderHeader(report);
        renderFunctionAnalysis(report);
        renderCategory('structure', report.scores.structure);
        renderCategory('functionality', report.scores.functionality);
        renderCategory('quality', report.scores.quality);
        renderSecurity(security);
        renderIntegrationTests(integration);
    } catch (error) {
        console.error('Error loading skill report:', error);
        document.querySelector('main.container').innerHTML = `<div class="error-message"><h2>Error Loading Skill Report</h2><p>Could not load validation report for "${skillName}"</p><p style="font-size: 12px; color: #666;">Error: ${error.message}</p><a href="../index.html" class="btn">Back to Dashboard</a></div>`;
    }
}

// Run on page load
document.addEventListener('DOMContentLoaded', init);
