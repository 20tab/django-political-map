document.addEventListener("DOMContentLoaded", function() {
  politicalplaces.init();

  // This would be the place to add custom events for the inline formsets, e.g:
  // 
  // django.jQuery(document).on('formset:added', function(evt, row, formset_name) {
  //   politicalplaces.addNewWidget(row[0].querySelector('.widget'), formset_name);
  // });
});