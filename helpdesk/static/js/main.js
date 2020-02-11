document.addEventListener('DOMContentLoaded', function() {
  // INITIALIZING MATERIALIZE ELEMENTS
  var selects = document.querySelectorAll('select');
  M.FormSelect.init(selects);

  var datepickers = document.querySelectorAll('.datepicker');
  M.Datepicker.init(datepickers, {format: 'yyyy-mm-dd', showClearBtn: true});

  var dropdowns = document.querySelectorAll('.dropdown-trigger');
  M.Dropdown.init(dropdowns);

  var collapsibles = document.querySelectorAll('.collapsible');
  M.Collapsible.init(collapsibles);


  //SCROLLS THE SEARCH TICKET TABLE INTO VIEW AFTER SEARCHING
  let searchTicketsWrapper = document.querySelector('.searchTicketsWrapper');
  if (searchTicketsWrapper) {
      searchTicketsWrapper.scrollIntoView({block: "center"});
  }

});
