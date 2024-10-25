let combinedAST = null; // Variable to store the combined AST

document.addEventListener('DOMContentLoaded', () => {
    const createRuleBtn = document.getElementById('create-rule');
    const evaluateRuleBtn = document.getElementById('evaluate-rule');
    const combineRulesBtn = document.getElementById('combine-rules-btn');

    createRuleBtn.addEventListener('click', createRule);
    evaluateRuleBtn.addEventListener('click', evaluateRule);
    combineRulesBtn.addEventListener('click', combineRules);
});

async function createRule() {
    const ruleString = document.getElementById('rule-input').value;
    if (!ruleString) {
        alert('Please enter a rule string.');
        return;
    }

    try {
        const response = await fetch('/create_rule', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ rule_string: ruleString })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.json();
        document.getElementById('rule-result').innerText = JSON.stringify(result, null, 2);
    } catch (error) {
        console.error('Error creating rule:', error);
        document.getElementById('rule-result').innerText = 'Error creating rule. Please check the console for details.';
    }
}

async function evaluateRule() {
    const inputData = document.getElementById('input-data').value;
    const combinedAST = document.getElementById('combined-rule-data').value; // Get combined AST data

    if (!inputData || !combinedAST) {
        alert('Please provide both input data and combined rule data.');
        return;
    }

    try {
        const response = await fetch('/evaluate_rule', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                data: JSON.parse(inputData), // Ensure input data is in the correct format
                combinedAST: JSON.parse(combinedAST) // Use the combined AST for evaluation
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.json();
        document.getElementById('evaluation-result').innerText = JSON.stringify(result, null, 2);
    } catch (error) {
        console.error('Error evaluating rule:', error);
        document.getElementById('evaluation-result').innerText = 'Error evaluating rule. Please check the console for details.';
    }
}

async function combineRules() {
    const ruleIds = document.getElementById('rule-ids').value.split(',').map(id => id.trim());
    if (ruleIds.length === 0) {
        alert('Please provide rule IDs to combine.');
        return;
    }

    try {
        const response = await fetch('/combine_rules', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ rules: ruleIds })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.json();
        document.getElementById('combine-result').innerText = JSON.stringify(result.ast, null, 2);
        
        // Update the combined rule data textarea
        document.getElementById('combined-rule-data').value = JSON.stringify(result.ast, null, 2); // Populate combined AST here

    } catch (error) {
        console.error('Error combining rules:', error);
        document.getElementById('combine-result').innerText = 'Error combining rules. Please check the console for details.';
    }
}
