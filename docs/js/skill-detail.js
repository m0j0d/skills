/**
 * Skill detail page — renders 3-layer scoring breakdown.
 */

const cacheBuster = Date.now();

function getSkillName() {
    const params = new URLSearchParams(window.location.search);
    return params.get('skill') || '';
}

async function fetchJson(url) {
    try {
        const response = await fetch(`${url}?v=${cacheBuster}`);
        if (!response.ok) return null;
        return await response.json();
    } catch (e) {
        return null;
    }
}

function esc(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// --- Render functions ---

function renderHeader(skillName, description, total, hasEval, status) {
    document.getElementById('skillName').textContent = skillName;
    document.getElementById('totalScore').textContent = total;
    if (description) {
        const descEl = document.getElementById('skillDescription');
        descEl.textContent = description;
        descEl.style.display = 'block';
    }
    const statusLine = document.getElementById('statusLine');
    let badge;
    if (status === 'Blocked') {
        badge = '<span class="status-badge status-blocked">Blocked</span>';
    } else if (status === 'Needs eval') {
        badge = '<span class="status-badge status-needs-eval">Needs eval</span>';
    } else if (status === 'Ready') {
        badge = '<span class="status-badge status-ready">Ready</span>';
    } else {
        badge = `<span class="status-badge status-below">${esc(status)}</span>`;
    }
    statusLine.innerHTML = badge;
}

function renderSafetyCard(safety) {
    const card = document.getElementById('safetyCard');
    const badge = safety.passed
        ? '<span class="safety-badge safety-pass">Pass</span>'
        : '<span class="safety-badge safety-block">Block</span>';

    let findingsHtml = '';
    if (safety.findings && safety.findings.length > 0) {
        const items = safety.findings.map(f => {
            const severity = f.severity || 'unknown';
            return `<li class="finding-item finding-${severity}"><span class="finding-severity">${severity.toUpperCase()}</span> <span class="finding-text">${esc(f.message || f.description || JSON.stringify(f))}</span></li>`;
        }).join('');
        findingsHtml = `<ul class="findings-list">${items}</ul>`;
    }

    const countsHtml = `<div class="safety-counts">
        <span>High: ${safety.highCount}</span>
        <span>Medium: ${safety.mediumCount}</span>
        <span>Low: ${safety.lowCount}</span>
    </div>`;

    card.innerHTML = `
        <div class="category-header">
            <h3>Safety Gate</h3>
            ${badge}
        </div>
        <div class="category-items">
            ${safety.passed
                ? '<div class="breakdown-item status-pass"><span class="item-icon">&#10003;</span><span class="item-label">No high-severity findings</span></div>'
                : '<div class="breakdown-item status-fail"><span class="item-icon">&#10007;</span><span class="item-label">High-severity findings detected</span></div>'
            }
            ${countsHtml}
            ${findingsHtml}
        </div>`;
}

function renderStaticCard(staticScore) {
    const card = document.getElementById('staticCard');
    const b = staticScore.breakdown;

    function renderGroup(label, group) {
        const checksHtml = group.checks.map(c => {
            const status = c.passed ? 'status-pass' : 'status-fail';
            const icon = c.passed ? '&#10003;' : '&#10007;';
            return `<div class="breakdown-item ${status}">
                <span class="item-icon">${icon}</span>
                <span class="item-label">${esc(c.name)}</span>
                <span class="item-score">${c.points}/${c.max}</span>
            </div>`;
        }).join('');

        return `<div class="static-group">
            <div class="group-header">
                <span class="group-label">${esc(label)}</span>
                <span class="group-score">${group.score}/${group.max}</span>
            </div>
            ${checksHtml}
        </div>`;
    }

    card.innerHTML = `
        <div class="category-header">
            <h3>Static Pre-flight</h3>
            <div class="category-score">${staticScore.total}/20</div>
        </div>
        <div class="category-items">
            ${renderGroup('Scripts parse & import', b.scripts)}
            ${renderGroup('Structure exists', b.structure)}
            ${renderGroup('Documentation & examples', b.docs)}
            ${renderGroup('Code quality', b.quality)}
        </div>`;
}

function renderEvalCard(evalScore) {
    const card = document.getElementById('evalCard');

    if (!evalScore.hasEval) {
        card.innerHTML = `
            <div class="category-header">
                <h3>Behavioral Eval</h3>
                <div class="category-score needs-eval-score">--/80</div>
            </div>
            <div class="no-eval-content">
                <p class="no-eval-message">No behavioral eval yet.</p>
                <p class="no-eval-explain">Run A/B eval: spawn with-skill + baseline agents, grade against assertions. Score = (with_skill - baseline) pass rate x 80.</p>
                <details class="eval-schema">
                    <summary>eval.json schema</summary>
                    <pre class="schema-pre">{
  "skill_name": "example",
  "eval_date": "2026-03-11",
  "prompts": [{
    "prompt": "Task description...",
    "assertions": ["Uses X tool", "Handles Y"],
    "with_skill": {
      "plan": "Agent plan text...",
      "assertions_passed": [true, true]
    },
    "baseline": {
      "plan": "Agent plan text...",
      "assertions_passed": [false, false]
    }
  }],
  "summary": {
    "with_skill_pass_rate": 1.0,
    "baseline_pass_rate": 0.0,
    "delta": 1.0,
    "eval_score": 80,
    "verdict": "PASS"
  }
}</pre>
                </details>
            </div>`;
        return;
    }

    // Render eval summary
    const deltaPercent = (evalScore.delta * 100).toFixed(0);
    const withPercent = (evalScore.withSkillRate * 100).toFixed(0);
    const basePercent = (evalScore.baselineRate * 100).toFixed(0);

    const verdictClass = evalScore.verdict === 'PASS' ? 'verdict-pass'
        : evalScore.verdict === 'FAIL' ? 'verdict-fail' : 'verdict-marginal';

    let promptsHtml = '';
    if (evalScore.prompts && evalScore.prompts.length > 0) {
        promptsHtml = evalScore.prompts.map((p, i) => {
            const assertionsHtml = (p.assertions || []).map((a, j) => {
                const withPassed = p.with_skill?.assertions_passed?.[j];
                const basePassed = p.baseline?.assertions_passed?.[j];
                const withIcon = withPassed ? '&#10003;' : '&#10007;';
                const baseIcon = basePassed ? '&#10003;' : '&#10007;';
                const withClass = withPassed ? 'assert-pass' : 'assert-fail';
                const baseClass = basePassed ? 'assert-pass' : 'assert-fail';
                return `<tr class="assertion-row">
                    <td class="assertion-text">${esc(a)}</td>
                    <td class="${withClass}">${withIcon}</td>
                    <td class="${baseClass}">${baseIcon}</td>
                </tr>`;
            }).join('');

            return `<div class="eval-prompt">
                <div class="prompt-header" onclick="this.parentElement.classList.toggle('expanded')">
                    <span class="expand-icon">&#9654;</span>
                    <span class="prompt-label">Prompt ${i + 1}</span>
                    <span class="prompt-text-preview">${esc(p.prompt?.substring(0, 80) || '')}${(p.prompt?.length || 0) > 80 ? '...' : ''}</span>
                </div>
                <div class="prompt-detail">
                    <div class="prompt-full">${esc(p.prompt || '')}</div>
                    <div class="comparison-grid">
                        <div class="comparison-col">
                            <h4>With Skill</h4>
                            <pre class="plan-text">${esc(p.with_skill?.plan || 'No plan recorded')}</pre>
                        </div>
                        <div class="comparison-col">
                            <h4>Baseline</h4>
                            <pre class="plan-text">${esc(p.baseline?.plan || 'No plan recorded')}</pre>
                        </div>
                    </div>
                    <table class="assertions-table">
                        <thead>
                            <tr><th>Assertion</th><th>With</th><th>Base</th></tr>
                        </thead>
                        <tbody>${assertionsHtml}</tbody>
                    </table>
                </div>
            </div>`;
        }).join('');
    }

    card.innerHTML = `
        <div class="category-header">
            <h3>Behavioral Eval</h3>
            <div class="category-score">${evalScore.total}/80</div>
        </div>
        <div class="eval-summary">
            <div class="eval-stat">
                <span class="eval-stat-value">${withPercent}%</span>
                <span class="eval-stat-label">With skill</span>
            </div>
            <div class="eval-stat">
                <span class="eval-stat-value">${basePercent}%</span>
                <span class="eval-stat-label">Baseline</span>
            </div>
            <div class="eval-stat">
                <span class="eval-stat-value">+${deltaPercent}%</span>
                <span class="eval-stat-label">Delta</span>
            </div>
            <div class="eval-stat">
                <span class="eval-stat-value ${verdictClass}">${esc(evalScore.verdict)}</span>
                <span class="eval-stat-label">Verdict</span>
            </div>
        </div>
        ${evalScore.evalDate ? `<div class="eval-date">Evaluated: ${esc(evalScore.evalDate)}</div>` : ''}
        <div class="eval-prompts">${promptsHtml}</div>`;
}

function renderApiCard(basicJson) {
    const card = document.getElementById('apiCard');
    const fa = basicJson?.function_analysis;

    if (!fa || !fa.comparison?.all_implemented?.length) {
        card.innerHTML = `
            <div class="category-header">
                <h3>API Reference</h3>
            </div>
            <div class="category-items">
                <p class="text-muted">No function data available.</p>
            </div>`;
        return;
    }

    const fns = fa.comparison.all_implemented
        .filter(f => !f.is_private)
        .sort((a, b) => a.name.localeCompare(b.name));

    const matched = new Set(fa.comparison.matched || []);
    const docOnly = new Set(fa.comparison.documented_only || []);

    const fnRows = fns.map(f => {
        const inDocs = matched.has(f.name) || docOnly.has(f.name);
        const docIcon = inDocs ? '&#10003;' : '';
        const cls = f.class_name ? `<span class="fn-class">${esc(f.class_name)}.</span>` : '';
        const sig = f.signature ? `<code class="fn-sig">(${esc(f.signature.replace(/^\(/, '').replace(/\)$/, ''))})</code>` : '';

        return `<div class="api-fn">
            <div class="fn-name-row">
                ${cls}<span class="fn-name">${esc(f.name)}</span>${sig}
            </div>
            <div class="fn-meta">
                <span class="fn-file">${esc(f.file)}:${f.line}</span>
                ${f.has_docstring ? '<span class="fn-tag fn-tag-doc">docstring</span>' : ''}
                ${inDocs ? '<span class="fn-tag fn-tag-matched">documented</span>' : '<span class="fn-tag fn-tag-undoc">undocumented</span>'}
            </div>
        </div>`;
    }).join('');

    const docFnCount = fa.documented_functions?.length || fa.comparison.documented_count || 0;
    const implCount = fns.length;

    card.innerHTML = `
        <div class="category-header">
            <h3>API Reference</h3>
            <div class="category-score">${docFnCount} documented / ${implCount} public</div>
        </div>
        <div class="category-items api-list">
            ${fnRows}
        </div>`;
}

// --- Main ---

async function init() {
    const skillName = getSkillName();
    if (!skillName) {
        document.querySelector('main.container').innerHTML =
            '<div class="error-message"><h2>No skill specified</h2><a href="../index.html" class="btn">Back to Dashboard</a></div>';
        return;
    }

    try {
        // Load skill description from manifest
        const skillsResponse = await fetch(`../data/skills.json?v=${cacheBuster}`);
        const skills = await skillsResponse.json();
        const skillInfo = skills.find(s => s.name === skillName);

        // Load all data in parallel
        const [basic, security, evalData] = await Promise.all([
            fetchJson(`../test-results/${skillName}/basic.json`),
            fetchJson(`../test-results/${skillName}/security.json`),
            fetchJson(`../test-results/${skillName}/eval.json`)
        ]);

        const safety = computeSafetyGate(security);
        const staticScore = computeStaticScore(basic);
        const evalScore = computeEvalScore(evalData);
        const total = computeTotalScore(safety, staticScore, evalScore);

        renderHeader(skillName, skillInfo?.description, total.total, total.hasEval, total.status);
        renderSafetyCard(safety);
        renderStaticCard(staticScore);
        renderEvalCard(evalScore);
        renderApiCard(basic);

    } catch (error) {
        console.error('Error:', error);
        document.querySelector('main.container').innerHTML =
            `<div class="error-message"><h2>Error Loading Skill</h2><p>${esc(error.message)}</p><a href="../index.html" class="btn">Back to Dashboard</a></div>`;
    }
}

document.addEventListener('DOMContentLoaded', init);
