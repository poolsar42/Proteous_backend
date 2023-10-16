from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
df = pd.read_csv('data.csv')  # Assuming data.csv is your CSV file


@app.route('/all-entries', methods=['GET'])
def all_entries():
    return df.head().to_json(orient='records')


@app.route('/substring-search', methods=['GET'])
def substring_search():
    substring = request.args.get('substring')
    if substring:
        result = df[df['name'].str.startswith(substring)]
        return result.to_json(orient='records')
    return jsonify([])


if __name__ == '__main__':
    app.run(debug=True)
