$(function(){
	InitCtrlCSS();
});

function InitCtrlCSS(){
	var ctrlSelect = $("select");
	for(var i=0;i<ctrlSelect.length;i++){
		ctrlSelect[i].className = "form-control";
	}

	var ctrlText = $("input[type='text']");
	for(var i=0;i<ctrlText.length;i++){
		ctrlText[i].className = "form-control";
	}

    var ctrlText = $("input[type='number']");
    for(var i=0;i<ctrlText.length;i++){
            ctrlText[i].className = "form-control";
    }
}




$("#btnCPPool").click(function(){

	var src_pool_id = $("#selSrcPool").val();
	var dest_pool_id = $("#selDestPool").val();

	if(src_pool_id == dest_pool_id){
		showTip("error","Failed to copy pool: src_pool, dest_pool cannot be the same!")
		return  false;
	}
	var data = {
			"storage_pools":[]
	}
    var pool = {
                'src_pool_id':src_pool_id,
                'dest_pool_id':dest_pool_id,
			}
	data["storage_pools"].push(pool)

	var postData = JSON.stringify(data);
	token = $("input[name=csrfmiddlewaretoken]").val();
	$.ajax({
		type: "post",
		url: "/dashboard/vsm/poolsmanagement/cp_pool_action/",
		data: postData,
		dataType:"json",
		success: function(data){
				if(data.error_code.length == 0){
                    window.location.href="/dashboard/vsm/poolsmanagement/";
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
})