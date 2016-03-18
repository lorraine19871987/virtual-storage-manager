


$(document).ajaxStart(function(){
    //load the spin
    ShowSpin();
});
function CreateRBDGroup(){
	//Check the field is should not null
	if($("#txtGroupName").val() == "" || $("#txtComments").val() == ""){
		showTip("error","The field is marked as '*' should not be empty");
		return  false;
	}
	var data = {
			"rbd_groups":[]
	}
    var rbd_group = {
                'name':$("#txtGroupName").val(),
                'comments':$("#txtComments").val(),
			}
	data["rbd_groups"].push(rbd_group)
	var postData = JSON.stringify(data);
	token = $("input[name=csrfmiddlewaretoken]").val();
	$.ajax({
		type: "post",
		url: "/dashboard/vsm/rbdgroups-management/add_rbd_group/",
		data: postData,
		dataType:"json",
		success: function(data){
				//console.log(data);
                if(data.error_code.length == 0){
                    window.location.href="/dashboard/vsm/rbdgroups-management/";
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

$(document).ajaxStart(function(){
    //load the spin
    ShowSpin();
});