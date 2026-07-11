# Quick API Reference Guide

## Model Prediction Endpoint

**Endpoint:** `POST /predict`

**Host:** `http://localhost:8000`

**Description:** Predicts heart disease severity level based on 13 cardiac features

---

## Input Format

### Request Body

```json
{
  "features": [
    44,      // [0] age: Age in years (18-77)
    1,       // [1] sex: Sex (0=female, 1=male)
    1,       // [2] cp: Chest pain type (0-3)
    120,     // [3] trestbps: Resting blood pressure (mm Hg)
    263,     // [4] chol: Serum cholesterol (mg/dl)
    0,       // [5] fbs: Fasting blood sugar > 120 mg/dl (0=false, 1=true)
    1,       // [6] restecg: Resting ECG results (0-2)
    173,     // [7] thalach: Maximum heart rate achieved
    0,       // [8] exang: Exercise induced angina (0=no, 1=yes)
    0.0,     // [9] oldpeak: ST depression induced by exercise
    2,       // [10] slope: Slope of peak ST segment (0-2)
    0,       // [11] ca: Number of major vessels (0-4)
    3        // [12] thal: Thalassemia (0=normal, 1=fixed, 2=reversible, 3=other)
  ]
}
```

---

## Output Format

### Success Response (200 OK)

```json
{
  "prediction": "No disease",
  "probabilities": {
    "No disease": 0.6558365175071036,
    "Mild disease": 0.20468399467853493,
    "Moderate disease": 0.052940319670214286,
    "Severe disease": 0.03916347982085114,
    "Very severe disease": 0.047375688323296423
  }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `prediction` | string | Predicted disease severity class |
| `probabilities` | object | Probability distribution across all 5 classes |
| `probabilities.No disease` | float | Probability of no disease (0.0-1.0) |
| `probabilities.Mild disease` | float | Probability of mild disease |
| `probabilities.Moderate disease` | float | Probability of moderate disease |
| `probabilities.Severe disease` | float | Probability of severe disease |
| `probabilities.Very severe disease` | float | Probability of very severe disease |

---

## Disease Severity Classes

| Class | Level | Description |
|-------|-------|-------------|
| **No disease** | 0 | Healthy, no heart disease detected |
| **Mild disease** | 1 | Early stage disease, low severity |
| **Moderate disease** | 2 | Mid-stage disease, moderate severity |
| **Severe disease** | 3 | Advanced disease, high severity |
| **Very severe disease** | 4 | Critical stage, very high severity |

---

## Test Curl Commands

### Using PowerShell (Windows)

**Example 1: Healthy patient**
```powershell
curl -X POST http://localhost:8000/predict `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{
    "features": [44,1,1,120,263,0,1,173,0,0.0,2,0,3]
  }'
```

**Example 2: Patient with disease indicators**
```powershell
curl -X POST http://localhost:8000/predict `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{
    "features": [65,1,3,140,200,1,2,100,1,2.5,2,2,3]
  }'
```

### Using Bash/Linux/Mac

**Example 1: Healthy patient**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": [44,1,1,120,263,0,1,173,0,0.0,2,0,3]
  }'
```

**Example 2: Patient with disease indicators**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": [65,1,3,140,200,1,2,100,1,2.5,2,2,3]
  }'
