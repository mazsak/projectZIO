function validateLogin() {
  let login = document.forms["registration_form"]["login"].value;
  if (login.length < 6) {
    fillErrorMessage("Login must be at least 6 characters long", 'error_message_login');
    return false;
  } else if (login.length > 149 ) {
    fillErrorMessage("Login to long", 'error_message_login');
    return false;
  }
  fillErrorMessage("", 'error_message_login')
  return true;
}

function validatePasswords() {
  let password = document.forms["registration_form"]["password"].value;
  let confirm_password = document.forms["registration_form"]["confirm_password"].value;
  if (password.length < 6 || confirm_password.length < 6) {
    fillErrorMessage("Passwords must be at least 6 characters long", 'error_message_password');
    return false;
  }
  else if (password.length > 149 || confirm_password.length > 149) {
    fillErrorMessage("Passwords to long", 'error_message_password');
    return false;
  } else if (password !== confirm_password) {
      fillErrorMessage ("Passwords did not match", 'error_message_password')
      return false;
  }
  fillErrorMessage("", 'error_message_password')
  return true;
}

function fillErrorMessage (msg, id) {
  let ele = document.getElementById(id);
  ele.innerHTML = msg;
  if (msg === ""){
    ele.hidden = true;
    document.getElementById('create_btn').disabled = false;
  }else{
    ele.hidden = false;
    document.getElementById('create_btn').disabled = true;
  }
}

function validateForm() {
  let is_login_valid = validateLogin();
  if (is_login_valid) {
    let is_password_valid = validatePasswords();
  }
}