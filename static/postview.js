/*
  author '@' avanteesh
  for post viewers in HTML page!
*/
(function() {
  // HTML elements and gloabals
  const deletePostButton = document.querySelector("#delete-post-btn");
  const postCommentsDialog = document.querySelector(".post-comments-dialog");
  const showCommentsBtn = document.querySelector("#add-new-comment-btn");
  const closeCommentDialogBtn = document.querySelector("#close-post-comment-dialog");
  const likeButton = document.querySelector("#update-post-likes");
  const commentInputBox = document.querySelector("#CommentTextBox");
  const addNewCommentBtn = document.querySelector("#add-new-comment");
  const deleteCommentsNodes = document.querySelectorAll("#delete-comment-button");
  const postmetadata = new URL(window.location.href).pathname.split("/");
  const editCommentsNodes = document.querySelectorAll("#edit-comment-button");
  const sharePostBtn = document.querySelector("#share-post");

  // all events will Only respond if are Trusted!
  
  if (deletePostButton !== null)  {
    deletePostButton.addEventListener("click", function()  {
      const dialog = document.querySelector(".confirm-dialog");
      dialog.showModal();    
      const confirmPostDeletion = document.querySelector("#confirm-to-delete-post");
      const cancelPostDeletion = document.querySelector("#cancel-post-deletion");
      cancelPostDeletion.addEventListener("click", function(evt)  {
        if (evt.isTrusted === false)
          return;
        dialog.close();
      }, false);
      confirmPostDeletion.addEventListener("click", function(evt)  {
        if (evt.isTrusted === false)  
          return;  // if the button was not clicked by user but click invoked through function call
        fetch(`/delete-post/${postmetadata.at(-1)}`, {
          method: 'DELETE'
        }).then((res) => {
          return res.json() 
        });
        window.location.href = "/profile/main";
      }, false)
    });
  }

  if (deleteCommentsNodes !== null)  {
    deleteCommentsNodes.forEach((deleteCommentBtn) => {
      deleteCommentBtn.addEventListener("click", function(evt)  {
        if (evt.isTrusted === false) 
          return; // if the button was not clicked by user but click invoked through function call
        if (window.confirm("Are you sure you want to delete this comment?") == false)  
          return;
        const btnkey = deleteCommentBtn.getAttribute("key");
        // DELETE request is similar to GET, But using it certainly makes sense!
        fetch(`/delete-comment/${postmetadata.at(-1)}/${btnkey}`, {
          method: 'DELETE'
        }).then((res) => {
          return res.json();
        });
        window.location.reload();
      })
    })
  }  

  if (editCommentsNodes !== null)  {
    editCommentsNodes.forEach((editCommentBtn) => {
      editCommentBtn.addEventListener("click", function(evt)  {
        if (evt.isTrusted === false)
          return;
        const parentElement = editCommentBtn.parentElement.previousElementSibling;
        commentInputBox.value = parentElement.textContent;
        commentInputBox.focus();
        closeCommentDialogBtn.addEventListener("click", function(evt)  {
        if (window.confirm("Are you sure you want to discard this?"))  {
          commentInputBox.value = "";
          postCommentsDialog.close();
          return;  
        }
        addNewCommentBtn.addEventListener("click", function(evt)  {
          if (evt.isTrusted === false) 
            return;
            fetch(`/edit-comment/?comment_id=${editCommentBtn.getAttribute("key")}&comment=${commentInputBox.value}`, {
              method: 'PUT', headers: {'Content-Type': 'application/json'}
            }).then((res) => {
              return res.json();
            });
          }, false);
        });
      })
    })
  }

  likeButton.addEventListener("click", function(evt)  {
    if (evt.isTrusted === false) 
      return;
    fetch(`/like-post?post_id=${postmetadata.at(-1)}`, {
      method: 'PUT', headers: {'Content-Type': 'application/json'}
    }).then((res) => {
      return res.json();
    });
    window.location.reload();
  }, false); 

  showCommentsBtn.addEventListener("click", function(evt) {
    if (evt.isTrusted === false)
      return;
    postCommentsDialog.showModal();
  }, false);

  closeCommentDialogBtn.addEventListener("click", function(evt)  {
    if (evt.isTrusted === false)
      return;
    postCommentsDialog.close();
  }, false);

  sharePostBtn.addEventListener("click", function(evt) {
    if (evt.isTrusted === false)
      return;
    navigator.clipboard.writeText(window.location.href);  
    window.alert("Link Copied successfully!!");
  }, false);

  addNewCommentBtn.addEventListener("click", function(evt)  {
    if (evt.isTrusted === false)
      return;
    if (commentInputBox.value == "") 
      return;
    fetch(`/new-comment?post_id=${postmetadata.at(-1)}&comment=${commentInputBox.value}`, {
      method: 'PUT', headers: {'Content-Type': 'application/json'}
    }).then((res) => res.json());
    window.location.reload();
  }, false);
  
})();
