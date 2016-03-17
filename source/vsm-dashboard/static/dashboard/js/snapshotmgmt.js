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


//remove the snapshot
$("#snapshots__action_remove_snapshots").click(function(){
	var snapshot_id_list = {"snapshot_id_list":[]}
	
	var is_selected = false;
	var is_status_nomal = true;
	$("#snapshots>tbody>tr").each(function(){
        if(this.children[0].children[0].checked) {
            is_selected = true;
            var snapshot_id = this.children[0].children[0].value;
            var snapshot_status = this.children[6].innerHTML;
            if ( snapshot_status != 'protected'){
                snapshot_id_list["snapshot_id_list"].push(snapshot_id);
            }
            else{
                is_status_nomal = false
            }

        }
	})

    if(is_selected == false){
        showTip("warning","please select the SnapShot");
        return false;
    }
    if(is_status_nomal == false){
        showTip("warning","please only select the SnapShots which are not protected");
        return false;
    }

	token = $("input[name=csrfmiddlewaretoken]").val();
	$.ajax({
		type: "post",
		url: "/dashboard/vsm/snapshots-management/remove_snapshots/",
		data: JSON.stringify(snapshot_id_list),
		dataType:"json",
		success: function(data){
				console.log(data);
                if(data.error_code.length == 0){
                    window.location.href="/dashboard/vsm/snapshots-management/";
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

