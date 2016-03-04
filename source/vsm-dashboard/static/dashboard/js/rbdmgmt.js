

//flatten the rbd
$("#rbd_list__action_flatten_rbds").click(function(){
	var rbd_id_list = {"rbd_id_list":[]}
    var rbd_parent_snapshot = {"rbd_parent_snapshot":[]}
    var is_selected = false;
    var is_parent_snapshot_valid = true
	$("#rbd_list>tbody>tr").each(function(){
        if(this.children[0].children[0].checked) {
            is_selected = true;
            var rbd_id = this.children[0].children[0].value;
            var parent_snapshot = this.children[9].innerHTML;
            if ( parent_snapshot == '-'){
                is_parent_snapshot_valid = false
            }
            rbd_id_list["rbd_id_list"].push(rbd_id);

        }
	})

    if(is_selected == false){
        showTip("warning","please select the RBD");
        return false;
    }
    if(is_parent_snapshot_valid == false){
        showTip("warning","please select the RBD which has a parent snapshot");
        return false;
    }
	token = $("input[name=csrfmiddlewaretoken]").val();
	$.ajax({
		type: "post",
		url: "/dashboard/vsm/rbds-management/flatten_rbds/",
		data: JSON.stringify(rbd_id_list),
		dataType:"json",
		success: function(data){
				console.log(data);
                window.location.href= "/dashboard/vsm/rbds-management/";
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

//remove the rbd
$("#rbd_list__action_remove_rbds").click(function(){
	var rbd_id_list = {"rbd_id_list":[]}
	
	  var is_selected = false;
	$("#rbd_list>tbody>tr").each(function(){
        if(this.children[0].children[0].checked) {
            is_selected = true;
            var rbd_id = this.children[0].children[0].value;
            rbd_id_list["rbd_id_list"].push(rbd_id);
        }
	})

    if(is_selected == false){
        showTip("warning","please select the RBD");
        return false;
    }

	token = $("input[name=csrfmiddlewaretoken]").val();
	$.ajax({
		type: "post",
		url: "/dashboard/vsm/rbds-management/remove_rbds/",
		data: JSON.stringify(rbd_id_list),
		dataType:"json",
		success: function(data){
				console.log(data);
                window.location.href= "/dashboard/vsm/rbds-management/";
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

