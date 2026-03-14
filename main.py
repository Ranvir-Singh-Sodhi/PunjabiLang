import sys
from src.lexer import tokenize
from src.parser import Parser
from src.evaluator import Evaluator
from src.environment import Environment

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <filename.pj>")
        return

    filename = sys.argv[1]
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' nahi labhi.")
        return

    try:
        print(f"--- Running {filename} ---\n")
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        
        global_env = Environment()
        evaluator = Evaluator(global_env)
        evaluator.evaluate(ast)
        print("\n--- Execution Finished ---")
    except Exception as e:
        print(f"\n[Error] {str(e)}")

if __name__ == "__main__":
    main()