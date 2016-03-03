
$(function(){
    GetPoolAndRBD();
})

function ChangePool(obj){
    var pool_selected = parseInt(obj.options[obj.selectedIndex].val();)
    $.ajax({
		type: "get",
		url: "/dashboard/vsm/poolsmanagement/list_rbds_by_pool?pool=%s"%pool_selected,
		data: "",
		dataType:"json",
		success: function(data){
				console.log(data);
                var rbd_list = data.rbd_list;
                if(rbd_list.length == 0){
                    //TODO Nothing
                }
                else{
                    $("#selImage")[0].options.length = 0;
                    for(var i=0;i<rbd_list.length;i++){
                        var item = new Option()
                        item.value = rbd_list[i][0];
                        item.text = rbd_list[i][1];
                        $("#selImage")[0].options.add(item);
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
function CreateSnapshot(){
	//Check the field is should not null
	if($("#txtRBDName").val() == ""){
		showTip("error","The field is marked as '*' should not be empty");
		return  false;
	}
	var data = {
			"snapshots":[]
	}
    var snapshot = {
                'pool':$("#selPool").val(),
                'image':$("#selImage").val(),
                'name':$("#txtSnapshotName").val(),

			}
	data.snapshots.append(snapshot)
	var postData = JSON.stringify(data);
	token = $("input[name=csrfmiddlewaretoken]").val();
	$.ajax({
		type: "post",
		url: "/dashboard/vsm/rbds-management/create_snapshot/",
		data: postData,
		dataType:"json",
		success: function(data){
				//console.log(data);
                if(data.status == "OK"){
                    window.location.href="/dashboard/vsm/rbds-management/";
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


function GetPoolAndRBD(){
    $.ajax({
		type: "get",
		url: "/dashboard/vsm/poolsmanagement/list_pools_and_first_rbds/",
		data: "",
		dataType:"json",
		success: function(data){
				console.log(data);
                var pool_list = data.pool_list;
                var rbd_list = data.rbd_list;
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
                    $("#selImage")[0].options.length = 0;
                    for(var i=0;i<rbd_list.length;i++){
                        var item = new Option()
                        item.value = rbd_list[i][0];
                        item.text = rbd_list[i][1];
                        $("#selImage")[0].options.add(item);
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