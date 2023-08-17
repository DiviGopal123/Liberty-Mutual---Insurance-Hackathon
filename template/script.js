const form = document.getElementById('predictionForm');
const errorElement = document.getElementById('error');
console.log("clicked button");
form.addEventListener('submit', async (e) => {
console.log("clicked button");
e.preventDefault();
errorElement.textContent = '';

// Validate the form inputs
const payment_per_month = form.payment_per_month.value;
const weeks_since_claim = form.weeks_since_claim.value;
const open_policies = form.open_policies.value;
const Renew_Offer_Type = form.Renew_Offer_Type.value;

if (!payment_per_month || isNaN(payment_per_month)) {
showError('Payment Per Month must be a valid number.');
return;
}

// Add validation for other numeric fields...

// If all inputs are valid, make a POST request to the Flask backend
const data = {
payment_per_month: parseInt(payment_per_month),
weeks_since_claim: parseInt(weeks_since_claim),
open_policies: parseInt(open_policies),
Renew_Offer_Type: parseInt(Renew_Offer_Type),
type_of_plan: form.type_of_plan.value,
work_status: form.work_status.value,
reachability: form.reachability.value,
type_of_vehicle: form.type_of_vehicle.value
};

try {
const response = await fetch('/predict', {
method: 'POST',
headers: {
'Content-Type': 'application/json'
},
body: JSON.stringify(data)
});

const result = await response.json();

// Handle the response from the Flask backend
if (response.ok) {
alert(`Prediction: ${result.prediction}`);
} else {
showError(`Error: ${result.error}`);
}
} catch (error) {
showError('Something went wrong. Please try again later.');
}
});

function showError(message) {
errorElement.textContent = message;
}