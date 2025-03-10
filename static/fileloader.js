const addProfilePicBtn = document.querySelector("#add-profile-photo-btn");
const profilePicInput = document.querySelector(".img-thumbnail");
const invisibleInput = document.querySelector(".invisible-input");

addProfilePicBtn.addEventListener("click", function(evt)  {
  evt.preventDefault();
  const input = document.createElement("input");
  input.type = "file";
  input.accept = "image/*";
  input.addEventListener("change", function() {
    const fileReader = new FileReader();
    const files = Array.from(input.files).at(0);
    fileReader.addEventListener("load", function()  {
      profilePicInput.src = fileReader.result;
      invisibleInput.value = fileReader.result;
    }, false);
    if (files) 
      fileReader.readAsDataURL(files);
  });
  input.click();
  input.remove();
}, false);


