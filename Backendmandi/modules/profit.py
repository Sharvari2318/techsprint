"""Profit analysis module"""

def profit_estimation(price, quantity, risk_score, transport_cost=500, storage_cost=300):
    """
    Estimate profit considering spoilage risk
    
    Args:
        price: Price per unit
        quantity: Total quantity in kg
        risk_score: Risk percentage (0-100)
        transport_cost: Transport cost in rupees
        storage_cost: Storage cost in rupees
    
    Returns:
        dict: Profit analysis
    """
    try:
        # Estimate spoilage loss based on risk percentage
        spoilage_loss = (risk_score / 100) * quantity

        # Effective quantity after spoilage
        effective_quantity = quantity - spoilage_loss

        # Revenue after spoilage
        revenue = price * effective_quantity

        # Total costs
        total_cost = transport_cost + storage_cost

        # Net profit
        net_profit = revenue - total_cost

        # Profit margin
        profit_margin = (net_profit / revenue) * 100 if revenue != 0 else 0

        return {
            "effective_quantity": round(effective_quantity, 2),
            "revenue": round(revenue, 2),
            "total_cost": total_cost,
            "net_profit": round(net_profit, 2),
            "profit_margin_percent": round(profit_margin, 2)
        }
    except Exception as e:
        print(f"Error in profit_estimation: {str(e)}")
        return None


def analyze_profit(lat, lon, price, quantity, risk_score):
    """
    Analyze profit for API endpoint
    
    Args:
        lat: Latitude
        lon: Longitude
        price: Price per unit
        quantity: Quantity in kg
        risk_score: Risk percentage
    
    Returns:
        dict: Profit analysis
    """
    try:
        return profit_estimation(price, quantity, risk_score)
    except Exception as e:
        print(f"Error in analyze_profit: {str(e)}")
        return None