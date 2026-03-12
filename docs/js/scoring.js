/**
 * Shared scoring logic for the 3-layer skill scoring system.
 *
 * Layer 1: Safety Gate (binary pass/block)
 * Layer 2: Static Pre-flight (20 points)
 * Layer 3: Behavioral Eval (80 points)
 *
 * Every point is traceable to a specific check.
 */

function computeSafetyGate(securityJson) {
    if (!securityJson) {
        return { passed: true, highCount: 0, mediumCount: 0, lowCount: 0, findings: [], status: 'no data' };
    }
    const findings = securityJson.findings || {};
    const highCount = findings.high || 0;
    const mediumCount = findings.medium || 0;
    const lowCount = findings.low || 0;
    return {
        passed: highCount === 0,
        highCount,
        mediumCount,
        lowCount,
        findings: securityJson.details || [],
        status: highCount === 0 ? 'pass' : 'block'
    };
}

function computeStaticScore(basicJson) {
    if (!basicJson) {
        return { total: 0, breakdown: emptyStaticBreakdown() };
    }

    const structure = basicJson.scores?.structure?.breakdown || {};
    const functionality = basicJson.scores?.functionality?.breakdown || {};
    const quality = basicJson.scores?.quality?.breakdown || {};

    // Scripts parse & import (7 pts)
    const syntaxOk = (functionality.no_syntax_errors || 0) >= 3;
    const importOk = (functionality.importable || 0) >= 3;
    const syntaxPts = syntaxOk ? 4 : 0;
    const importPts = importOk ? 3 : 0;
    const scriptsPts = syntaxPts + importPts;

    // Structure exists (5 pts)
    const skillMdOk = (structure.skill_md_exists || 0) >= 2;
    const scriptsDirOk = (structure.scripts_dir || 0) >= 2;
    const skillMdPts = skillMdOk ? 3 : 0;
    const scriptsDirPts = scriptsDirOk ? 2 : 0;
    const structurePts = skillMdPts + scriptsDirPts;

    // Documentation & examples (3 pts)
    const examplesOk = (quality.examples || 0) >= 2;
    const docsOk = (quality.documentation || 0) >= 3;
    const examplesPts = examplesOk ? 2 : 0;
    const docsPts = docsOk ? 1 : 0;
    const docExPts = examplesPts + docsPts;

    // Code quality (5 pts)
    const typeHintsOk = (quality.type_hints || 0) >= 2;
    const errorHandlingOk = (quality.error_handling || 0) >= 2;
    const docstringsOk = (functionality.has_docstrings || 0) >= 2;
    const typeHintsPts = typeHintsOk ? 2 : 0;
    const errorHandlingPts = errorHandlingOk ? 2 : 0;
    const docstringsPts = docstringsOk ? 1 : 0;
    const qualityPts = typeHintsPts + errorHandlingPts + docstringsPts;

    const total = scriptsPts + structurePts + docExPts + qualityPts;

    return {
        total,
        breakdown: {
            scripts: {
                score: scriptsPts,
                max: 7,
                checks: [
                    { name: 'No syntax errors', passed: syntaxOk, points: syntaxPts, max: 4 },
                    { name: 'Modules importable', passed: importOk, points: importPts, max: 3 }
                ]
            },
            structure: {
                score: structurePts,
                max: 5,
                checks: [
                    { name: 'SKILL.md exists', passed: skillMdOk, points: skillMdPts, max: 3 },
                    { name: 'scripts/ directory', passed: scriptsDirOk, points: scriptsDirPts, max: 2 }
                ]
            },
            docs: {
                score: docExPts,
                max: 3,
                checks: [
                    { name: 'Code examples', passed: examplesOk, points: examplesPts, max: 2 },
                    { name: 'Documentation', passed: docsOk, points: docsPts, max: 1 }
                ]
            },
            quality: {
                score: qualityPts,
                max: 5,
                checks: [
                    { name: 'Type hints', passed: typeHintsOk, points: typeHintsPts, max: 2 },
                    { name: 'Error handling', passed: errorHandlingOk, points: errorHandlingPts, max: 2 },
                    { name: 'Docstrings', passed: docstringsOk, points: docstringsPts, max: 1 }
                ]
            }
        }
    };
}

function computeEvalScore(evalJson) {
    if (!evalJson) {
        return { total: 0, hasEval: false, delta: 0, prompts: [], withSkillRate: 0, baselineRate: 0, verdict: 'none' };
    }
    const summary = evalJson.summary || {};
    return {
        total: Math.min(summary.eval_score || 0, 80),
        hasEval: true,
        delta: summary.delta || 0,
        withSkillRate: summary.with_skill_pass_rate || 0,
        baselineRate: summary.baseline_pass_rate || 0,
        verdict: summary.verdict || 'unknown',
        prompts: evalJson.prompts || [],
        evalDate: evalJson.eval_date || null
    };
}

function computeTotalScore(safety, staticScore, evalScore) {
    if (!safety.passed) {
        return { total: 0, status: 'Blocked', hasEval: evalScore.hasEval };
    }
    const total = staticScore.total + evalScore.total;
    let status;
    if (!evalScore.hasEval) {
        status = 'Needs eval';
    } else if (total >= 70) {
        status = 'Ready';
    } else {
        status = 'Below threshold';
    }
    return { total, status, hasEval: evalScore.hasEval };
}

function getGrade(score, hasEval) {
    if (!hasEval) return '-';
    if (score >= 90) return 'A';
    if (score >= 80) return 'B';
    if (score >= 70) return 'C';
    if (score >= 60) return 'D';
    return 'F';
}

function emptyStaticBreakdown() {
    return {
        scripts: { score: 0, max: 7, checks: [] },
        structure: { score: 0, max: 5, checks: [] },
        docs: { score: 0, max: 3, checks: [] },
        quality: { score: 0, max: 5, checks: [] }
    };
}
