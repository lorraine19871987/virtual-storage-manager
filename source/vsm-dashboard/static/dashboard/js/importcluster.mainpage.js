/* Copyright 2014 Intel Corporation, All Rights Reserved.

 Licensed under the Apache License, Version 2.0 (the"License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing,
 software distributed under the License is distributed on an
 "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 KIND, either express or implied. See the License for the
 specific language governing permissions and limitations
 under the License.
 */
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
