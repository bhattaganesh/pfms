const emailField  = document.querySelector('#email');
const passwordField  = document.querySelector('#password');
const emailFeedbackArea = document.querySelector('.email-feedback');
const passwordFeedbackArea = document.querySelector('.password-feedback');
const submitBtn = document.querySelector('.submit-btn');

emailField.addEventListener("focusout", (e) => {
    const emailVal = e.target.value;

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

