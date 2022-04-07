var map;
var markers = [];
var panel;
var map_canvas;
var search_map;
var address_input;


function initMap() {
  console.log("---initMap");
  map = new google.maps.Map(map_canvas, {
    zoom: 4,
    minZoom: 2
  });
  if(address_input.val()!=""){
      geoCode(address_input.val(), map);
  }
  readInput(map);
}

function addAndResetMarker(location){
  console.log("---addAndResetMarker");
  deleteMarkers();
  addMarker(location);
}

function addMarker(location){
  console.log("---addMarker");
  var marker = new google.maps.Marker({
    position: location,
    map: map
  });
  markers.push(marker);
}

function setMapOnAll(map){
  console.log("---setMapOnAll");
  for(var i = 0; i < markers.length; i++){
    markers[i].setMap(map)
  }
}

function clearMarkers(){
  console.log("---clearMarkers");
  setMapOnAll(null);
}

function deleteMarkers(){
  console.log("---deleteMarkers");
  clearMarkers();
  markers = []
}

function updatePanel(results, map){
  console.log("---updatePanel: ", results);
  var html_panel = "<ul>";
  for(var i = 0; i < results.length; i++){
    html_panel += "<li class='result_component'>"+results[i].formatted_address+"</li>";
  }
  panel.html(html_panel+"</ul>");
  $(".result_component").click(function(){
    geoCode($(this).text(), map)
  })
}

function logErrorPanel(error){
  panel.html(error);
}

function geoCode(address, map){
  console.log("---geoCode:", address);
  var geocoder = new google.maps.Geocoder();
  var res = geocoder.geocode(
    {'address': address},
    function(results, status){
      if(status==google.maps.GeocoderStatus.OK){
        if(results.length == 1){
          deleteMarkers();
          map.setCenter(results[0].geometry.location);
          if(results[0].geometry.bounds){
              map.fitBounds(results[0].geometry.bounds)
          }
          addMarker(results[0].geometry.location);
          panel.html("");
          address_input.val(results[0].formatted_address);
        }else{
          updatePanel(results, map);
        }
      }else{logErrorPanel("Gmaps Error:"+status);}
    }
  )
}

function readInput(map){
  console.log("---readInput");
  search_map.click(function(){
      console.log('search_map.click');
      var value = address_input.val()
      geoCode(value, map);
    })
}
