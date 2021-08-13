      //make sure map is a global variable
      var map;

      function ajax_loading(element) {
          var t = $(element);
          var offset = t.offset();
          var dim = {
              left:    offset.left,
              top:    offset.top,
              width:    t.outerWidth(),
              height:    t.outerHeight()
          };
          $('<div class="ajax_loading"></div>').css({
              position:    'absolute',
              left:        dim.left + 'px',
              top:        dim.top + 'px',
              width:        dim.width + 'px',
              height:        dim.height + 'px'
          }).appendTo(document.body).show();


      }
      function refresh_tree() {
        ajax_loading('#tree');
        $('#tree').load('/simple_locations/render_tree/',function(){
             $('.ajax_loading').remove();
        });
      }
      
      function load_add_location() {

          ajax_loading('#edit_location');
        $('#edit_location').load('/simple_locations/add/',function(){
           $('.ajax_loading').remove();
        });
      }
      
      function load_add_location_child(location_id) {
          ajax_loading('#edit_location');
        $('#edit_location').load('/simple_locations/add/' + location_id + '/',function()
        {
           $('.ajax_loading').remove();
        });
      }
      
      function load_edit_location(location_id) {
          ajax_loading('#edit_location');
        $('#edit_location').load('/simple_locations/edit/' + location_id + '/',function(){
           $('.ajax_loading').remove();
        });
      }
      
      function add_location(link) {
          form = $(link).parents("form");
          form_data = form.serializeArray();
          $('#edit_location').load(form.attr("action"), form_data, function() { refresh_tree() });      
      }
      
      function save_location(link) {
          form = $(link).parents("form");
          form_data = form.serializeArray();
          $('#edit_location').load(form.attr("action"), form_data, function() { refresh_tree() });
      }
      
      function delete_location(location_id) {
    	  if (confirm("Are you sure?")) {
        $.ajax({'async':false,
              'cache':false,
              'type':'POST',
              'url':'/simple_locations/delete/' + location_id + '/',
              'success': function() { refresh_tree(); load_add_location(); }  
             });
    	  } else {
    		  return false;
    		  
    	  }
      }
      
      $(document).ready(function() {
        refresh_tree();
        load_add_location();   
       
      });