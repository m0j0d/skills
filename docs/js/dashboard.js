/**
 * Dashboard — loads skill data, computes scores, renders table.
 */

const cacheBuster = Date.now();

async function fetchJson(url) {
    try {
        const response = await fetch(`${url}?v=${cacheBuster}`);
        if (!response.ok) return null;
        return await response.json();
    } catch (e) {
        return null;
    }
}

async function loadSkillScores() {
    const skillsResponse = await fetch(`data/skills.json?v=${cacheBuster}`);
    const skills = await skillsResponse.json();

    const results = await Promise.all(skills.map(async (skill) => {
        const [basic, security, evalData] = await Promise.all([
            fetchJson(`test-results/${skill.name}/basic.json`),
            fetchJson(`test-results/${skill.name}/security.json`),
            fetchJson(`test-results/${skill.name}/eval.json`)
        ]);

        const safety = computeSafetyGate(security);
        const staticScore = computeStaticScore(basic);
        const evalScore = computeEvalScore(evalData);
        const total = computeTotalScore(safety, staticScore, evalScore);

        return {
            name: skill.name,
            description: skill.description,
            safety,
            static: staticScore,
            eval: evalScore,
            total: total.total,
            status: total.status,
            hasEval: total.hasEval
        };
    }));

    results.sort((a, b) => b.total - a.total);
    return results;
}

function renderTable(results) {
    const tbody = document.getElementById('skillTableBody');

    const rows = results.map(r => {
        const safetyBadge = r.safety.passed
            ? '<span class="safety-badge safety-pass">Pass</span>'
            : '<span class="safety-badge safety-block">Block</span>';

        let statusBadge;
        if (r.status === 'Blocked') {
            statusBadge = '<span class="status-badge status-blocked">Blocked</span>';
        } else if (r.status === 'Needs eval') {
            statusBadge = '<span class="status-badge status-needs-eval">Needs eval</span>';
        } else if (r.status === 'Ready') {
            statusBadge = '<span class="status-badge status-ready">Ready</span>';
        } else {
            statusBadge = `<span class="status-badge status-below">${r.status}</span>`;
        }

        const evalDisplay = r.hasEval
            ? `${r.eval.total}/80`
            : '<span class="text-muted">--</span>';

        return `<tr>
            <td><a href="skills/detail.html?skill=${r.name}" class="skill-name">${r.name}</a></td>
            <td class="desc-cell">${r.description}</td>
            <td><span class="score-badge">${r.total}</span></td>
            <td>${safetyBadge}</td>
            <td class="score-fraction">${r.static.total}/20</td>
            <td class="score-fraction">${evalDisplay}</td>
            <td>${statusBadge}</td>
        </tr>`;
    }).join('');

    tbody.innerHTML = rows;

    // Update subtitle
    const avgScore = results.length > 0
        ? (results.reduce((sum, r) => sum + r.total, 0) / results.length).toFixed(1)
        : 0;
    const evalCount = results.filter(r => r.hasEval).length;
    document.getElementById('subtitle').textContent =
        `${results.length} skills \u2022 Average: ${avgScore}/100 \u2022 ${evalCount}/${results.length} eval'd`;
}

document.addEventListener('DOMContentLoaded', async () => {
    try {
        const results = await loadSkillScores();
        renderTable(results);
    } catch (error) {
        console.error('Failed to load dashboard:', error);
        document.getElementById('skillTableBody').innerHTML =
            '<tr><td colspan="7" class="loading">Failed to load skill data</td></tr>';
    }
});
