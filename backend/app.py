"""
Flask backend for Brent Oil Dashboard
USING PRECOMPUTED RESULTS - Instant startup!
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = Flask(__name__)
CORS(app)

# ============================================
# PATHS
# ============================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
PROCESSED_DATA_PATH = os.path.join(DATA_DIR, 'processed', 'brent_prices_processed.csv')
RAW_DATA_PATH = os.path.join(DATA_DIR, 'raw', 'BrentOilPrices.csv')
EVENTS_DATA_PATH = os.path.join(DATA_DIR, 'external', 'key_events.csv')
PRECOMPUTED_RESULTS_PATH = os.path.join(os.path.dirname(__file__), 'precomputed_results.json')


# ============================================
# LOAD DATA (Fast - just CSV reading)
# ============================================
def load_data():
    """Load price and events data (fast - no model training)"""
    print("\n📂 Loading data...")
    
    price_data = None
    events_data = None
    
    # Load price data
    try:
        if os.path.exists(PROCESSED_DATA_PATH):
            price_data = pd.read_csv(PROCESSED_DATA_PATH)
            price_data['Date'] = pd.to_datetime(price_data['Date'])
            price_data = price_data.sort_values('Date')
            print(f"✅ Loaded price data: {len(price_data)} rows")
        else:
            # Create minimal mock data
            dates = pd.date_range(start='2020-01-01', end='2022-12-31', freq='D')
            price_data = pd.DataFrame({
                'Date': dates,
                'Price': 50 + np.cumsum(np.random.randn(len(dates)) * 0.1),
                'Log_Return': np.random.randn(len(dates)) * 0.02
            })
            print(f"✅ Created mock price data: {len(price_data)} rows")
    except Exception as e:
        print(f"⚠ Error: {e}")
        # Ultimate fallback
        price_data = pd.DataFrame({
            'Date': [datetime.now() - timedelta(days=i) for i in range(100, 0, -1)],
            'Price': [50 + i * 0.1 for i in range(100)],
            'Log_Return': [0.001] * 100
        })
    
    # Load events data
    try:
        if os.path.exists(EVENTS_DATA_PATH):
            events_data = pd.read_csv(EVENTS_DATA_PATH)
            events_data['event_date'] = pd.to_datetime(events_data['event_date'])
            print(f"✅ Loaded events: {len(events_data)} events")
        else:
            events_data = pd.DataFrame([
                {'event_date': '2021-04-30', 'event_name': 'Change Point Detected', 
                 'event_type': 'Analysis', 'severity': 'High'},
                {'event_date': '2021-05-01', 'event_name': 'India COVID-19 Second Wave', 
                 'event_type': 'Economic', 'severity': 'High'},
                {'event_date': '2021-04-02', 'event_name': 'OPEC+ Production Increase', 
                 'event_type': 'OPEC Policy', 'severity': 'Medium'},
                {'event_date': '2021-03-23', 'event_name': 'Suez Canal Blockage', 
                 'event_type': 'Economic', 'severity': 'High'},
            ])
            events_data['event_date'] = pd.to_datetime(events_data['event_date'])
            print(f"✅ Created mock events: {len(events_data)} events")
    except Exception as e:
        events_data = pd.DataFrame()
    
    return price_data, events_data


# ============================================
# LOAD PRECOMPUTED RESULTS (from Week 11)
# ============================================
def load_precomputed_results():
    """Load results from Task 2 analysis"""
    try:
        if os.path.exists(PRECOMPUTED_RESULTS_PATH):
            with open(PRECOMPUTED_RESULTS_PATH, 'r') as f:
                results = json.load(f)
            print(f"✅ Loaded precomputed results")
            return results
    except Exception as e:
        print(f"⚠ Could not load precomputed results: {e}")
    
    # Hardcoded fallback (your actual results)
    return {
        "change_point_date": "2021-04-30",
        "price_before": 52.31,
        "price_after": 68.96,
        "price_change_pct": 31.8,
        "return_before": -0.001792,
        "return_after": 0.004035,
        "return_change_pp": 0.5827,
        "volatility_before": 0.0412,
        "volatility_after": 0.0421,
        "volatility_change_pct": 2.2,
        "correlated_events": [
            {"event_date": "2021-05-01", "event_name": "India COVID-19 Second Wave Peaks", 
             "event_type": "Economic", "days_from_change": 1, "direction": "after"},
            {"event_date": "2021-04-02", "event_name": "OPEC+ Gradual Production Increase", 
             "event_type": "OPEC Policy", "days_from_change": -28, "direction": "before"},
            {"event_date": "2021-03-23", "event_name": "Suez Canal Container Ship Blockage", 
             "event_type": "Economic", "days_from_change": -38, "direction": "before"}
        ]
    }


# ============================================
# INITIALIZE - FAST STARTUP
# ============================================
print("\n" + "=" * 60)
print("🚀 BRENT OIL DASHBOARD API - FAST STARTUP")
print("=" * 60)

# Load data (fast)
price_data, events_data = load_data()

# Load results (instant)
CHANGE_POINT_RESULTS = load_precomputed_results()

print(f"\n✅ Ready! Dashboard will load in < 2 seconds")
print(f"📊 Change Point: {CHANGE_POINT_RESULTS['change_point_date']}")
print(f"💰 Price Impact: +{CHANGE_POINT_RESULTS['price_change_pct']}%")


# ============================================
# API ENDPOINTS (Your existing endpoints - unchanged)
# ============================================

@app.route('/')
def home():
    return jsonify({
        "api": "Brent Oil Dashboard API",
        "version": "1.0",
        "status": "running",
        "data_source": "REAL" if price_data is not None and len(price_data) > 100 else "MOCK",
        "change_point": CHANGE_POINT_RESULTS['change_point_date'],
        "price_impact": f"+{CHANGE_POINT_RESULTS['price_change_pct']}%"
    })


@app.route('/api/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "data": {
            "price_records": len(price_data) if price_data is not None else 0,
            "events_count": len(events_data) if events_data is not None else 0,
            "change_point_date": CHANGE_POINT_RESULTS['change_point_date']
        }
    })


@app.route('/api/prices', methods=['GET'])
def get_prices():
    try:
        if price_data is None:
            return jsonify({"error": "No data"}), 500
        
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        limit = request.args.get('limit', default=500, type=int)
        
        data = price_data.copy()
        
        if start_date:
            data = data[data['Date'] >= pd.to_datetime(start_date)]
        if end_date:
            data = data[data['Date'] <= pd.to_datetime(end_date)]
        
        result = []
        for _, row in data.iterrows():
            result.append({
                "Date": row['Date'].strftime('%Y-%m-%d'),
                "Price": float(row['Price']),
                "Log_Return": float(row.get('Log_Return', 0))
            })
        
        if len(result) > limit:
            result = result[-limit:]
        
        return jsonify({"success": True, "data": result, "count": len(result)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/events', methods=['GET'])
def get_events():
    try:
        if events_data is None or len(events_data) == 0:
            return jsonify({"success": True, "data": []})
        
        result = []
        for idx, row in events_data.iterrows():
            result.append({
                "id": idx,
                "event_date": row['event_date'].strftime('%Y-%m-%d'),
                "event_name": row['event_name'],
                "event_type": row.get('event_type', 'Unknown'),
                "severity": row.get('severity', 'Medium')
            })
        
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/change-point', methods=['GET'])
def get_change_point():
    return jsonify({"success": True, "data": CHANGE_POINT_RESULTS})


@app.route('/api/summary', methods=['GET'])
def get_summary():
    try:
        if price_data is None:
            return jsonify({"error": "No data"}), 500
        
        summary = {
            "latest_price": round(price_data['Price'].iloc[-1], 2),
            "average_price": round(price_data['Price'].mean(), 2),
            "min_price": round(price_data['Price'].min(), 2),
            "max_price": round(price_data['Price'].max(), 2),
            "volatility": round(price_data['Log_Return'].std(), 4) if 'Log_Return' in price_data.columns else 0.025,
            "total_events": len(events_data) if events_data is not None else 0,
            "change_point_date": CHANGE_POINT_RESULTS['change_point_date'],
            "price_impact_pct": CHANGE_POINT_RESULTS['price_change_pct']
        }
        
        return jsonify({"success": True, "data": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/volatility', methods=['GET'])
def get_volatility():
    try:
        if price_data is None:
            return jsonify({"error": "No data"}), 500
        
        window = request.args.get('window', default=30, type=int)
        
        returns = price_data['Log_Return'] if 'Log_Return' in price_data.columns else price_data['Price'].pct_change()
        rolling_vol = returns.rolling(window=window).std().dropna()
        
        vol_data = []
        for i, (idx, vol) in enumerate(rolling_vol.items()):
            if pd.notna(vol) and idx < len(price_data):
                vol_data.append({
                    "date": price_data.loc[idx, 'Date'].strftime('%Y-%m-%d'),
                    "volatility": round(vol, 4),
                    "price": round(price_data.loc[idx, 'Price'], 2)
                })
        
        return jsonify({
            "success": True,
            "rolling_volatility": vol_data[-200:],
            "statistics": {
                "mean": round(returns.std(), 4),
                "current": round(rolling_vol.iloc[-1], 4) if len(rolling_vol) > 0 else round(returns.std(), 4)
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/price-predictions', methods=['GET'])
def get_price_predictions():
    try:
        if price_data is None:
            return jsonify({"error": "No data"}), 500
        
        recent = price_data.tail(30)
        avg_return = recent['Log_Return'].mean() if 'Log_Return' in recent.columns else 0.0002
        last_price = recent['Price'].iloc[-1]
        last_date = recent['Date'].iloc[-1]
        
        predictions = []
        for i in range(1, 8):
            pred_date = last_date + timedelta(days=i)
            pred_price = last_price * np.exp(avg_return * i)
            predictions.append({
                "date": pred_date.strftime('%Y-%m-%d'),
                "price": round(pred_price, 2)
            })
        
        return jsonify({"success": True, "data": {"predictions": predictions}})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================
# MAIN
# ============================================
if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🚀 Server starting...")
    print("📊 Endpoints ready at http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=False)