// Converts FormData() object to JSON
function formDataToJSON(htmlform){
    const formData = new FormData(htmlform)
    let jsonObject = {}
    // Loop through FormData Object key value pairs
    formData.forEach((value, key) =>
        // Assign value to each key
        jsonObject[key] = value
    );
    return jsonObject
}

// Post JSON to A.P.I
function postData(url,json){
    fetch(url,{
        method: 'POST',
        headers:{
            'Content-Type': 'application/json'        
        },
        body: json
    })
    .then(response => response.json())
    .catch(error => console.error('Error:', error))
    .then(response => console.log('Success: ',response));
}

let signupUrl = 'http://localhost:5000/api/v2/auth/signup',
    signupForm = document.getElementById("sign_up"),
    jsonFormData = JSON.stringify(formDataToJSON(signupForm));

// Signup a new User
signupForm.addEventListener("submit",function(event){
    event.preventDefault();
    postData(signupUrl,jsonFormData)
});
