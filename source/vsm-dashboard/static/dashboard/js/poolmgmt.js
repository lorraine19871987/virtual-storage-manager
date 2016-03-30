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

//remove pools
$("#btnRemovePools").click(function(){
	var storage_pool_id_list = {"storage_pool_id_list":[]}

	var is_selected = false;
	$("#storage_pool_list>tbody>tr").each(function(){
        if(this.children[0].children[0].checked) {
            is_selected = true;
            var storage_pool_id = this.children[0].children[0].value;
            storage_pool_id_list["storage_pool_id_list"].push(storage_pool_id);
        }
	})

    if(is_selected == false){
        showTip("warning","please select the Pool");
        return false;
    }

	token = $("input[name=csrfmiddlewaretoken]").val();
	$.ajax({
		type: "post",
		url: "/dashboard/vsm/poolsmanagement/remove_pools_action/",
		data: JSON.stringify(rbd_id_list),
		dataType:"json",
		success: function(data){
				//console.log(data);
                if(data.error_code.length == 0){
                    window.location.href="/dashboard/vsm/poolsmanagement/";
                    showTip("info",data.info);
                }
                else{
                    showTip("error",data.error_msg);
                }
		   	},
		error: function (XMLHttpRequest, textStatus, errorThrown) {
				if(XMLHttpRequest.status == 500){
					$("#divOSDTip").show();
					$("#divOSDTip")[0].innerHTML = XMLHttpRequest.statusText;
				}
			},
		headers: {
			"X-CSRFToken": token
			},
		complete: function(){

		}
    });
	return false;
});


$("#btnRemoveCacheTier").click(function(){
	var CachePoolID = $("#id_cache_tier_pool").val();
	var data = {
       	'cache_tier': {
            'cache_pool_id': CachePoolID
        }
    }

    var postData = JSON.stringify(data);
    token = $("input[name=csrfmiddlewaretoken]").val();
	$.ajax({
		type: "post",
		url: "/dashboard/vsm/poolsmanagement/remove_cache_tier_action/",
		data: postData,
		dataType:"json",
		success: function(data){
				console.log(data);
				window.location.href="/dashboard/vsm/poolsmanagement/";
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

    return false;
})

function ChangePoolQuota(checked){
	$("#txtPoolQuota")[0].readOnly = !checked
	if(checked==false){
		$("#txtPoolQuota").val("");
	}
}

$("#id_name").change(function(){
    $("#id_tag").val(this.value);
});


$("#btnCreateErasureCodedPool").click(function(){
	//Check the field is should not null
	if(   $("#id_name").val() == ""
	   || $("#id_tag").val() == ""){

		showTip("error","The field is marked as '*' should not be empty");
		return  false;
	}


	var data = {
		"pool": {
            'name': $("#id_name").val(),
            'storageGroupId': $("#id_storage_group").val(),
            'storageGroupName': $("#id_storage_group")[0].options[$("#id_storage_group")[0].selectedIndex].text,
            'tag': $("#id_tag").val(),
            'clusterId': '0',
            'createdBy': 'VSM',
            'ecProfileId': $("#id_ec_profile").val(),
            'ecFailureDomain': $("#id_ec_failure_domain").val(),
            'enablePoolQuota':  $("#chkEnablePoolQuota")[0].checked,
            'poolQuota': $("#txtPoolQuota").val()
        }
	}

	var postData = JSON.stringify(data);
    token = $("input[name=csrfmiddlewaretoken]").val();
	$.ajax({
		type: "post",
		url: "/dashboard/vsm/poolsmanagement/create_ec_pool_action/",
		data: postData,
		dataType:"json",
		success: function(data){
				console.log(data);
				window.location.href="/dashboard/vsm/poolsmanagement/";
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

});