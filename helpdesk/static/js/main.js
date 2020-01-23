// <!-- Initializing select elements on document ready -->
document.addEventListener('DOMContentLoaded', function() {
  var selects = document.querySelectorAll('select');
  M.FormSelect.init(selects);
  var datepickers = document.querySelectorAll('.datepicker');
  M.Datepicker.init(datepickers, {format: 'yyyy-mm-dd', showClearBtn: true});
  });
