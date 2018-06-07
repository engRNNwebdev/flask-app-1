$(document).ready(function() {
  var picker = $('.selectpicker');
  var input = $('#inputQuery');
  picker.selectpicker();
  picker.on('change', function(e) {
    searchLog(this.value);
  });
  var dump = document.getElementById('logdump');
  var div = dump.getElementsByTagName('div');
});

function searchLog (filter) {
  // Declare variables
  var dump, div, a, i;
  dump = document.getElementById('logdump');
  console.log(filter);
  div = dump.getElementsByTagName('div');
  // Loop through all list items, and hide those who don't match the search query
  for (i = 0; i < div.length; i++) {
    a = div[i].getElementsByTagName('p')[0]
    if (a.innerHTML.toUpperCase().indexOf(filter) > -1) {
      div[i].style.display = '';
    } else {
      div[i].style.display = 'none';
    }
  }
  return false;
}
function clearLogDump () {$('#logdump').empty();return false;}
