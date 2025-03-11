from flask import Flask, render_template, request, jsonify
import csv
import os

app = Flask(__name__, template_folder='templates')
log_file = "game_log.csv"
moves_file = "moves_log.csv"

# Ensure CSV files exist with headers
for file, headers in [(log_file, ["Team 1", "Team 2", "Winner"]), (moves_file, ["Player", "Row", "Column", "Move"])]:
    if not os.path.exists(file):
        with open(file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/declare_winner', methods=['POST'])
def declare_winner():
    data = request.json
    team1 = data.get("team1")
    team2 = data.get("team2")
    winner = data.get("winner")

    # Debugging: Log the received data
    print(f"Received data: Team 1 = {team1}, Team 2 = {team2}, Winner = {winner}")

    # Log the winner
    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([team1, team2, winner])

    # Clear the moves log
    with open(moves_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Player", "Row", "Column", "Move"])  # Rewriting header

    return jsonify({"success": True, "message": f"Winner {winner} logged. Game log cleared."})


@app.route('/log_move', methods=['POST'])
def log_move():
    data = request.json
    player = data.get("player")
    row = data.get("row")
    column = data.get("column")
    move = data.get("move")

    with open(moves_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([player, row, column, move])

    return jsonify({"success": True})


@app.route('/get_moves', methods=['GET'])
def get_moves():
    moves = []
    if os.path.exists(moves_file):
        with open(moves_file, "r") as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            moves = [row for row in reader]
    return jsonify(moves)


@app.route('/clear_logs', methods=['POST'])
def clear_logs():
    # Clear the moves log file
    with open(moves_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Player", "Row", "Column", "Move"])  # Rewrite headers

    return jsonify({"success": True, "message": "Game log cleared successfully."})


if __name__ == '__main__':
    app.run(debug=True)