"""
Flask backend for Brent Oil Dashboard
Provides API endpoints for data and analysis results
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Paths to data files
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
PROCESSED_DATA_PATH = os.path.join(DATA_DIR, 'processed', 'brent_prices_processed.csv')
EVENTS_DATA_PATH = os.path.join(DATA_DIR, 'external', 'key_events.csv')
RESULTS_PATH = os.path.join(os.path.dirname(__file__), '..', 'notebooks', '02_Change_Point_Modeling.ipynb')

# Load data
try:
    price_data = pd.read_csv(PROCESSED_DATA_PATH)
    price_data['Date'] = pd.to_datetime(price_data['Date'])
    price_data = price_data.sort_values('Date')
    print(f"✓ Loaded price data: {len(price_data)} rows")
except Exception as e:
    print(f"⚠ Error loading price data: {e}")
    price_data = pd.DataFrame()

try:
    events_data = pd.read_csv(EVENTS_DATA_PATH)
    events_data['event_date'] = pd.to_datetime(events_data['event_date'])
    print(f"✓ Loaded events data: {len(events_data)} events")
except Exception as e:
    print(f"⚠ Error loading events data: {e}")
    events_data = pd.DataFrame()

# Pre-calculated change point results (from Task 2)
CHANGE_POINT_RESULTS = {
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
    "credible_interval_lower": "2021-04-30",
    "credible_interval_upper": "2021-04-30",
    "correlated_events": [
        {
            "event_date": "2021-05-01",
            "event_name": "India COVID-19 Second Wave Peaks",
            "event_type": "Economic",
            "days_from_change": 1,
            "direction": "after"
        },
        {
            "event_date": "2021-04-02",
            "event_name": "OPEC+ Gradual Production Increase",
            "event_type": "OPEC Policy",
            "days_from_change": -28,
            "direction": "before"
        },
        {
            "event_date": "2021-03-23",
            "event_name": "Suez Canal Container Ship Blockage",
            "event_type": "Economic",
            "days_from_change": -38,
            "direction": "before"
        }
    ]
}

@app.route('/')
def home():
    """API Home endpoint"""
    return jsonify({
        "api": "Brent Oil Dashboard API",
        "version": "1.0",
        "endpoints": {
            "/api/prices": "Get historical price data",
            "/api/events": "Get geopolitical/economic events",
            "/api/change-point": "Get change point analysis results",
            "/api/summary": "Get key metrics summary",
            "/api/volatility": "Get volatility metrics",
            "/api/event-impact/<event_id>": "Get impact analysis for specific event"
        }
    })

@app.route('/api/prices', methods=['GET'])
def get_prices():
    """Get historical price data with optional filtering"""
    try:
        # Get query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        data = price_data.copy()
        
        # Apply date filters if provided
        if start_date:
            start_date = pd.to_datetime(start_date)
            data = data[data['Date'] >= start_date]
        if end_date:
            end_date = pd.to_datetime(end_date)
            data = data[data['Date'] <= end_date]
        
        # Convert to list of dictionaries for JSON
        result = data.to_dict('records')
        
        # Format dates as strings
        for item in result:
            if 'Date' in item and pd.notna(item['Date']):
                item['Date'] = item['Date'].strftime('%Y-%m-%d')
        
        return jsonify({
            "success": True,
            "data": result,
            "count": len(result),
            "date_range": {
                "start": data['Date'].min().strftime('%Y-%m-%d') if len(data) > 0 else None,
                "end": data['Date'].max().strftime('%Y-%m-%d') if len(data) > 0 else None
            }
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/events', methods=['GET'])
def get_events():
    """Get geopolitical/economic events"""
    try:
        # Get query parameters
        event_type = request.args.get('type')
        severity = request.args.get('severity')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        data = events_data.copy()
        
        # Apply filters
        if event_type:
            data = data[data['event_type'] == event_type]
        if severity:
            data = data[data['severity'] == severity]
        if start_date:
            start_date = pd.to_datetime(start_date)
            data = data[data['event_date'] >= start_date]
        if end_date:
            end_date = pd.to_datetime(end_date)
            data = data[data['event_date'] <= end_date]
        
        # Format for response
        result = []
        for idx, row in data.reset_index(drop=True).iterrows():
            result.append({
                "id": idx,  # Use sequential numeric ID
                "event_date": row['event_date'].strftime('%Y-%m-%d'),
                "event_name": row['event_name'],
                "event_type": row['event_type'],
                "severity": row.get('severity', 'Medium'),
                "region": row.get('region', 'Global'),
                "description": row.get('description', '')
            })
        
        return jsonify({
            "success": True,
            "data": result,
            "count": len(result)
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/change-point', methods=['GET'])
def get_change_point():
    """Get change point analysis results"""
    try:
        return jsonify({
            "success": True,
            "data": CHANGE_POINT_RESULTS
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/summary', methods=['GET'])
def get_summary():
    """Get key metrics summary"""
    try:
        if price_data.empty:
            raise ValueError("Price data not loaded")
        
        # Calculate summary statistics
        latest_price = price_data['Price'].iloc[-1] if len(price_data) > 0 else 0
        avg_price = price_data['Price'].mean()
        min_price = price_data['Price'].min()
        max_price = price_data['Price'].max()
        volatility = price_data['Log_Return'].std() if 'Log_Return' in price_data.columns else 0
        
        # Calculate annual returns
        if len(price_data) > 1:
            first_price = price_data['Price'].iloc[0]
            last_price = price_data['Price'].iloc[-1]
            total_return_pct = ((last_price - first_price) / first_price) * 100
            
            # Estimate annualized return
            days_diff = (price_data['Date'].iloc[-1] - price_data['Date'].iloc[0]).days
            years_diff = days_diff / 365.25
            annualized_return = ((1 + total_return_pct/100) ** (1/years_diff) - 1) * 100
        else:
            total_return_pct = 0
            annualized_return = 0
        
        summary = {
            "latest_price": round(latest_price, 2),
            "average_price": round(avg_price, 2),
            "min_price": round(min_price, 2),
            "max_price": round(max_price, 2),
            "price_range": round(max_price - min_price, 2),
            "volatility": round(volatility, 4),
            "total_return_pct": round(total_return_pct, 1),
            "annualized_return_pct": round(annualized_return, 1),
            "total_events": len(events_data),
            "change_point_date": CHANGE_POINT_RESULTS["change_point_date"],
            "price_impact_pct": CHANGE_POINT_RESULTS["price_change_pct"]
        }
        
        return jsonify({
            "success": True,
            "data": summary
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/volatility', methods=['GET'])
def get_volatility():
    """Get volatility metrics and rolling volatility"""
    try:
        if price_data.empty or 'Log_Return' not in price_data.columns:
            raise ValueError("Price data with returns not available")
        
        # Calculate rolling volatility (30-day window)
        returns = price_data['Log_Return'].dropna()
        rolling_volatility = returns.rolling(window=30).std().dropna()
        
        # Prepare volatility data
        vol_data = []
        for idx, vol in rolling_volatility.items():
            if pd.notna(vol) and idx in price_data.index:
                vol_data.append({
                    "date": price_data.loc[idx, 'Date'].strftime('%Y-%m-%d'),
                    "volatility": round(vol, 4),
                    "price": round(price_data.loc[idx, 'Price'], 2) if 'Price' in price_data.columns else None
                })
        
        # Volatility statistics
        vol_stats = {
            "mean": round(returns.std(), 4),
            "max": round(returns.std() * 3, 4),  # Approx max
            "min": round(returns.std() * 0.5, 4),  # Approx min
            "current": round(rolling_volatility.iloc[-1] if len(rolling_volatility) > 0 else returns.std(), 4)
        }
        
        return jsonify({
            "success": True,
            "rolling_volatility": vol_data[-100:],  # Last 100 days
            "statistics": vol_stats
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/event-impact/<event_id>', methods=['GET'])
def get_event_impact(event_id):
    """Get impact analysis for specific event"""
    try:
        # Find the event
        event_idx = int(event_id) if event_id.isdigit() else 0
        if event_idx >= len(events_data):
            return jsonify({
                "success": False,
                "error": f"Event with ID {event_id} not found"
            }), 404
        
        event = events_data.iloc[event_idx]
        event_date = event['event_date']
        
        # Calculate impact window (30 days before/after)
        window_days = 30
        start_date = event_date - timedelta(days=window_days)
        end_date = event_date + timedelta(days=window_days)
        
        # Get prices in impact window
        window_data = price_data[
            (price_data['Date'] >= start_date) & 
            (price_data['Date'] <= end_date)
        ].copy()
        
        if len(window_data) == 0:
            return jsonify({
                "success": False,
                "error": f"No price data available for event window"
            }), 404
        
        # Calculate price changes
        before_event = window_data[window_data['Date'] < event_date]
        after_event = window_data[window_data['Date'] > event_date]
        
        price_before = before_event['Price'].mean() if len(before_event) > 0 else 0
        price_after = after_event['Price'].mean() if len(after_event) > 0 else 0
        price_change = price_after - price_before
        price_change_pct = (price_change / price_before * 100) if price_before > 0 else 0
        
        # Prepare response
        impact_data = {
            "event": {
                "id": event_idx,
                "date": event_date.strftime('%Y-%m-%d'),
                "name": event['event_name'],
                "type": event['event_type'],
                "severity": event.get('severity', 'Medium')
            },
            "impact_window": {
                "days_before": window_days,
                "days_after": window_days,
                "start_date": start_date.strftime('%Y-%m-%d'),
                "end_date": end_date.strftime('%Y-%m-%d')
            },
            "price_impact": {
                "before_event": round(price_before, 2),
                "after_event": round(price_after, 2),
                "absolute_change": round(price_change, 2),
                "percentage_change": round(price_change_pct, 2)
            },
            "price_data": window_data[['Date', 'Price']].to_dict('records')
        }
        
        # Format dates in price data
        for item in impact_data['price_data']:
            if 'Date' in item and pd.notna(item['Date']):
                item['Date'] = item['Date'].strftime('%Y-%m-%d')
        
        return jsonify({
            "success": True,
            "data": impact_data
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/price-predictions', methods=['GET'])
def get_price_predictions():
    """Get simple price predictions based on recent trends"""
    try:
        if price_data.empty:
            raise ValueError("Price data not available")
        
        # Simple prediction: last 30 days average trend
        recent_data = price_data.tail(30)
        if len(recent_data) < 2:
            return jsonify({
                "success": False,
                "error": "Not enough data for prediction"
            }), 400
        
        # Calculate average daily return
        recent_returns = recent_data['Log_Return'].dropna().mean()
        
        # Generate 7-day forecast
        last_price = recent_data['Price'].iloc[-1]
        last_date = recent_data['Date'].iloc[-1]
        
        predictions = []
        for i in range(1, 8):
            forecast_date = last_date + timedelta(days=i)
            forecast_price = last_price * (1 + recent_returns) ** i
            
            predictions.append({
                "date": forecast_date.strftime('%Y-%m-%d'),
                "price": round(forecast_price, 2),
                "change_pct": round(((forecast_price / last_price) - 1) * 100, 2)
            })
        
        return jsonify({
            "success": True,
            "data": {
                "last_actual_price": round(last_price, 2),
                "last_actual_date": last_date.strftime('%Y-%m-%d'),
                "prediction_horizon_days": 7,
                "predictions": predictions
            },
            "disclaimer": "Predictions based on simple trend extrapolation. Not financial advice."
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Brent Oil Dashboard API...")
    print("📊 Available endpoints:")
    print("   http://localhost:5000/")
    print("   http://localhost:5000/api/prices")
    print("   http://localhost:5000/api/events")
    print("   http://localhost:5000/api/change-point")
    print("   http://localhost:5000/api/summary")
    print("   http://localhost:5000/api/volatility")
    print("   http://localhost:5000/api/event-impact/0")
    print("   http://localhost:5000/api/price-predictions")
    
    app.run(debug=True, host='0.0.0.0', port=5000)