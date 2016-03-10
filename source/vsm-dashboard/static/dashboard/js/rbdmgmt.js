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

