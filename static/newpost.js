const selection = document.querySelector("#postVisibility");
const postVisibilityLabel = document.querySelector(".post-visibility-label");

selection.addEventListener("change", function(evt)  {
  if (evt.target.value === "private") 
    postVisibilityLabel.textContent = "(only you can view the post)";
  else
    postVisibilityLabel.textContent = "(Everyone can view the post)";
});
