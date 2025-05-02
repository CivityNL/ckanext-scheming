
this.ckan.module('scheming_checkbox', function ($) {
  return {
    initialize: function () {

    var field_name_list_to_toggle = this.options.fields.split(',');

    this.el.on('click', function(){
        field_name_list_to_toggle.forEach(field_name=>{
            var element_name = "field-" + field_name
            var element = $("#"+element_name).parent().parent()
            if (this.checked){
                element.hide()
            }
            else{
                element.show()
            }
        });
    });
    }
  };
});