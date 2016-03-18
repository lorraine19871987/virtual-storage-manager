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


//remove the rbd_groups
$("#rbd_groups__action_remove_rbd_groups").click(function(){
	var rbd_group_id_list = {"rbd_group_id_list":[]}
	
	var is_selected = false;

	$("#rbd_groups>tbody>tr").each(function(){
        if(this.children[0].children[0].checked) {

            var rbd_group_id = this.children[0].children[0].value;
            if (rbd_group_id != '1'){
            is_selected = true;
            rbd_group_id_list["rbd_group_id_list"].push(rbd_group_id);
            }
        }
	})

    if(is_selected == false){
        showTip("warning","please select the RBD Group except default group!");
        return false;
    }

	token = $("input[name=csrfmiddlewaretoken]").val();
	$.ajax({
		type: "post",
		url: "/dashboard/vsm/rbdgroups-management/remove_rbd_groups/",
		data: JSON.stringify(rbd_group_id_list),
		dataType:"json",
		success: function(data){
				console.log(data);
                if(data.error_code.length == 0){
                    window.location.href="/dashboard/vsm/rbdgroups-management/";
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

