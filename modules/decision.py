from modules.harvest import harvest_recommendation
from modules.mandi import mandi_recommendation
from modules.spoilage import spoilage_simulation
from modules.profit import profit_estimation


def smart_decision_engine(df, quantity):

    # 1️⃣ Harvest Recommendation
    harvest_data = harvest_recommendation(df)

    # 2️⃣ Mandi Suggestion
    mandi_data = mandi_recommendation()
    best_price = mandi_data["expected_price"]

    # 3️⃣ Spoilage Risk (Use Current Plan scenario)
    max_temp = df["temperature_2m"].max()
    spoilage_results = spoilage_simulation(max_temp)

    # Extract risk score from "Current Plan"
    current_plan = next(
        (s for s in spoilage_results if s["scenario"] == "Current Plan"),
        spoilage_results[0]
    )

    risk_score = current_plan["risk_score"]

    # 4️⃣ Profit Estimation
    profit_data = profit_estimation(best_price, quantity, risk_score)

    # 5️⃣ Final Structured Output
    return {
        "harvest_advisor": harvest_data,
        "market_advisor": mandi_data,
        "risk_analysis": current_plan,
        "profit_estimation": profit_data,
        "final_summary": generate_summary(
            harvest_data,
            mandi_data,
            current_plan,
            profit_data
        )
    }


def generate_summary(harvest, mandi, risk, profit):

    summary = (
        f"Harvest Decision: {harvest['recommendation']}. "
        f"Best Market: {mandi['best_mandi']} at ₹{mandi['expected_price']} per unit. "
        f"Risk Level: {risk['risk_level']} ({risk['risk_score']}%). "
        f"Expected Net Profit: ₹{profit['net_profit']}."
    )

    return summary


