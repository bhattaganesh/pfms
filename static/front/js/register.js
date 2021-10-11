const nameField  = document.querySelector('#name');
const emailField  = document.querySelector('#email');
const passwordField  = document.querySelector('#password');
const cpasswordField  = document.querySelector('#cpassword');
const nameFeedbackArea = document.querySelector('.name-feedback');
const emailFeedbackArea = document.querySelector('.email-feedback');
const passwordFeedbackArea = document.querySelector('.password-feedback');
const cpasswordFeedbackArea = document.querySelector('.cpassword-feedback');
const submitBtn = document.querySelector('.submit-btn');
// const emailSuccessFeedbackArea = document.querySelector('.email-success-feedback');

nameField.addEventListener("focusout", (e) => {
    const nameVal = e.target.value;


    nameField.classList.remove('is-invalid');
    nameFeedbackArea.classList.add('d-none')
    nameFeedbackArea.innerHTML = "";

    if(nameVal.length > 0){
        fetch("/validate-name/", {
            body: JSON.stringify({ "name": nameVal }),
            method: "POST"
        })
        .then((res) => res.json())
        .then((data) => {
            if(data.name_error){
                nameField.classList.add('is-invalid');
                nameFeedbackArea.classList.add('d-block');
                nameFeedbackArea.innerHTML = `<p>${data.name_error}</p>`;
                submitBtn.disabled = true;

            }else{
                submitBtn.removeAttribute('disabled');
            }
        })
    }
});

// for email

emailField.addEventListener("focusout", (e) => {
    const emailVal = e.target.value;

    // emailSuccessFeedbackArea.textContent = `Checking ${emailVal}`;
    // emailSuccessFeedbackArea.classList.add('d-block');


    emailField.classList.remove('is-invalid');
    emailFeedbackArea.classList.add('d-none');
    emailFeedbackArea.innerHTML = "";

    if(emailVal.length > 0){
        fetch("/validate-email/", {
            body: JSON.stringify({ "email": emailVal }),
            method: "POST"
        })
        .then((res) => res.json())
        .then((data) => {
            // emailSuccessFeedbackArea.classList.add('d-none');
            if(data.email_error){
                emailField.classList.add('is-invalid');
                emailFeedbackArea.classList.add('d-block');
                emailFeedbackArea.innerHTML = `<p>${data.email_error}</p>`;
                submitBtn.disabled = true;

            }else{
                submitBtn.removeAttribute('disabled');
            }
        })
    }
});

passwordField.addEventListener("focusout", (e) => {
    const passwordVal = e.target.value;

    passwordField.classList.remove('is-invalid');
    passwordFeedbackArea.classList.add('d-none')
    passwordFeedbackArea.innerHTML = "";

    if(passwordVal.length > 0){
        fetch("/validate-password/", {
            body: JSON.stringify({ "password": passwordVal }),
            method: "POST"
        })
        .then((res) => res.json())
        .then((data) => {
            if(data.password_error){
                passwordField.classList.add('is-invalid');
                passwordFeedbackArea.classList.add('d-block');
                passwordFeedbackArea.innerHTML = `<p>${data.password_error}</p>`;
                submitBtn.disabled = true;

            }else{
                submitBtn.removeAttribute('disabled');
            }
        })
    }
});

cpasswordField.addEventListener("keyup", (e) => {
    const cpasswordVal = e.target.value;
    let pass = document.querySelector('#password').value;


    cpasswordField.classList.remove('is-invalid');
    cpasswordFeedbackArea.classList.add('d-none')
    cpasswordFeedbackArea.innerHTML = "";

    if(cpasswordVal.length > 0){
        fetch("/validate-cpassword/", {
            body: JSON.stringify({ "cpassword": cpasswordVal, "password": pass }),
            method: "POST"
        })
        .then((res) => res.json())
        .then((data) => {
            if(data.cpassword_error){
                cpasswordField.classList.add('is-invalid');
                cpasswordFeedbackArea.classList.add('d-block');
                cpasswordFeedbackArea.innerHTML = `<p>${data.cpassword_error}</p>`;
                submitBtn.disabled = true;

            }else{
                submitBtn.removeAttribute('disabled');
            }
        })
    }
});
