from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
FILE_NAME = "voters.txt"

def load_voters():
    voters = []
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            for line in f:
                parts = line.strip().split(" ", 1)
                if len(parts) == 2:
                    voters.append({"id": int(parts[0]), "name": parts[1]})
    return voters

def save_voters(voters):
    with open(FILE_NAME, "w") as f:
        for v in voters:
            f.write(f"{v['id']} {v['name']}\n")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/voters', methods=['GET', 'POST'])
def handle_voters():
    voters = load_voters()
    if request.method == 'POST':
        new_voter = request.json
        # Duplicate check
        if any(v['id'] == int(new_voter['id']) for v in voters):
            return jsonify({"message": "Duplicate ID!"}), 400
        
        voters.append({"id": int(new_voter['id']), "name": new_voter['name']})
        save_voters(voters)
        return jsonify({"message": "Registered!"})
    
    # If sorting is requested
    if request.args.get('sort') == 'true':
        voters.sort(key=lambda x: x['id'])
    
    return jsonify(voters)

if __name__ == '__main__':
    app.run(debug=True, port=5000)