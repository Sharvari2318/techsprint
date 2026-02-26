def profit_estimation(price, quantity, risk_score, transport_cost=500, storage_cost=300):

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


