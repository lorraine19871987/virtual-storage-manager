//delete the case
$("#benchmark_case_list__action_delete_benchmark_case").click(function(){
	var case_id_list = {"case_id_list":[]};

    var is_selected = false;
	$("#benchmark_case_list>tbody>tr").each(function(){
        if(this.children[0].children[0].checked) {
            is_selected = true;
            var case_id = this.children[0].children[0].value;
            case_id_list["case_id_list"].push(case_id);
        }
	});

    if(is_selected == false){
        showTip("warning","please select the case");
        return false;
    }

	token = $("input[name=csrfmiddlewaretoken]").val();
	$.ajax({
		type: "post",
		url: "/dashboard/vsm/benchmark_case/delete_benchmark_case/",
		data: JSON.stringify(case_id_list),
		dataType:"json",
		success: function(data){
				console.log(data);
                window.location.href= "/dashboard/vsm/benchmark_case/";
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

//terminate the case
$("#benchmark_case_list__action_terminate_benchmark_case").click(function(){
	var case_id_list = {"case_id_list":[]};

    var is_selected = false;
	$("#benchmark_case_list>tbody>tr").each(function(){
        if(this.children[0].children[0].checked) {
            is_selected = true;
            var case_id = this.children[0].children[0].value;
            case_id_list["case_id_list"].push(case_id);
        }
	});

    if(is_selected == false){
        showTip("warning","please select the case");
        return false;
    }

	token = $("input[name=csrfmiddlewaretoken]").val();
	$.ajax({
		type: "post",
		url: "/dashboard/vsm/benchmark_case/terminate_benchmark_case/",
		data: JSON.stringify(case_id_list),
		dataType:"json",
		success: function(data){
				console.log(data);
                window.location.href= "/dashboard/vsm/benchmark_case/";
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

function CreateBenchmarkCase(){
	//Check the field is should not null
	var name = $("#txtBCName").val();
	var readwrite = $("#txtReadWrite").val();
	if(name == ""){
		showTip("error","The field is marked as '*' should not be empty");
		return false
	}
	if(readwrite == ""){
		showTip("error","The field is marked as '*' should not be empty");
		return false
	}
	var data = {
		'name':name,
		'readwrite':readwrite,
		'blocksize' :$("#txtBlockSize").val(),
		'iodepth':$("#txtIODepth").val(),
		'runtime':$("#txtRunTime").val(),
		'ioengine':$("#txtIOEngine").val(),
		'clientname':$("#txtClientName").val(),
		'additional_options':$("#txtAdditionalOptions").val()
	};
	var postData = JSON.stringify(data);
	token = $("input[name=csrfmiddlewaretoken]").val();
	$.ajax({
		type: "post",
		url: "/dashboard/vsm/benchmark_case/add_benchmark_case/",
		data: postData,
		dataType:"json",
		success: function(data){
				//console.log(data);
                if(data.error_code == 0){
                    window.location.href="/dashboard/vsm/benchmark_case/";
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