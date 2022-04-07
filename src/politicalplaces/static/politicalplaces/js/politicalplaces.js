document.addEventListener("DOMContentLoaded", function() {
  politicalplaces.init();
});

var politicalplaces = (function() {
  'use strict';

  var widgets = [];
  var options = {
      map_zoom: 4,
      map_min_zoom: 2,
  };

  function init() {
    var widgetsDOMElements = document.querySelectorAll('.politicalplace-widget');
    for (var i = widgetsDOMElements.length - 1; i >= 0; i--) {
      addNewWidget(widgetsDOMElements[i]);
    }
    if (window.django && window.django.jQuery) {
      window.django.jQuery(document).on('formset:added', onFormsetAdded);
    }
  }

  function addEventListeners(widget) {
      widget.search_button.addEventListener('click', onSearchClick);
      widget.panel.addEventListener('click', onResultClick);
      widget.address_input.addEventListener('keydown', onInputKeyDown);
  }

  function onSearchClick(evt) {
    var id = evt.currentTarget.parentElement.getAttribute('data-id');
    var widget = widgets.find(function(widget) { return widget.id === id })
    var query = widget.address_input.value;
    geoCode(query, widget);
  }
  
  function onResultClick(evt) {
    var id = evt.currentTarget.parentElement.parentElement.getAttribute('data-id');
    var widget = widgets.find(function(widget) { return widget.id === id })
    if (evt.target.classList.contains('panel__result')) {
      geoCode(evt.target.innerText, widget);
    }
  }
  
  function onFormsetAdded(evt, row, formset_name) {
    if (row[0].querySelector('.politicalplace-widget')) {
      addNewWidget(row[0].querySelector('.politicalplace-widget'), formset_name);
    }
  }

  function onInputKeyDown(evt) {
    var id = evt.currentTarget.parentElement.getAttribute('data-id');
    var widget = widgets.find(function(widget) { return widget.id === id })
    if (evt.keyCode === 13) {
      evt.preventDefault();
      widget.search_button.click();
    }
  }

  function addNewWidget(widgetDOMElement, formset_name) {
    var widget = {};
    widget.panel = widgetDOMElement.querySelector('.widget__place__panel');
    widget.map_canvas = widgetDOMElement.querySelector('.widget__place__map');
    widget.search_button = widgetDOMElement.querySelector('.widget__search');
    widget.address_input = widgetDOMElement.querySelector('input'); //this needs a class      
    widget.map = new google.maps.Map(widget.map_canvas, {
      zoom: options.map_zoom,
      minZoom: options.map_min_zoom,
    });
    // if the widget is added from an inline formset, get the id from the dynamically added input name...
    if (widgetDOMElement.getAttribute('data-id').indexOf('__prefix__') >= -1 && formset_name) {
      widget.id = widget.address_input.id;
      // and update the data-id;
      widgetDOMElement.setAttribute('data-id', widget.id);
    // ...otherwise get it from the data-id of the template
    } else {
      widget.id = widgetDOMElement.getAttribute('data-id');
    }
    if (widget.address_input.value !== '') {
      geoCode(widget.address_input.value, widget);
    }
    addEventListeners(widget);
    widgets.push({
      id: widget.id,
      panel: widget.panel,
      map_canvas: widget.map_canvas,
      search_button: widget.search_button,
      address_input: widget.address_input,
      map: widget.map,
      markers: [],
    });
  }

  function addMarker(location, widget) {
    var marker = new google.maps.Marker({
      position: location,
      map: widget.map,
    });
    widget.markers.push(marker);
  }

  function setMapOnAll(widget, delete_marker) {
    if (widget.markers) {
      for (var i = widget.markers.length - 1; i >= 0; i--) {
        widget.markers[i].setMap(delete_marker ? null : widget.map);
      }
    }
  }

  function clearMarkers(widget) {
    setMapOnAll(widget, true);
  }

  function deleteMarkers(widget) {
    clearMarkers(widget);
    widget.markers = [];
  }

  function updatePanel(results, widget) {
    var html_panel = '<ul>';
    for (var i = 0; i < results.length; i++){
      html_panel += '<li class="panel__result">' + results[i].formatted_address + '</li>';
    }
    widget.panel.innerHTML = html_panel + '</ul>';
  }

  function logErrorPanel(error, widget){
    widget.panel.innerHTML = '<ul><li>' + error + '</li></ul>';
  }

  function geoCode(address, widget) {
    var geocoder = new google.maps.Geocoder();
    var res = geocoder.geocode({ address: address }, function(results, status) {
      if (status === google.maps.GeocoderStatus.OK) {
        if (results.length === 1) {
          deleteMarkers(widget);
          widget.map.setCenter(results[0].geometry.location);
          if (results[0].geometry.bounds) {
            widget.map.fitBounds(results[0].geometry.bounds)
          }
          addMarker(results[0].geometry.location, widget);
          widget.panel.innerHTML = '';
          widget.address_input.value = results[0].formatted_address;
        } else {
          updatePanel(results, widget)
        }
      } else {
        logErrorPanel('Gmaps Error: ' + status, widget);
      }
    });
  }

  return {
    init: init,
    addNewWidget: addNewWidget,
  };
}());