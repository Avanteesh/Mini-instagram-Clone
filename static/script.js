(function()  {
  const showPasswordCheck = document.querySelector("#showPasswordCheckBox");
  const inputPasswordEle = document.querySelector("#inputPassword");
  
  showPasswordCheck.addEventListener("change", function(evt)  {
    inputPasswordEle.type = (evt.target.checked == true)? "text":"password";
  });
  
})();
