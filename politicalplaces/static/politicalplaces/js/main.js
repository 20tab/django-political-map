$(function($) {

  politicalplaces.init();
  $(document).on('formset:added', function(event, $row, formsetName) {
          
              console.log(evt, $row, formsetName);
          
      });

});