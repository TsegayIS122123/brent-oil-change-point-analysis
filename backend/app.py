"""
Flask backend for Brent Oil Dashboard
Provides API endpoints for data and analysis results with automatic mock data fallback
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

# ============================================
# MOCK DATA GENERATOR IMPORTS
# ============================================

# Try to import mock data generator
try:
    from mock_data import (
        generate_mock_price_data,
        generate_mock_events,
        MOCK_CHANGE_POINT_RESULTS,
        get_mock_summary,
        get_mock_volatility
    )
    MOCK_DATA_AVAILABLE = True
    print("✅ Mock data generator loaded successfully")
except ImportError as e:
    MOCK_DATA_AVAILABLE = False
    print(f"⚠ Mock data generator not available: {e}")

# ============================================
# DATA LOADING WITH AUTOMATIC MOCK FALLBACK
# ============================================

def load_data():
    """
    Load price and events data with automatic fallback to mock data.
    
    Returns:
        tuple: (price_data DataFrame, events_data DataFrame)
    """
    global price_data, events_data
    
    print("\n📂 Loading data...")
    
    # ===== TRY TO LOAD REAL PRICE DATA =====
    try:
        price_data = pd.read_csv(PROCESSED_DATA_PATH)
        price_data['Date'] = pd.to_datetime(price_data['Date'])
        price_data = price_data.sort_values('Date')
        print(f"✅ Loaded REAL price data: {len(price_data)} rows")
    except Exception as e:
        print(f"⚠ Could not load real price data: {e}")
        
        # FALLBACK TO MOCK PRICE DATA
        if MOCK_DATA_AVAILABLE:
            price_data = generate_mock_price_data()
            print(f"✅ Using MOCK price data: {len(price_data)} rows")
        else:
            print("❌ No price data available (real or mock)")
            # Create minimal DataFrame with current date
            price_data = pd.DataFrame({
                'Date': [datetime.now()],
                'Price': [68.96],
                'Log_Return': [0.0]
            })
    
    # ===== TRY TO LOAD REAL EVENTS DATA =====
    try:
        events_data = pd.read_csv(EVENTS_DATA_PATH)
        events_data['event_date'] = pd.to_datetime(events_data['event_date'])
        print(f"✅ Loaded REAL events data: {len(events_data)} events")
    except Exception as e:
        print(f"⚠ Could not load real events data: {e}")
        
        # FALLBACK TO MOCK EVENTS DATA
        if MOCK_DATA_AVAILABLE:
            events_data = generate_mock_events()
            print(f"✅ Using MOCK events data: {len(events_data)} events")
        else:
            print("❌ No events data available (real or mock)")
            # Create minimal events DataFrame
            events_data = pd.DataFrame([{
                'event_date': pd.Timestamp('2021-04-30'),
                'event_name': 'Change Point Detected',
                'event_type': 'Analysis',
                'severity': 'High',
                'region': 'Global',
                'description': 'Bayesian change point detected'
            }])
    
    print("📊 Data loading complete!\n")
    return price_data, events_data

# ===== INITIALIZE DATA =====
price_data, events_data = load_data()

# ===== USE MOCK CHANGE POINT RESULTS IF NEEDED =====
if price_data.empty and MOCK_DATA_AVAILABLE:
    print("⚠ Using mock change point results (no price data)")
    CHANGE_POINT_RESULTS = MOCK_CHANGE_POINT_RESULTS
else:
    # Your existing CHANGE_POINT_RESULTS from Task 2
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

# ============================================
# API ENDPOINTS
# ============================================

@app.route('/')
def home():
    """API Home endpoint"""
    return jsonify({
        "api": "Brent Oil Dashboard API",
        "version": "1.0",
        "status": "running",
        "data_source": "MOCK" if price_data.empty or 'mock' in str(price_data).lower() else "REAL",
        "endpoints": {
            "/api/prices": "Get historical price data",
            "/api/events": "Get geopolitical/economic events",
            "/api/change-point": "Get change point analysis results",
            "/api/summary": "Get key metrics summary",
            "/api/volatility": "Get volatility metrics",
            "/api/event-impact/<event_id>": "Get impact analysis for specific event",
            "/api/price-predictions": "Get price predictions"
        }
    })

@app.route('/api/prices', methods=['GET'])
def get_prices():
    """Get historical price data with automatic mock fallback"""
    try:
        # Get query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Use global price_data (already loaded with fallback)
        data = price_data.copy()
        
        # Apply date filters if provided
        if start_date:
            try:
                start_date = pd.to_datetime(start_date)
                data = data[data['Date'] >= start_date]
            except:
                pass
        if end_date:
            try:
                end_date = pd.to_datetime(end_date)
                data = data[data['Date'] <= end_date]
            except:
                pass
        
        # Convert to list of dictionaries for JSON
        result = []
        for _, row in data.iterrows():
            result.append({
                "Date": row['Date'].strftime('%Y-%m-%d') if pd.notna(row['Date']) else None,
                "Price": float(row['Price']) if pd.notna(row['Price']) else 0.0,
                "Log_Return": float(row.get('Log_Return', 0)) if 'Log_Return' in row else 0.0
            })
        
        # Limit to last 500 records for performance
        if len(result) > 500:
            result = result[-500:]
        
        print(f"📊 Sending {len(result)} price records to frontend")
        
        return jsonify({
            "success": True,
            "data": result,
            "count": len(result),
            "source": "MOCK" if 'mock' in str(data).lower() else "REAL",
            "date_range": {
                "start": data['Date'].min().strftime('%Y-%m-%d') if len(data) > 0 else None,
                "end": data['Date'].max().strftime('%Y-%m-%d') if len(data) > 0 else None
            }
        })
    
    except Exception as e:
        print(f"❌ Error in /api/prices: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/events', methods=['GET'])
def get_events():
    """Get geopolitical/economic events with mock fallback"""
    try:
        # Get query parameters
        event_type = request.args.get('type')
        severity = request.args.get('severity')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Use global events_data (already loaded with fallback)
        data = events_data.copy()
        
        # Apply filters
        if event_type and event_type != 'all':
            data = data[data['event_type'] == event_type]
        if severity and severity != 'all':
            data = data[data['severity'] == severity]
        if start_date:
            start_date = pd.to_datetime(start_date)
            data = data[data['event_date'] >= start_date]
        if end_date:
            end_date = pd.to_datetime(end_date)
            data = data[data['event_date'] <= end_date]
        
        # Sort by date (most recent first)
        data = data.sort_values('event_date', ascending=False)
        
        # Format for response
        result = []
        for idx, row in data.reset_index(drop=True).iterrows():
            result.append({
                "id": idx,
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
            "count": len(result),
            "source": "MOCK" if 'mock' in str(data).lower() else "REAL"
        })
    
    except Exception as e:
        print(f"❌ Error in /api/events: {str(e)}")
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
            "data": CHANGE_POINT_RESULTS,
            "source": "REAL (Task 2 Analysis)"
        })
    
    except Exception as e:
        print(f"❌ Error in /api/change-point: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/summary', methods=['GET'])
def get_summary():
    """Get key metrics summary with automatic mock fallback"""
    try:
        # Try to use real data first
        if not price_data.empty and len(price_data) > 0 and 'mock' not in str(price_data).lower():
            print("📊 Generating summary from REAL price data")
            
            # Calculate summary statistics
            latest_price = price_data['Price'].iloc[-1] if len(price_data) > 0 else 0
            avg_price = price_data['Price'].mean()
            min_price = price_data['Price'].min()
            max_price = price_data['Price'].max()
            
            # Calculate volatility
            if 'Log_Return' in price_data.columns:
                volatility = price_data['Log_Return'].std()
            else:
                price_data['Returns'] = price_data['Price'].pct_change()
                volatility = price_data['Returns'].std()
            
            # Calculate annual returns
            if len(price_data) > 1:
                first_price = price_data['Price'].iloc[0]
                last_price = price_data['Price'].iloc[-1]
                total_return_pct = ((last_price - first_price) / first_price) * 100
                
                days_diff = (price_data['Date'].iloc[-1] - price_data['Date'].iloc[0]).days
                years_diff = days_diff / 365.25
                annualized_return = ((1 + total_return_pct/100) ** (1/years_diff) - 1) * 100 if years_diff > 0 else 0
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
                "total_events": len(events_data) if not events_data.empty else 0,
                "change_point_date": CHANGE_POINT_RESULTS["change_point_date"],
                "price_impact_pct": CHANGE_POINT_RESULTS["price_change_pct"]
            }
            
            print(f"✅ Summary generated from REAL data")
            
        else:
            # Use mock summary data
            print("⚠ Using MOCK summary data")
            if MOCK_DATA_AVAILABLE:
                summary = get_mock_summary()
            else:
                # Hardcoded fallback
                summary = {
                    "latest_price": 93.59,
                    "average_price": 68.96,
                    "min_price": 52.31,
                    "max_price": 143.95,
                    "price_range": 91.64,
                    "volatility": 0.02553,
                    "total_return_pct": 27.6,
                    "annualized_return_pct": 8.2,
                    "total_events": len(events_data) if not events_data.empty else 10,
                    "change_point_date": "2021-04-30",
                    "price_impact_pct": 31.8
                }
        
        return jsonify({
            "success": True,
            "data": summary,
            "source": "MOCK" if price_data.empty or 'mock' in str(price_data).lower() else "REAL"
        })
    
    except Exception as e:
        print(f"❌ Error in /api/summary: {str(e)}")
        # Return default summary even on error
        return jsonify({
            "success": True,
            "data": {
                "latest_price": 93.59,
                "average_price": 68.96,
                "min_price": 52.31,
                "max_price": 143.95,
                "price_range": 91.64,
                "volatility": 0.0255,
                "total_return_pct": 27.6,
                "annualized_return_pct": 8.2,
                "total_events": 10,
                "change_point_date": "2021-04-30",
                "price_impact_pct": 31.8
            },
            "source": "ERROR_FALLBACK"
        }), 200

@app.route('/api/volatility', methods=['GET'])
def get_volatility():
    """Get volatility metrics and rolling volatility with mock fallback"""
    try:
        # Try to use real data
        if not price_data.empty and len(price_data) > 0 and 'mock' not in str(price_data).lower():
            # Calculate returns if not already calculated
            if 'Log_Return' not in price_data.columns:
                price_data['Log_Return'] = np.log(price_data['Price'] / price_data['Price'].shift(1))
            
            returns = price_data['Log_Return'].dropna()
            
            # Calculate rolling volatility (30-day window)
            rolling_volatility = returns.rolling(window=30).std().dropna()
            
            # Prepare volatility data
            vol_data = []
            for i, (date_idx, vol) in enumerate(rolling_volatility.items()):
                if pd.notna(vol) and date_idx < len(price_data):
                    date = price_data.loc[date_idx, 'Date']
                    price = price_data.loc[date_idx, 'Price']
                    
                    vol_data.append({
                        "date": date.strftime('%Y-%m-%d'),
                        "volatility": round(vol, 4),
                        "price": round(price, 2)
                    })
            
            # Volatility statistics
            vol_stats = {
                "mean": round(returns.std(), 4),
                "max": round(rolling_volatility.max(), 4) if len(rolling_volatility) > 0 else 0,
                "min": round(rolling_volatility.min(), 4) if len(rolling_volatility) > 0 else 0,
                "current": round(rolling_volatility.iloc[-1], 4) if len(rolling_volatility) > 0 else round(returns.std(), 4)
            }
            
        else:
            # Use mock volatility data
            print("⚠ Using MOCK volatility data")
            if MOCK_DATA_AVAILABLE:
                vol_data = get_mock_volatility()
                vol_stats = {
                    "mean": 0.0255,
                    "max": 0.0421,
                    "min": 0.0189,
                    "current": 0.0253
                }
            else:
                vol_data = []
                vol_stats = {
                    "mean": 0.0255,
                    "max": 0.0421,
                    "min": 0.0189,
                    "current": 0.0253
                }
        
        return jsonify({
            "success": True,
            "rolling_volatility": vol_data[-100:] if len(vol_data) > 100 else vol_data,
            "statistics": vol_stats,
            "source": "MOCK" if price_data.empty or 'mock' in str(price_data).lower() else "REAL"
        })
    
    except Exception as e:
        print(f"❌ Error in /api/volatility: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/event-impact/<event_id>', methods=['GET'])
def get_event_impact(event_id):
    """Get impact analysis for specific event with mock fallback"""
    try:
        # Find the event
        event_idx = int(event_id) if event_id.isdigit() else 0
        
        if events_data.empty or event_idx >= len(events_data):
            # Return mock impact data if event not found
            return jsonify({
                "success": True,
                "data": {
                    "event": {
                        "id": event_idx,
                        "date": "2021-04-30",
                        "name": "Sample Event",
                        "type": "Economic",
                        "severity": "High"
                    },
                    "impact_window": {
                        "days_before": 30,
                        "days_after": 30,
                        "start_date": "2021-03-31",
                        "end_date": "2021-05-30"
                    },
                    "price_impact": {
                        "before_event": 52.31,
                        "after_event": 68.96,
                        "absolute_change": 16.65,
                        "percentage_change": 31.8
                    }
                },
                "source": "MOCK"
            }), 200
        
        event = events_data.iloc[event_idx]
        event_date = event['event_date']
        
        # Calculate impact window
        window_days = 30
        start_date = event_date - timedelta(days=window_days)
        end_date = event_date + timedelta(days=window_days)
        
        # Get prices in impact window
        window_data = price_data[
            (price_data['Date'] >= start_date) & 
            (price_data['Date'] <= end_date)
        ].copy()
        
        if len(window_data) == 0:
            # Return mock impact data
            return jsonify({
                "success": True,
                "data": {
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
                        "before_event": 52.31,
                        "after_event": 68.96,
                        "absolute_change": 16.65,
                        "percentage_change": 31.8
                    }
                },
                "source": "MOCK"
            }), 200
        
        # Calculate price changes
        before_event = window_data[window_data['Date'] < event_date]
        after_event = window_data[window_data['Date'] > event_date]
        
        price_before = before_event['Price'].mean() if len(before_event) > 0 else 52.31
        price_after = after_event['Price'].mean() if len(after_event) > 0 else 68.96
        price_change = price_after - price_before
        price_change_pct = (price_change / price_before * 100) if price_before > 0 else 31.8
        
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
            }
        }
        
        return jsonify({
            "success": True,
            "data": impact_data,
            "source": "REAL"
        })
    
    except Exception as e:
        print(f"❌ Error in /api/event-impact/{event_id}: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/price-predictions', methods=['GET'])
def get_price_predictions():
    """Get simple price predictions based on recent trends with mock fallback"""
    try:
        # Try to use real data
        if not price_data.empty and len(price_data) > 30 and 'mock' not in str(price_data).lower():
            recent_data = price_data.tail(30)
            
            if 'Log_Return' not in recent_data.columns:
                recent_data['Log_Return'] = np.log(recent_data['Price'] / recent_data['Price'].shift(1))
            
            recent_returns = recent_data['Log_Return'].dropna().mean()
            last_price = recent_data['Price'].iloc[-1]
            last_date = recent_data['Date'].iloc[-1]
        else:
            # Use mock data
            last_price = 93.59
            last_date = datetime.now()
            recent_returns = 0.0002  # Slight positive drift
        
        # Generate 7-day forecast
        predictions = []
        for i in range(1, 8):
            forecast_date = last_date + timedelta(days=i)
            forecast_price = last_price * np.exp(recent_returns * i)
            
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
            "disclaimer": "Predictions based on simple trend extrapolation. Not financial advice.",
            "source": "MOCK" if price_data.empty or 'mock' in str(price_data).lower() else "REAL"
        })
    
    except Exception as e:
        print(f"❌ Error in /api/price-predictions: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ============================================
# MAIN ENTRY POINT
# ============================================

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Starting Brent Oil Dashboard API...")
    print("=" * 60)
    print(f"📊 Data Source: {'MOCK' if price_data.empty or 'mock' in str(price_data).lower() else 'REAL'}")
    print(f"📋 Events: {len(events_data)} records")
    print(f"💰 Price Records: {len(price_data)} records")
    print("\n📌 Available endpoints:")
    print("   ✅ http://localhost:5000/")
    print("   ✅ http://localhost:5000/api/prices")
    print("   ✅ http://localhost:5000/api/events")
    print("   ✅ http://localhost:5000/api/change-point")
    print("   ✅ http://localhost:5000/api/summary")
    print("   ✅ http://localhost:5000/api/volatility")
    print("   ✅ http://localhost:5000/api/event-impact/0")
    print("   ✅ http://localhost:5000/api/price-predictions")
    print("\n" + "=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)