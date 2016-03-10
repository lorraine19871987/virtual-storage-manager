
$(function(){
    GetPool();
})


function ChangePool(obj){
    var pool_selected = obj.options[obj.selectedIndex].text;
    $.ajax({
		type: "get",
		url: "/dashboard/vsm/rbds-management/list_rbds_by_pool?format=2&pool_name="+pool_selected,
		data: "",
		dataType:"json",
		success: function(data){
				console.log(data);
                var rbd_list = data.rbd_list;
                if(rbd_list.length == 0){
                    //TODO Nothing
                }
                else{
                    $("#selSrcImage")[0].options.length = 0;
                    for(var i=0;i<rbd_list.length;i++){
                        var item = new Option()
                        item.value = rbd_list[i][0];
                        item.text = rbd_list[i][1];
                        $("#selSrcImage")[0].options.add(item);
                    }
                    GetSnapshot(rbd_list[0][0])
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

function ChangeRBD(obj){
    var rbd_selected = obj.options[obj.selectedIndex].value;
    $.ajax({
		type: "get",
		url: "/dashboard/vsm/rbds-management/list_snapshots_by_image?rbd_id="+rbd_selected,
		data: "",
		dataType:"json",
		success: function(data){
				console.log(data);
                var snapshot_list = data.snapshot_list;
                if(snapshot_list.length == 0){
                    //TODO Nothing
                }
                else{
                    $("#selSrcSnapshot")[0].options.length = 0;
                    for(var i=0;i<snapshot_list.length;i++){
                        var item = new Option()
                        item.value = snapshot_list[i][0];
                        item.text = snapshot_list[i][1];
                        $("#selSrcSnapshot")[0].options.add(item);
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
function CloneRBD(){
	//Check the field is should not null
	if($("#txtRBDName").val() == "" || $("#selSrcSnapshot").val() == "" || $("#selDestPool").val() == ""){
		showTip("error","The field is marked as '*' should not be empty");
		return  false;
	}
	var data = {
			"rbds":[]
	}
    var rbd = {
                'src_snap_id':$("#selSrcSnapshot").val(),
                'dest_pool':$("#selDestPool")[0].options[$("#selDestPool")[0].selectedIndex].text,
                'dest_image':$("#txtRBDName").val(),
                'autosnapstart':$("#txtAutoSnapStartTime").val(),
                'autosnapinterval' :$("#txtAutoSnapInterval").val(),
			}
	data["rbds"].push(rbd)
	var postData = JSON.stringify(data);
	token = $("input[name=csrfmiddlewaretoken]").val();
	$.ajax({
		type: "post",
		url: "/dashboard/vsm/rbds-management/clone_rbd/",
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
                    $("#selSrcPool")[0].options.length = 0;
                    $("#selDestPool")[0].options.length = 0;
                    for(var i=0;i<pool_list.length;i++){
                        var item = new Option()
                        item.value = pool_list[i][0];
                        item.text = pool_list[i][1];
                        $("#selSrcPool")[0].options.add(item);
                        var item_dest = new Option()
                        item_dest.value = pool_list[i][0];
                        item_dest.text = pool_list[i][1];
                        $("#selDestPool")[0].options.add(item_dest);
                    }
                    GetRBD(pool_list[0][1])
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

function GetRBD(pool_name){
    $.ajax({
		type: "get",
		url: "/dashboard/vsm/rbds-management/list_rbds_by_pool?format=2&pool_name="+pool_name,
		data: "",
		dataType:"json",
		success: function(data){
				console.log(data);
                var rbd_list = data.rbd_list;
                if(rbd_list.length == 0){
                    //TODO Nothing
                    return 0
                }
                else{
                    $("#selSrcImage")[0].options.length = 0;
                    for(var i=0;i<rbd_list.length;i++){
                        var item = new Option()
                        item.value = rbd_list[i][0];
                        item.text = rbd_list[i][1];
                        $("#selSrcImage")[0].options.add(item);
                    }
                    GetSnapshot(rbd_list[0][0])
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

function GetSnapshot(rbd_id){
    $.ajax({
		type: "get",
		url: "/dashboard/vsm/rbds-management/list_snapshots_by_image?rbd_id="+rbd_id,
		data: "",
		dataType:"json",
		success: function(data){
				console.log(data);
                var snapshot_list = data.snapshot_list;
                if(snapshot_list.length == 0){
                    //TODO Nothing
                    return 0
                }
                else{
                    $("#selSrcSnapshot")[0].options.length = 0;
                    for(var i=0;i<snapshot_list.length;i++){
                        var item = new Option()
                        item.value = snapshot_list[i][0];
                        item.text = snapshot_list[i][1];
                        $("#selSrcSnapshot")[0].options.add(item);
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