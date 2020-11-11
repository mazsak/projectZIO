function validateLogin() {
  let login = document.forms["registration_form"]["login"].value;
  if (login.length < 6) {
    fillErrorMessage("Name must be at least 6 characters long");
    return false;
  }
  fillErrorMessage("")
  return true;
}

function validatePasswords() {
  let password = document.forms["registration_form"]["password"].val();
  let confirm_password = document.forms["registration_form"]["confirm_password"].val();
  if (password.length < 6 || confirm_password.length < 6) {
    fillErrorMessage("Passwords must be at least 6 characters long");
    return false;
  } else if (password !== confirm_password) {
      fillErrorMessage ("Password did not match")
      return false;
  }
  fillErrorMessage("")
  return true;
}

function fillErrorMessage (msg) {
  let ele = document.getElementById('error_message');
  ele.innerHTML = msg;
}

function validateForm() {
  let is_login_valid = validateLogin()
  if (is_login_valid) {
    validatePasswords()
  }
}