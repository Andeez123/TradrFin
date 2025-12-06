#!/usr/bin/env python3
"""
Market Analysis Web Interface - Method B Testing

A simple Flask web application that demonstrates how end users can
interact with the Market Analysis Agent through a web interface.

Run with: python web_interface.py
Then visit: http://localhost:5000
"""

from flask import Flask, request, jsonify, render_template_string
import json
import subprocess
import os
import tempfile

app = Flask(__name__)

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Market Analysis Agent</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #34495e;
        }
        input, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            box-sizing: border-box;
        }
        input:focus, select:focus {
            border-color: #3498db;
            outline: none;
        }
        .checkbox-group {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        .checkbox-item {
            display: flex;
            align-items: center;
            background: #f8f9fa;
            padding: 8px 12px;
            border-radius: 5px;
            border: 1px solid #dee2e6;
        }
        .checkbox-item input[type="checkbox"] {
            margin-right: 8px;
        }
        button {
            background: #3498db;
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 5px;
            font-size: 18px;
            cursor: pointer;
            width: 100%;
            transition: background 0.3s;
        }
        button:hover {
            background: #2980b9;
        }
        button:disabled {
            background: #95a5a6;
            cursor: not-allowed;
        }
        .loading {
            display: none;
            text-align: center;
            margin-top: 20px;
        }
        .loading.show {
            display: block;
        }
        .results {
            margin-top: 30px;
            display: none;
        }
        .results.show {
            display: block;
        }
        .symbol-card {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .symbol-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .symbol-name {
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
        }
        .confidence-badge {
            padding: 5px 10px;
            border-radius: 15px;
            color: white;
            font-weight: bold;
        }
        .confidence-high { background: #27ae60; }
        .confidence-medium { background: #f39c12; }
        .confidence-low { background: #e74c3c; }
        .price-display {
            font-size: 18px;
            color: #27ae60;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .summary {
            background: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 15px;
            line-height: 1.6;
        }
        .indicators {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 15px;
        }
        .indicator {
            background: white;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #bdc3c7;
        }
        .indicator-name {
            font-weight: bold;
            color: #34495e;
            margin-bottom: 5px;
        }
        .indicator-value {
            font-size: 16px;
            color: #2c3e50;
        }
        .guidance {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 15px;
            border-radius: 5px;
            font-weight: bold;
        }
        .error {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Market Analysis Agent</h1>

        <form id="analysisForm">
            <div class="form-group">
                <label for="symbols">Select Stocks to Analyze:</label>
                <div class="checkbox-group" id="symbolsList">
                    <div class="checkbox-item">
                        <input type="checkbox" id="NVDA" value="NVDA">
                        <label for="NVDA">NVDA (NVIDIA)</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="AAPL" value="AAPL">
                        <label for="AAPL">AAPL (Apple)</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="TSLA" value="TSLA">
                        <label for="TSLA">TSLA (Tesla)</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="MSFT" value="MSFT">
                        <label for="MSFT">MSFT (Microsoft)</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="GOOGL" value="GOOGL">
                        <label for="GOOGL">GOOGL (Google)</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="AMZN" value="AMZN">
                        <label for="AMZN">AMZN (Amazon)</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="BEAM" value="BEAM">
                        <label for="BEAM">BEAM (Beam Therapeutics)</label>
                    </div>
                </div>
            </div>

            <div class="form-group">
                <label for="dataType">Analysis Type:</label>
                <select id="dataType" name="data_type">
                    <option value="historical">Historical Data (Technical Analysis)</option>
                    <option value="quote">Current Price Only</option>
                </select>
            </div>

            <div class="form-group" id="timeframeGroup">
                <label for="timeRange">Time Range:</label>
                <select id="timeRange" name="range">
                    <option value="1mo">1 Month</option>
                    <option value="3mo">3 Months</option>
                    <option value="6mo">6 Months</option>
                    <option value="1y">1 Year</option>
                </select>
            </div>

            <div class="form-group" id="intervalGroup">
                <label for="interval">Time Interval:</label>
                <select id="interval" name="interval">
                    <option value="1d">Daily</option>
                    <option value="1h">Hourly</option>
                    <option value="5m">5 Minutes</option>
                </select>
            </div>

            <button type="submit" id="analyzeBtn">🚀 Analyze Stocks</button>
        </form>

        <div class="loading" id="loading">
            <h3>🔍 Analyzing stocks... This may take a moment.</h3>
            <p>Please wait while we fetch market data and generate AI-powered insights.</p>
        </div>

        <div class="results" id="results">
            <!-- Results will be inserted here -->
        </div>
    </div>

    <script>
        document.getElementById('analysisForm').addEventListener('submit', async function(e) {
            e.preventDefault();

            // Get selected symbols
            const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
            const symbols = Array.from(checkboxes).map(cb => cb.value);

            if (symbols.length === 0) {
                alert('Please select at least one stock to analyze.');
                return;
            }

            // Show loading
            document.getElementById('loading').classList.add('show');
            document.getElementById('results').classList.remove('show');
            document.getElementById('analyzeBtn').disabled = true;
            document.getElementById('analyzeBtn').textContent = 'Analyzing...';

            try {
                // Prepare request data
                const formData = new FormData(e.target);
                const requestData = {
                    symbols: symbols,
                    data_type: formData.get('data_type'),
                    interval: formData.get('interval'),
                    range: formData.get('range')
                };

                // Make API call
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(requestData)
                });

                const data = await response.json();

                if (data.success) {
                    // Save results to output.json
                    fetch('/api/save_results', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(data)
                    }).then(() => {
                        displayResults(data);
                    }).catch(() => {
                        // Continue displaying results even if save fails
                        displayResults(data);
                    });
                } else {
                    showError(data.error || 'Analysis failed');
                }

            } catch (error) {
                showError('Network error: ' + error.message);
            } finally {
                // Hide loading
                document.getElementById('loading').classList.remove('show');
                document.getElementById('analyzeBtn').disabled = false;
                document.getElementById('analyzeBtn').textContent = '🚀 Analyze Stocks';
            }
        });

        function displayResults(data) {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '<h2>📈 Analysis Results</h2>';

            if (data.results) {
                // Multiple symbols
                data.results.forEach(result => {
                    resultsDiv.innerHTML += createSymbolCard(result);
                });
            } else {
                // Single symbol
                resultsDiv.innerHTML += createSymbolCard(data);
            }

            resultsDiv.classList.add('show');
        }

        function createSymbolCard(result) {
            const confidence = result.llm_analysis.overall_confidence;
            const confidenceClass = confidence >= 0.8 ? 'high' :
                                   confidence >= 0.6 ? 'medium' : 'low';

            return `
                <div class="symbol-card">
                    <div class="symbol-header">
                        <div class="symbol-name">${result.symbol}</div>
                        <div class="confidence-badge confidence-${confidenceClass}">
                            ${(confidence * 100).toFixed(0)}% Confidence
                        </div>
                    </div>

                    <div class="price-display">
                        Current Price: $${result.price.toFixed(2)}
                    </div>

                    <div class="summary">
                        <strong>AI Summary:</strong> ${result.summary}
                    </div>

                    <div class="indicators">
                        <div class="indicator">
                            <div class="indicator-name">RSI</div>
                            <div class="indicator-value">${result.indicators.rsi ? result.indicators.rsi.toFixed(1) : 'N/A'}</div>
                        </div>
                        <div class="indicator">
                            <div class="indicator-name">SMA 20</div>
                            <div class="indicator-value">${result.indicators.sma20 ? result.indicators.sma20.toFixed(2) : 'N/A'}</div>
                        </div>
                        <div class="indicator">
                            <div class="indicator-name">Volatility</div>
                            <div class="indicator-value">${result.indicators.volatility ? (result.indicators.volatility).toFixed(2) + '%' : 'N/A'}</div>
                        </div>
                        <div class="indicator">
                            <div class="indicator-name">Momentum</div>
                            <div class="indicator-value">${result.indicators.momentum ? result.indicators.momentum.toFixed(2) : 'N/A'}</div>
                        </div>
                    </div>

                    <div class="guidance">
                        🎯 <strong>Actionable Guidance:</strong> ${result.llm_analysis.actionable_guidance}
                    </div>
                </div>
            `;
        }

        function showError(message) {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = `<div class="error">❌ Error: ${message}</div>`;
            resultsDiv.classList.add('show');
        }

        // Handle data type change
        document.getElementById('dataType').addEventListener('change', function(e) {
            const timeframeGroup = document.getElementById('timeframeGroup');
            const intervalGroup = document.getElementById('intervalGroup');

            if (e.target.value === 'quote') {
                timeframeGroup.style.display = 'none';
                intervalGroup.style.display = 'none';
            } else {
                timeframeGroup.style.display = 'block';
                intervalGroup.style.display = 'block';
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/save_results', methods=['POST'])
def save_results():
    """Save analysis results to output.json"""
    try:
        data = request.get_json()
        if data:
            with open('output.json', 'w') as f:
                json.dump(data, f, indent=2)
            return jsonify({"status": "saved", "message": "Results saved to output.json"})
        else:
            return jsonify({"status": "error", "message": "No data to save"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_stocks():
    """API endpoint for stock analysis"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided", "success": False}), 400

        # Create temporary input file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            temp_file = f.name

        try:
            # Run the market analysis with INPUT_FILE environment variable
            env = os.environ.copy()
            env['INPUT_FILE'] = temp_file

            result = subprocess.run(
                ['python', 'main.py'],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(__file__),
                env=env
            )

            if result.returncode != 0:
                return jsonify({
                    "error": f"Analysis failed: {result.stderr}",
                    "success": False
                }), 500

            # Parse the JSON output
            try:
                output_lines = result.stdout.strip().split('\n')
                # Find the JSON output (usually the last meaningful line)
                json_output = None
                for line in reversed(output_lines):
                    line = line.strip()
                    if line.startswith('{'):
                        json_output = line
                        break

                if not json_output:
                    return jsonify({
                        "error": "No JSON output found",
                        "success": False
                    }), 500

                analysis_result = json.loads(json_output)
                return jsonify(analysis_result)

            except json.JSONDecodeError as e:
                return jsonify({
                    "error": f"Failed to parse analysis output: {str(e)}",
                    "raw_output": result.stdout[-500:],  # Last 500 chars for debugging
                    "success": False
                }), 500

        finally:
            # Clean up temp file
            try:
                os.unlink(temp_file)
            except:
                pass

    except Exception as e:
        return jsonify({
            "error": f"Server error: {str(e)}",
            "success": False
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Market Analysis Web Interface...")
    print("📱 Visit: http://localhost:5000")
    print("🎯 Select stocks and click 'Analyze Stocks' to test Method B")
    app.run(debug=True, host='0.0.0.0', port=5000)
