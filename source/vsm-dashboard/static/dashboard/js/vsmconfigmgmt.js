$(function(){
   //LoadFilterTextbox
    LoadFilterTextbox();

});

//CheckFilterStatus
function LoadFilterTextbox(){
    var filterRow = "";
    filterRow += "  <div class='table_search client'>";
    filterRow += "      <input id='txtFilter' type='text' class='form-control' placeHolder='name' />";
    filterRow += "      <button id='btnFilter' class='btn btn-primary' onClick='FilterConfigList()'>filter</button>";
    filterRow += "  </div>";

    $(".table_actions.clearfix").append(filterRow);
}

function FilterConfigList(){
    var name = $("#txtFilter").val();
    if(name == ""){
        window.location.href = "/dashboard/vsm/vsm_config_mgmt/";
        alert(name)
    }
    else{
        window.location.href = "/dashboard/vsm/vsm_config_mgmt/?name="+name;
        alert(name)
    }
}

$(".update").click(function(){
 	token = $("input[name=csrfmiddlewaretoken]").val();

 	var config_id = $(this).parent().parent().attr('configid');
	var config_name = $(this).parent().parent().attr('name');
	var config_section = $(this).parent().parent().attr('section');
    var config_value = $(this).parent().parent().find('.new_value').val();
	var config_description = $(this).parent().parent().attr('description');
    var strJSONData = JSON.stringify({"config_id":config_id,
		"config_section":config_section,
		"config_value":config_value,
		"config_description":config_description
	});

    $.ajax({
        data: strJSONData,
        type: "post",
        dataType: "json",
        url: "/dashboard/vsm/vsm_config_mgmt/update",
        success: function (data) {
            if(data.status == "success"){
                showTip("success","set "+config_name+"="+config_value+" successfully");
            }
            else{
                showTip("error","set "+config_name+"="+config_value+" error");
            }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
             showTip("error","set "+config_name+"="+config_value+" error");
        },
        headers: {
          "X-CSRFToken": token
        },
        complete: function(){

        }
    });
});