```

---

## Test Data Samples

### Sample 1: Healthy Patient
```json
{
  "features": [44, 1, 1, 120, 263, 0, 1, 173, 0, 0.0, 2, 0, 3]
}
```
**Expected:** High "No disease" probability (~65%)

### Sample 2: Patient with Mild Disease Risk
```json
{
  "features": [55, 1, 2, 130, 200, 0, 1, 150, 0, 1.0, 1, 0, 2]
}
```
**Expected:** Mixed probabilities with some disease risk

### Sample 3: Patient with Severe Disease Risk
```json
{
  "features": [70, 1, 4, 150, 280, 1, 1, 80, 1, 3.0, 2, 4, 3]
}
```
**Expected:** Higher "Severe" or "Very severe" probability

---

## Using Swagger UI

### Interactive API Testing

1. Start the application:
   ```bash
   kubectl port-forward svc/heart-disease-service 8000:8000
   ```

2. Open browser:
   ```
   http://localhost:8000/docs
   ```

3. Click on **POST /predict**

4. Click **"Try it out"**

5. Enter sample data:
   ```json
   {
     "features": [44,1,1,120,263,0,1,173,0,0.0,2,0,3]
   }
   ```

6. Click **"Execute"**

7. View response in Response section

---

## Error Handling

### Invalid Input Error

**Request with wrong number of features:**
```json
{
  "features": [44, 1, 1]
}
```

**Response (422 Unprocessable Entity):**
```json
{
  "detail": "Expected 13 features, got 3"
}
```

### Missing Content-Type Header

**Response (400 Bad Request):**
```json
{
  "detail": "Invalid input format"
}
```

---

## Feature Ranges & Validation

| Feature | Min | Max | Type | Notes |
|---------|-----|-----|------|-------|
| age | 18 | 77 | integer | Patient age in years |
| sex | 0 | 1 | integer | 0=female, 1=male |
| cp | 0 | 3 | integer | 0=typical angina, 1=atypical, 2=non-anginal, 3=asymptomatic |
| trestbps | 60 | 200 | integer | Resting BP in mm Hg |
| chol | 100 | 600 | integer | Cholesterol in mg/dl |
| fbs | 0 | 1 | integer | 0=false, 1=true (>120 mg/dl) |
| restecg | 0 | 2 | integer | 0=normal, 1=ST-T abnormal, 2=LV hypertrophy |
| thalach | 60 | 202 | integer | Max heart rate achieved (bpm) |
| exang | 0 | 1 | integer | 0=no, 1=yes |
| oldpeak | 0.0 | 6.2 | float | ST depression induced by exercise |
| slope | 0 | 2 | integer | 0=upsloping, 1=flat, 2=downsloping |
| ca | 0 | 4 | integer | Number of major vessels (0-4) |
| thal | 0 | 3 | integer | 0=normal, 1=fixed, 2=reversible, 3=other |

---

## Performance Metrics

**Model Performance on Test Set:**

```
Overall Accuracy: [Your %]
Macro Precision: [Your %]
Macro Recall: [Your %]
Weighted F1-Score: [Your %]

Per-Class Performance:
- No disease: Precision [%], Recall [%]
- Mild disease: Precision [%], Recall [%]
- Moderate disease: Precision [%], Recall [%]
- Severe disease: Precision [%], Recall [%]
- Very severe disease: Precision [%], Recall [%]
```

**Inference Time:** < 10ms per prediction

**Model Size:** ~[Size] MB

---

## Common Test Cases

### Test 1: Young Healthy Male
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [35,1,0,110,180,0,0,160,0,0.0,1,0,2]}'
```
**Expected:** Very high "No disease" probability

### Test 2: Older Female with Symptoms
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [60,0,3,140,250,1,2,95,1,2.0,2,1,3]}'
```
**Expected:** Higher disease probability

### Test 3: Multiple Risk Factors
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [75,1,4,160,300,1,1,70,1,4.0,2,4,3]}'
```
**Expected:** Higher severe disease probability

---

## Debugging Tips

### Check API Health
```bash
curl http://localhost:8000/health
```

### View Metrics
```bash
curl http://localhost:8000/metrics
```

### Check Logs
```bash
# If running in Docker
docker logs <container_id>

# If running in Kubernetes
kubectl logs -f deployment/heart-disease-model
```

### Validate JSON Format
Use online JSON validators before sending:
- https://jsonlint.com/
- https://www.json-online-editor.com/

---

## Integration Examples

### Python Client
```python
import requests
import json

url = "http://localhost:8000/predict"
data = {
    "features": [44,1,1,120,263,0,1,173,0,0.0,2,0,3]
}

response = requests.post(url, json=data)
print(response.json())
```

### Node.js/JavaScript
```javascript
fetch('http://localhost:8000/predict', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    features: [44,1,1,120,263,0,1,173,0,0.0,2,0,3]
  })
})
.then(r => r.json())
.then(data => console.log(data))
```

### Java
```java
HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("http://localhost:8000/predict"))
    .POST(HttpRequest.BodyPublishers.ofString(
        "{\"features\": [44,1,1,120,263,0,1,173,0,0.0,2,0,3]}"
    ))
    .header("Content-Type", "application/json")
    .build();

client.send(request, HttpResponse.BodyHandlers.ofString());
```

---

**Last Updated:** 2024  
**API Version:** 1.0
