const editUserProfile = document.querySelector("#edit-user-profile");
const updateProfileDialog = document.querySelector(".update-profile-dialog");
const closeDialogBtn = document.querySelector("#close-dialog");
const userPosts = document.querySelectorAll("#users-posts-display");

editUserProfile.addEventListener("click", function(evt) {
  updateProfileDialog.showModal();
});

closeDialogBtn.addEventListener("click", function(evt)  {
  if (window.confirm("Are you sure you want to cancel?"))  
    updateProfileDialog.close();
});

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


