//flag the tab
var _CURRENT_TAB = "";

$(function(){
   //LoadFilterTextbox
    LoadFilterTextbox();

    InitCtrlCSS();
    _CURRENT_TAB = $(".nav-tabs>li>a")[0].innerHTML;
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
        window.location.href = "/dashboard/vsm/ceph_config_mgmt/";
    }
    else{
        window.location.href = "/dashboard/vsm/ceph_config_mgmt/?name="+name;
    }
}

function InitCtrlCSS(){
    var ctrlSelect = $("select");
    for(var i=0;i<ctrlSelect.length;i++){
        ctrlSelect[i].className = "form-control";
    }

    var ctrlText = $("input[type='text']");
    for(var i=0;i<ctrlText.length;i++){
        ctrlText[i].className = "form-control";
    }
}

function SwitchTab(obj,tabname){
    //flag the tab
    _CURRENT_TAB = tabname;

    //show the current table
    $(".table-config").hide();
    $("#t"+tabname).show();

    //change the current section
    $(".nav-tabs>li").each(function(){
        this.className = "";
    });
    obj.className = "active";
}

function SelectAllCheckbox(obj,name){
    var checked = obj.checked;
    $("input[name="+name+"]").each(function(){
        this.checked = checked;
    })
}

$("#btnCreateCephConfig").click(function(){
	var name = $("#id_name").val();
	var value = $("#id_value").val();
	var category = $("#id_category").val();
    var section = $("#id_section").val();
    var alterable = $("#id_alterable")[0].checked;
    var description = $("#id_description").val();

	//Check the field is should not null
    if(name == "" || value == "" || category == "" || section == "" ){
        showTip("error","The field is marked as '*' should not be empty");
        return  false;
    }

	//Send the data and create
	var data = {
        "name":name,
        "value":value,
		"category":category,
        "section":section,
        "alterable":alterable,
        "description":description
	};
	var postData = JSON.stringify(data);

    //execuate post
    Post("create_ceph_config",postData);
});

function DeleteConfig(section_name){
    var config_id_list = [];
    $("input[name="+_CURRENT_TAB+"]").each(function(){
        if(this.checked == true){
            if(this.value!="on")
                config_id_list.push(this.value);
        }
    });

    var postData = JSON.stringify(config_id_list);

    //execuate post
    Post("delete_ceph_config",postData);
}

function DetectConfig(){
    var postData = JSON.stringify("");
    Post("detect_ceph_config", postData);
}


function Post(method,data){
    token = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
        data: data,
        type: "post",
        dataType: "json",
        url: "/dashboard/vsm/ceph_config_mgmt/"+method+"/",
        success: function (data) {
            if(data.status == "OK"){
                window.location.href="/dashboard/vsm/ceph_config_mgmt/";
                showTip("info", data.message)
            } else if(data.status == "Error") {
                showTip("error", data.message)
            }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            if(XMLHttpRequest.status == 500)
                showTip("error","INTERNAL SERVER ERROR")
        },
        headers: {
          "X-CSRFToken": token
        },
        complete: function(){

        }
    });
}

$(".update").click(function(){
 	token = $("input[name=csrfmiddlewaretoken]").val();

 	var config_id = $(this).parent().parent().attr('configid');
	var config_name = $(this).parent().parent().attr('name');
	var config_section = $(this).parent().parent().attr('section');
    var config_value = $(this).parent().parent().find('.form-control').val();
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
        url: "/dashboard/vsm/ceph_config_mgmt/update",
        success: function (data) {
            if(data.status == "success"){
                showTip("success","set "+config_section+"'s "+config_name+"="+config_value+" successfully");
            }
            else{
                showTip("error","set "+config_section+"'s "+config_name+"="+config_value+" error");
            }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
             showTip("error","set "+config_section+"'s "+config_name+"="+config_value+" error");
        },
        headers: {
          "X-CSRFToken": token
        },
        complete: function(){

        }
    });
});