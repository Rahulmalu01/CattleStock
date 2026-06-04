from prediction.models import DiseasePrediction
from prediction.services import get_prediction


def create_prediction(cattle, sensor_reading):
    try:
        result = get_prediction(sensor_reading)
        print("=" * 60)
        print("ML RESPONSE:")
        print(result)
        print("=" * 60)
        prediction_data = result.get('prediction', result)
        disease = prediction_data.get('disease','healthy')
        confidence = prediction_data.get('confidence',0)
        risk_level = prediction_data.get('risk_level','low')
        recommendation = prediction_data.get('recommendation','No recommendation available.')
        model_version = prediction_data.get('model_version','v1.0')
        contributing_factors = prediction_data.get('contributing_factors',[])
        prediction = DiseasePrediction.objects.create(
            cattle=cattle,
            disease=disease,
            confidence=confidence,
            risk_level=risk_level,
            recommendation=recommendation,
            model_version=model_version
        )
        print(f"Prediction Saved: " f"{cattle.cattle_id} -> {disease}")
        return prediction
    except Exception as e:
        print(f"Prediction Error: {str(e)}")
        return None