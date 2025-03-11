(function()  {
  const editUserProfile = document.querySelector("#edit-user-profile");
  const updateProfileDialog = document.querySelector(".update-profile-dialog");
  const closeDialogBtn = document.querySelector("#close-dialog");
  const userPosts = document.querySelectorAll("#users-posts-display");
  const setStatusBtn = document.querySelector("#set-status-btn")

  editUserProfile.addEventListener("click", function(evt) {
    updateProfileDialog.showModal();
  });

  closeDialogBtn.addEventListener("click", function(evt)  {
    if (window.confirm("Are you sure you want to cancel?"))  
      updateProfileDialog.close();
  });

  if (setStatusBtn !== null)  {
    const statusDialog = document.querySelector(".set-status-dialog");
    const closeDialogBtn = document.querySelector("#close-set-status-dialog");
    const emojiFormInput = document.querySelector("#emojiformFloating");
    const statusInputText = document.querySelector("#status-text-inp");
    
    setStatusBtn.addEventListener("click", function(evt)  {
      if (evt.isTrusted === false)
        return;
      statusDialog.showModal();
    }, false);

    closeDialogBtn.addEventListener("click", function(evt) {
      if (evt.isTrusted === false)
        return;
      statusDialog.close();
    }, false);

    emojiFormInput.addEventListener("change", function(evt)  {
      statusInputText.value += evt.target.value;
    }, false);
  }

  userPosts.forEach((userPost) => {
    userPost.addEventListener("mouseover", 
      function(evt) {
        this.style.cursor = "pointer";
      }, 
    false);
    userPost.addEventListener("mouseout", 
      function(evt) {
        this.style.cursor = "default";
      }, 
    false);
    userPost.addEventListener("click", 
      function(evt) {
        const [target, userName] = [this.firstElementChild.getAttribute("alt"), document.querySelector("#users-username")];
        window.location.href = `/post/${userName.textContent.replace("@","")}/${target}`;
      }
    );
  })

})();

