import re

class Node:
    def __init__(self, type, left=None, right=None, value=None):
        self.type = type
        self.left = left
        self.right = right
        self.value = value

    def to_dict(self):
        return {
            "type": self.type,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None,
            "value": self.value
        }

def create_rule(rule_string):
    tokens = tokenize(rule_string)
    return parse_tokens(tokens)

def tokenize(rule_string):
    pattern = r'\s*(=>|<=|>=|!=|=|>|<|AND|OR|\(|\)|\w+)\s*'
    return [token for token in re.split(pattern, rule_string) if token]

def parse_tokens(tokens):
    if not tokens:
        return None

    def parse_expression():
        token = tokens.pop(0)

        if token == '(':
            left = parse_expression()
            operator = tokens.pop(0)
            right = parse_expression()
            tokens.pop(0)  # pop the closing parenthesis
            return Node(type='operator', left=left, right=right, value=operator)
        elif token in ['AND', 'OR']:
            right = parse_expression()
            return Node(type='operator', left=None, right=right, value=token)
        else:
            attr = token
            op = tokens.pop(0)
            val = tokens.pop(0)
            return Node(type='operand', value=(attr, op, val))

    ast = parse_expression()

    while tokens:
        token = tokens.pop(0)
        if token in ['AND', 'OR']:
            right = parse_expression()
            ast = Node(type='operator', left=ast, right=right, value=token)

    return ast

def evaluate_rule(ast, data):
    def evaluate_node(node):
        if node.type == 'operand':
            var_name = node.value[0]
            comparison_op = node.value[1]
            expected_value = node.value[2].strip('"')

            actual_value = data.get(var_name)
            #print(f"Evaluating: {var_name} {comparison_op} {expected_value} (actual: {actual_value})")


            if actual_value is None:
                return False  # Handle missing values

            # Compare based on the operator
            if comparison_op == '=':
                return actual_value == expected_value
            elif comparison_op == '<':
                return actual_value < float(expected_value) if isinstance(actual_value, (int, float)) else False
            elif comparison_op == '>':
                return actual_value > float(expected_value) if isinstance(actual_value, (int, float)) else False
            elif comparison_op == '!=':
                return actual_value != expected_value
            elif comparison_op == '<=':
                return actual_value <= float(expected_value) if isinstance(actual_value, (int, float)) else False
            elif comparison_op == '>=':
                return actual_value >= float(expected_value) if isinstance(actual_value, (int, float)) else False

        elif node.type == 'operator':
            left_result = evaluate_node(node.left)
            right_result = evaluate_node(node.right)
            operator = node.value

            if operator == 'AND':
                return left_result and right_result
            elif operator == 'OR':
                return left_result or right_result

        return False

    return evaluate_node(ast)

def combine_rules(rule_strings):
    combined_ast = None
    for rule_string in rule_strings:
        ast = create_rule(rule_string)
        #print(f"Combining AST for rule: {rule_string} -> {ast.to_dict()}")
        combined_ast = ast if combined_ast is None else Node(type='operator', left=combined_ast, right=ast, value='AND')
    return combined_ast

def dict_to_node(node_dict):
    if node_dict is None:
        return None
    node = Node(type=node_dict['type'], value=node_dict.get('value'))
    node.left = dict_to_node(node_dict.get('left'))
    node.right = dict_to_node(node_dict.get('right'))
    return node
