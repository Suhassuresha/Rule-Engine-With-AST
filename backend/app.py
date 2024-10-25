from flask import Flask, jsonify, request, render_template
from ast_processor import create_rule, evaluate_rule, combine_rules, dict_to_node
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,
            template_folder='../frontend/templates', 
            static_folder='../frontend/static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rules.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rule_string = db.Column(db.String, nullable=False)
    ast_json = db.Column(db.JSON, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_rule', methods=['POST'])
def create_rule_endpoint():
    data = request.get_json()
    
    if not data or 'rule_string' not in data:
        return jsonify({"error": "Missing rule_string in request"}), 400

    rule_string = data['rule_string']
    
    try:
        ast = create_rule(rule_string)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    new_rule = Rule(rule_string=rule_string, ast_json=ast.to_dict())
    db.session.add(new_rule)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "success", "ast": ast.to_dict(), "id": new_rule.id})

@app.route('/combine_rules', methods=['POST'])
def combine_rules_endpoint():
    global combinedAST  
    rule_ids = request.json.get('rules')

    if not rule_ids or len(rule_ids) < 2:
        return jsonify({"error": "Please provide at least two unique rule IDs"}), 400

    # Ensure unique rule IDs
    unique_rule_ids = list(set(rule_ids))
    rules = Rule.query.filter(Rule.id.in_(unique_rule_ids)).all()
    
    if len(rules) != len(unique_rule_ids):
        return jsonify({"error": "Some rule IDs are not found"}), 404

    rule_strings = [rule.rule_string for rule in rules]

    # Combine the rules and get the AST
    combinedAST = combine_rules(rule_strings)
    return jsonify({"ast": combinedAST.to_dict()})

@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_endpoint():
    global combinedAST
    data = request.json
    input_data = data.get('data')

    if not isinstance(input_data, dict):
        return jsonify({"error": "Invalid input, data must be a dictionary"}), 400
    
    if combinedAST is None:
        return jsonify({"error": "Combined AST is not defined. Please combine rules first."}), 400

    try:
        combinedASTNode = dict_to_node(combinedAST.to_dict())
        result = evaluate_rule(combinedASTNode, input_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"result": result})

@app.route('/favicon.ico')
def favicon():
    return '', 204  # No content

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, threaded=True)
