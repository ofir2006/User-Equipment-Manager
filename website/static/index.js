function deleteItem(itemId) {
  check = confirm("Are you sure you want to delete this item?");  
  if(check){
  fetch("/delete-item", {
      method: "POST",
      body: JSON.stringify({ itemId: itemId }),
    }).then((_res) => {
      location.reload();
    });
  }
}
  function deleteUser(userId) {
    check = confirm("Are you sure you want to delete this item?");  
    if(check){
    fetch("/delete-user", {
      method: "POST",
      body: JSON.stringify({ userId: userId }),
    }).then((_res) => {
      window.location.href = "/user-management";
    });
  }
}