
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
	data["rbds"].push(rbd)
	var postData = JSON.stringify(data);
	token = $("input[name=csrfmiddlewaretoken]").val();
	$.ajax({
		type: "post",
		url: "/dashboard/vsm/rbds-management/create_new_rbd/",
		data: postData,
		dataType:"json",
		success: function(data){
				//console.log(data);
                if(data.error_code.length == 0){
                    window.location.href="/dashboard/vsm/rbds-management/";
                    showTip("info",data.info);
                }
                else{
                    showTip("error",data.error_msg);
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
		url: "/dashboard/vsm/rbds-management/get_image_formt/",
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
                        item.value = pool_list[i][0];
                        item.text = pool_list[i][1];
                        $("#selPool")[0].options.add(item);
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