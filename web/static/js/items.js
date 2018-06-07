function deleteItem(item) {
  console.log(item);
  $.ajax({
    url: '/item?mod=del',
    type: 'POST',
    dataType: 'html',
    data: {item: item}
  })
  .done(function(data) {
    console.log("success", data);
  })
  .fail(function(req, res, err) {
    if(err){
      console.log(err);
      alert('An error has been thrown by the AJAX call');
    }
  })
  .always(function(req, res, err) {
    location.reload();
    console.log("complete");
  });
}
