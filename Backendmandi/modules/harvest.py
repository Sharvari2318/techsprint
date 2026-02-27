"""Harvest recommendation module"""

def get_harvest_recommendation(lat, lon, quantity):
    """Get harvest recommendations"""
    try:
        recommendations = [
            {
                "title": "Optimal Harvest Window",
                "description": "Crop ready for harvest in 7-10 days based on maturity",
                "priority": "high",
                "confidence": 0.88
            },
            {
                "title": "Weather Alert",
                "description": "Monitor rainfall - avoid harvesting in heavy rain",
                "priority": "medium",
                "confidence": 0.75
            },
            {
                "title": "Labor Availability",
                "description": "Ensure sufficient labor for timely harvest",
                "priority": "medium",
                "confidence": 0.70
            },
            {
                "title": "Equipment Check",
                "description": "Verify harvesting equipment is ready",
                "priority": "low",
                "confidence": 0.95
            }
        ]
        
        return {
            "recommendations": recommendations,
            "estimated_yield": f"{quantity} kg",
            "expected_harvest_date": "2026-03-08",
            "quality_grade": "A"
        }
    except Exception as e:
        print(f"Error in get_harvest_recommendation: {str(e)}")
        return None