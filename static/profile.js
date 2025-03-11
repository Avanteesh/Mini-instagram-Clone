(function()  {
  const editUserProfile = document.querySelector("#edit-user-profile");
  const updateProfileDialog = document.querySelector(".update-profile-dialog");
  const closeDialogBtn = document.querySelector("#close-dialog");
  const userPosts = document.querySelectorAll("#users-posts-display");
  const setStatusBtn = document.querySelector("#set-status-btn");
  const followUser = document.querySelector("#follow-user");

  if (editUserProfile !== null)  {
    editUserProfile.addEventListener("click", function(evt) {
      updateProfileDialog.showModal();
    });
  }

  if (closeDialogBtn !== null)  {
    closeDialogBtn.addEventListener("click", function(evt)  {
      if (window.confirm("Are you sure you want to cancel?"))  
        updateProfileDialog.close();
    });
  }

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

  if (followUser !== null)  {
    const parenturl = new URL(window.location.href);
    followUser.addEventListener("click", function(evt)  {
      if (evt.isTrusted === false)
        return;
      fetch(`/follow?username=${parenturl.searchParams.get("username")}`, {
        method: 'PUT', headers: {'Content-Type': 'application/json'}
      }).then((res) => {
        return res.json()
      })
      window.location.reload();
      window.location.href = `/profile?username=${parenturl.searchParams.get("username")}`;
    }, false)
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

