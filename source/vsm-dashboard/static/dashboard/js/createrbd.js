
$(function(){
    GetPool();
    GetImageFormat();
})


function CreateRBD(){
	//Check the field is should not null
	if($("#txtRBDName").val() == ""){
		showTip("error","The field is marked as '*' should not be empty");
		return  false;
	}
	var data = {
			"rbds":[]
	}
    var rbd = {
                'pool':$("#selPool").val(),
                'image':$("#txtRBDName").val(),
                'size' :$("#txtImageSize").val(),
                'format':$("#selFormat").val(),
                'objects':'',
                'order':22,
			}
	data.rbds.append(rbd)
	var postData = JSON.stringify(data);
	token = $("input[name=csrfmiddlewaretoken]").val();
	$.ajax({
		type: "post",
		url: "/dashboard/vsm/poolsmanagement/create_replicated_pool_action/",
		data: postData,
		dataType:"json",
		success: function(data){
				//console.log(data);
                if(data.status == "OK"){
                    window.location.href="/dashboard/vsm/poolsmanagement/";
                }
                else{
                    showTip("error",data.message);
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

function GetImageFormat(){
    $.ajax({
		type: "get",
		url: "/dashboard/vsm/rbds_management/get_image_formt/",
		data: "",
		dataType:"json",
		success: function(data){
				console.log(data);
                var image_formt_list = data.image_formt_list;
                if(image_formt_list.length == 0){
                    //TODO Nothing
                }
                else{
                    $("#selFormat")[0].options.length = 0;
                    for(var i=0;i<image_formt_list.length;i++){
                        var item = new Option()
                        item.value = image_formt_list[i][0];
                        item.text = image_formt_list[i][1];
                        $("#selFormat")[0].options.add(item);
                    }

                }
		   	},
		error: function (XMLHttpRequest, textStatus, errorThrown) {
				if(XMLHttpRequest.status == 500)
                	showTip("error","INTERNAL SERVER ERROR")
			},
		headers: {
			},
		complete: function(){

		}
    });
}

function GetPool(){
    $.ajax({
		type: "get",
		url: "/dashboard/vsm/poolsmanagement/list_pools_for_sel_input/",
		data: "",
		dataType:"json",
		success: function(data){
				console.log(data);
                var pool_list = data.pool_list;
                if(pool_list.length == 0){
                    //TODO Nothing
                }
                else{
                    $("#selPool")[0].options.length = 0;
                    for(var i=0;i<pool_list.length;i++){
                        var item = new Option()
                        item.value = storage_group_list[i][0];
                        item.text = storage_group_list[i][1];
                        $("#selStorageGroup")[0].options.add(item);
                    }

                }
		   	},
		error: function (XMLHttpRequest, textStatus, errorThrown) {
				if(XMLHttpRequest.status == 500)
                	showTip("error","INTERNAL SERVER ERROR")
			},
		headers: {
			},
		complete: function(){

		}
    });
}


$(document).ajaxStart(function(){
    //load the spin
    ShowSpin();
});