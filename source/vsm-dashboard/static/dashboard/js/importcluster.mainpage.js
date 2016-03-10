$(function(){
    $("#server_list>tbody>tr>td.status_up").each(function(){
        if(this.innerHTML != "available"){
            $("#server_list__action_import_cluster").hide();
        }
    });
    if($("#server_list__action_import_cluster")[0].style.display != "none"){
        $("#server_list__action_remove_cluster").hide();
    }
    else{
        $("#server_list__action_remove_cluster").show();
    }
})
//remove the cluster
$("#server_list__action_remove_cluster").click(function(){
	var cluster_id_list = {"cluster_id_list":[1]}
	token = $("input[name=csrfmiddlewaretoken]").val();
	$.ajax({
		type: "post",
		url: "/dashboard/vsm/cluster-import/remove_cluster/",
		data: JSON.stringify(cluster_id_list),
		dataType:"json",
		success: function(data){
				//console.log(data);
                if(data.error_code.length == 0){
                    window.location.href="/dashboard/vsm/cluster-import/";
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
